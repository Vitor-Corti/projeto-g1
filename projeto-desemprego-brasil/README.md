# 📉 Evolução do Desemprego no Brasil (2015–2024)

Projeto G2 – Tema 4: análise e visualização de dados sobre o comportamento do desemprego no Brasil, com notebook de análise e dashboard interativo em Streamlit.

> ⚠️ Os dados são **simulados** e servem para fins didáticos. Não representam estatísticas oficiais (IBGE/PNAD).

## 🔗 Links

| Recurso | Endereço |
|---|---|
| Código-fonte (GitHub) | https://github.com/Vitor-Corti/projeto-g1/tree/main/projeto-desemprego-brasil |
| Página do projeto (GitHub Pages) | https://vitor-corti.github.io/siteIndiceDesemprego/ |
| Dashboard (Streamlit Cloud) | https://projeto-g1vitoor.streamlit.app/ |

## 🎯 Objetivo

Investigar a evolução do desemprego entre 2015 e 2024, identificando tendências, períodos de crise, regiões e estados mais afetados e a relação do desemprego com renda e inflação.

## 📁 Estrutura

```
projeto-desemprego-brasil/
├── app.py                       # Dashboard Streamlit
├── requirements.txt             # Dependências
├── README.md
├── index.html                   # Página para o GitHub Pages
├── dados/
│   └── simulacao_desemprego_brasil.csv
├── notebooks/
│   └── analise_desemprego.ipynb # Análise completa
├── database/                    # Reservado (ex.: SQLite)
└── imagens/                     # 13 gráficos exportados do notebook
```

## 🗂️ Base de dados

800 registros: 20 UFs × 10 anos × 4 trimestres, sem valores nulos ou duplicados.

| Coluna | Descrição |
|---|---|
| ano, trimestre, data | Período de referência |
| regiao, uf | Região e estado |
| populacao_ativa, empregados, desempregados | Estoques trimestrais (empregados + desempregados = população ativa) |
| taxa_desemprego | Percentual de desemprego |
| renda_media | Renda média mensal (R$) |
| setor_predominante | Principal setor econômico |
| vagas_formais | Novas vagas formais |
| inflacao | Inflação (%) |
| nivel_risco | Baixo, Médio, Alto ou Crítico |

## 🚀 Como executar

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU-USUARIO/projeto-desemprego-brasil.git
cd projeto-desemprego-brasil

# 2. (Opcional) criar ambiente virtual
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Abrir o dashboard
streamlit run app.py
```

O dashboard abre em `http://localhost:8501`. Para o notebook, abra `notebooks/analise_desemprego.ipynb` no Jupyter ou no Google Colab (no Colab, envie o CSV quando solicitado).

## 📊 Dashboard

- **KPIs:** taxa média, estado com maior desemprego, região mais afetada, desempregados (último trimestre), renda média e evolução no período.
- **Filtros:** ano, trimestre, região, estado, setor e nível de risco.
- **Gráficos:** linha temporal, barras por região e por estado, dispersão renda × desemprego e heatmap ano × trimestre.
- **Tabela dinâmica** configurável, **interpretação textual** em cada bloco e **conclusão executiva**.

## 🔎 Principais resultados

- O desemprego **caiu de 9,97% (2015) para 8,43% (2024)**, o menor valor da série.
- **2016, 2020 e 2021** são anos de crise (acima de média + 1 desvio-padrão = 11,01%); o pior trimestre foi 2020-T3 (11,85%).
- **Nordeste (13,28%) vs. Sul (6,79%):** CE, PB, BA, PE e MA são os 5 estados com maior desemprego.
- 37% dos trimestres do Nordeste estão em nível de risco **Crítico**; Sul e Centro-Oeste nunca chegam a esse nível.
- Renda, inflação e vagas formais têm correlação ≈ 0 com o desemprego **neste dataset simulado**.

## 🧪 Decisões metodológicas

- **Taxa ponderada** (`soma de desempregados / soma da população ativa`) apresentada junto da média simples.
- **Total de desempregados:** somar trimestres repete as mesmas pessoas; por isso o dashboard usa o último trimestre.
- **Crises** definidas por critério objetivo (média + 1 desvio-padrão da série anual).

## ⚠️ Limitações

Dados simulados; apenas 20 dos 27 estados; sem recortes por sexo, idade ou escolaridade; setor predominante varia de forma aleatória no tempo.

## 🛠️ Tecnologias

Python · Pandas · NumPy · Matplotlib · Seaborn · Streamlit · GitHub · GitHub Pages

## 👤 Autor

**Vitor Cristino Corti**  
Disciplina: Linguagens de Programação  
Professor: Alexandre Neves Louzada
