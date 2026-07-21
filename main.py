import pandas as pd
import folium
from folium.plugins import HeatMap
import unicodedata
import os

# Função para normalizar nomes (remove acentos e espaços)
def normalizar_texto(txt):
    if pd.isna(txt): return ""
    txt = str(txt).upper().strip()
    return "".join(c for c in unicodedata.normalize('NFD', txt) if unicodedata.category(c) != 'Mn')

# 1. Caminhos - Ajustado com acentuação conforme seu sistema de arquivos
caminho_excel = r'Dados\PAINEL DE DESEMPENHO DAS DISTRIBUIDORAS POR MUNICIPIO.xlsx'
caminho_csv = r'Dados\municipios.csv'

# Verificação de segurança: avisa se o arquivo sumiu ou mudou de nome
if not os.path.exists(caminho_excel):
    print(f"\n[ERRO] Arquivo não encontrado: {os.path.abspath(caminho_excel)}")
else:
    # 2. Carregamento - sheet_name=0 carrega a PRIMEIRA aba, independente do nome
    df_aneel = pd.read_excel(caminho_excel, sheet_name=0) 
    df_coords = pd.read_csv(caminho_csv)

    # 3. Tratamento de Dados (Merge Prep)
    # Pegamos a coluna de Município pela posição (2ª coluna, índice 1)
    col_municipio_excel = df_aneel.columns[1]
    df_aneel['chave'] = df_aneel[col_municipio_excel].apply(normalizar_texto)
    df_coords['chave'] = df_coords['nome'].apply(normalizar_texto)

    # 4. Cruzamento Geográfico
    df_mapa = pd.merge(df_aneel, df_coords, on='chave', how='inner')

    # 5. Cálculo de Criticidade por ÍNDICE (F=5 e G=6)
    # Isso evita erros com caracteres complexos como 'DEC³' ou espaços fantasmas
    col_dec = df_mapa.columns[5]
    col_limite = df_mapa.columns[6]
    df_mapa['peso_calor'] = df_mapa[col_dec] / df_mapa[col_limite]

    # Filtro: Áreas com descumprimento de meta (Peso > 1)
    df_critico = df_mapa[df_mapa['peso_calor'] > 1].copy()

    # 6. Construção do Mapa (Centralizado no Paraná)
    mapa = folium.Map(location=[-24.8, -51.5], zoom_start=7, tiles='cartodbpositron')
    dados_calor = df_critico[['latitude', 'longitude', 'peso_calor']].values.tolist()

    HeatMap(dados_calor, radius=15, blur=12, max_zoom=10, 
            gradient={0.4: 'blue', 0.6: 'yellow', 0.8: 'orange', 1: 'red'}).add_to(mapa)

    # 7. Salvando o mapa final
    mapa.save('Mapa_Qualidade_Energia_2025.html')
    print(f"\nSucesso! Gerado mapa com {len(df_critico)} municípios acima da meta no PR.\n")
    
    
#  O script possui uma trava de segurança: ele só plota no mapa municípios onde o resultado da sua conta for maior que 1.0 
# (df_critico = df_mapa[df_mapa['peso_calor'] > 1]).

# Se Resultado <= 1.0: O município ou conjunto elétrico está dentro da meta da ANEEL e é ignorado pelo mapa de calor (área fria).

# Se Resultado > 1.0: O local está descumprindo a meta e "acende" uma mancha no mapa.

# 2. Intensidade das Cores
# A "quente" ou "vermelha" uma mancha aparece depende da gravidade do descumprimento:

# Manchas Azuis/Amarelas Claras: Valores próximos a 1.1 ou 1.2 (excesso leve).

# Manchas Laranjas/Vermelhas: Valores altos como 1.5, 2.0 ou superiores 
#(interrupções duraram o dobro do permitido), gerando os núcleos de calor intensos que você vê no Norte e Oeste do Paraná.


# O HeatMap (Soma de Intensidade): O plugin HeatMap do Folium funciona por densidade e acúmulo. Quando ele encontra vários pontos no mesmo local, ele não cria manchas separadas; ele "soma" a intensidade deles.

# Resultado: Aquela mancha amarela/vermelha no Alto da Glória é a soma de todos os problemas de Curitiba. Ela está "quente" porque ali estão empilhados os descumprimentos da CIC, Tatuquara e outros.