import pandas as pd
import folium
from folium.plugins import HeatMap
import unicodedata
import os

def normalizar_texto(txt):
    if pd.isna(txt): return ""
    txt = str(txt).upper().strip()
    return "".join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

# 1. Caminhos
caminho_excel = r'Dados\PAINEL DE DESEMPENHO DAS DISTRIBUIDORAS POR MUNICIPIO.xlsx'
caminho_csv   = r'Dados\municipios.csv'

if not os.path.exists(caminho_excel):
    print(f"\n[ERRO] Arquivo não encontrado: {os.path.abspath(caminho_excel)}")
else:
    # 2. Carregamento
    df_aneel  = pd.read_excel(caminho_excel, sheet_name=0)
    df_coords = pd.read_csv(caminho_csv)

    # 3. Normalização para merge
    df_aneel['chave']  = df_aneel[df_aneel.columns[1]].apply(normalizar_texto)
    df_coords['chave'] = df_coords['nome'].apply(normalizar_texto)

    # 4. Cruzamento Geográfico
    df_mapa = pd.merge(df_aneel, df_coords, on='chave', how='inner')

    # 5. Cálculo de Criticidade por ÍNDICE (H=7 e I=8 = FEC e FEC Limite)
    # Índice 7 = FEC | Índice 8 = FEC Limite
    col_fec       = df_mapa.columns[7]
    col_fec_limite = df_mapa.columns[8]
    df_mapa['peso_calor'] = df_mapa[col_fec] / df_mapa[col_fec_limite]

    # Filtro: apenas municípios com descumprimento (peso > 1)
    df_critico = df_mapa[df_mapa['peso_calor'] > 1].copy()

    # 6. Construção do Mapa (centralizado no Paraná)
    mapa = folium.Map(location=[-24.8, -51.5], zoom_start=7, tiles='cartodbpositron')
    dados_calor = df_critico[['latitude', 'longitude', 'peso_calor']].values.tolist()

    HeatMap(dados_calor, radius=15, blur=12, max_zoom=10,
            gradient={0.3: 'blue', 0.5: 'cyan', 0.7: 'purple', 1: 'red'}).add_to(mapa)

    # 7. Salvar
    mapa.save('Mapa_FEC_Qualidade_Energia_2025.html')
    print(f"\nSucesso! Gerado mapa FEC com {len(df_critico)} municípios acima da meta.\n")


# --- NOTAS ---
# FEC (Frequência de Interrupção Equivalente por Unidade Consumidora):
#   Mede QUANTAS VEZES a energia foi interrompida no ano (contagem de eventos).
#   Diferente do DEC, que mede a DURAÇÃO total das interrupções em horas.
#
# Colunas usadas (por índice para evitar problemas de encoding):
#   Índice 7 → FEC (valor realizado pela distribuidora)
#   Índice 8 → FEC Limite (meta máxima permitida pela ANEEL)
#
# peso_calor = FEC / FEC Limite
#   > 1.0 → descumprimento de meta (plotado no mapa)
#   ≤ 1.0 → dentro da meta (ignorado)
#
# Gradiente de cores (Azul → Ciano → Roxo → Vermelho):
#   Azul/Ciano claro : peso entre 1.0 e 1.5 (excesso leve de interrupções)
#   Roxo             : peso entre 1.5 e 2.0 (excesso moderado)
#   Vermelho intenso : peso acima de 2.0 (área crítica — mais que o dobro do permitido)
