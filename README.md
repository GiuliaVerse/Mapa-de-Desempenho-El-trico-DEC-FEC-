# ⚡ ANEEL Quality Heatmap — Analisador Geográfico de Desempenho Elétrico (DEC & FEC)

Este repositório contém uma solução completa para extração, tratamento, análise espacial e visualização de dados de qualidade do fornecimento de energia elétrica nos municípios brasileiros, com base nos dados oficiais da **ANEEL (Agência Nacional de Energia Elétrica)**[cite: 1, 2, 3, 4].

O projeto identifica áreas críticas que descumprem as metas regulatórias de **DEC** (*Duração Equivalente de Interrupção por Unidade Consumidora*) e **FEC** (*Frequência Equivalente de Interrupção por Unidade Consumidora*), gerando mapas de calor interativos em formato web[cite: 1, 2, 3, 4].

---

## 📌 Funcionalidades

- **Tratamento e Normalização de Dados**: Processamento de planilhas complexas da ANEEL utilizando `pandas`, removendo acentuações e caracteres especiais para *join* geográfico preciso.
- **Cálculo de Razão de Criticidade (Peso)**: Filtro dinâmico que isola apenas municípios com estouro de meta ($\text{Peso} = \frac{\text{Realizado}}{\text{Limite}} > 1.0$)[cite: 1, 2].
- **Geração de Mapas de Calor Interativos**:
  - **Script Python**: Automação utilizando `folium` e `HeatMap` para exportação rápida de relatórios estáticos/HTML[cite: 1, 2].
  - **Painel Web (HTML/JS standalone)**: Dashboards modernos com `Leaflet.js` e `Leaflet.heat`, oferecendo filtros de opacidade, raio de calor, seleção de mapas base (Escuro, Topográfico, Satélite) e marcadores interativos com métricas detalhadas.

---

## 🛠️ Tecnologias Utilizadas

### Backend / Data Processing
- **Python 3.x**[cite: 1, 2]
- **Pandas**: Manipulação, saneamento e agrupamento de dados[cite: 1, 2]
- **Folium**: Visualização geoespacial rápida em Python[cite: 1, 2]
- **Unicodedata & OS**: Normalização de textos e checagem de integridade de arquivos[cite: 1, 2]

### Frontend / Data Visualization
- **HTML5 & CSS3**: Interface customizada no estilo *Dark Theme* inspirada em dashboards analíticos modernos[cite: 3, 4]
- **JavaScript (ES6+)**[cite: 3, 4]
- **Leaflet.js & Leaflet.heat**: Renderização performática de camadas geográficas e manchas de calor[cite: 3, 4]

---

## 📂 Estrutura do Repositório

```text
├── Dados/
│   ├── PAINEL DE DESEMPENHO DAS DISTRIBUIDORAS POR MUNICIPIO.xlsx
│   └── municipios.csv
├── gerador_mapa_dec.py       # Script Python para geração do Mapa de Calor de DEC
├── gerador_mapa_fec.py       # Script Python para geração do Mapa de Calor de FEC
├── mapa_dec_interactive.html # Dashboard Web standalone do DEC
├── mapa_fec_interactive.html # Dashboard Web standalone do FEC
└── README.md
