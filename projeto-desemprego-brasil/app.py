"""Dashboard – Evolução do Desemprego no Brasil (2015–2024)
Execute com:  streamlit run app.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Desemprego no Brasil", page_icon="📉", layout="wide")
sns.set_theme(style="whitegrid")

CSV = Path(__file__).parent / "dados" / "simulacao_desemprego_brasil.csv"
RISCOS = ["Baixo", "Médio", "Alto", "Crítico"]


@st.cache_data
def carregar() -> pd.DataFrame:
    df = pd.read_csv(CSV, parse_dates=["data"])
    df["nivel_risco"] = pd.Categorical(df["nivel_risco"], RISCOS, ordered=True)
    return df


def taxa_pond(d: pd.DataFrame) -> float:
    return d["desempregados"].sum() / d["populacao_ativa"].sum() * 100


df = carregar()

# ---------- Cabeçalho ----------
st.title("📉 Evolução do Desemprego no Brasil (2015–2024)")
st.markdown(
    "**Problema:** como o desemprego evoluiu no país, quais regiões e estados são mais "
    "afetados e quando ocorreram os períodos de crise? "
    "*(Base simulada com 20 UFs, 40 trimestres.)*"
)

# ---------- Filtros ----------
st.sidebar.header("Filtros")
f_ano = st.sidebar.multiselect("Ano", sorted(df["ano"].unique()), default=sorted(df["ano"].unique()))
f_tri = st.sidebar.multiselect("Trimestre", [1, 2, 3, 4], default=[1, 2, 3, 4])
f_reg = st.sidebar.multiselect("Região", sorted(df["regiao"].unique()), default=sorted(df["regiao"].unique()))
ufs_disp = sorted(df[df["regiao"].isin(f_reg)]["uf"].unique())
f_uf = st.sidebar.multiselect("Estado", ufs_disp, default=ufs_disp)
f_set = st.sidebar.multiselect("Setor", sorted(df["setor_predominante"].unique()),
                               default=sorted(df["setor_predominante"].unique()))
f_ris = st.sidebar.multiselect("Nível de risco", RISCOS, default=RISCOS)

d = df[df["ano"].isin(f_ano) & df["trimestre"].isin(f_tri) & df["regiao"].isin(f_reg)
       & df["uf"].isin(f_uf) & df["setor_predominante"].isin(f_set) & df["nivel_risco"].isin(f_ris)]
if d.empty:
    st.warning("Nenhum registro para os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ---------- KPIs ----------
uf_rank = d.groupby("uf")["taxa_desemprego"].mean().sort_values(ascending=False)
reg_rank = d.groupby("regiao")["taxa_desemprego"].mean().sort_values(ascending=False)
anual = d.groupby("ano")["taxa_desemprego"].mean()
delta = anual.iloc[-1] - anual.iloc[0] if len(anual) > 1 else 0.0

c1, c2, c3 = st.columns(3)
c1.metric("Taxa média de desemprego", f"{d['taxa_desemprego'].mean():.2f}%")
c2.metric("Estado com maior desemprego", uf_rank.index[0], f"{uf_rank.iloc[0]:.2f}%", delta_color="off")
c3.metric("Região mais afetada", reg_rank.index[0], f"{reg_rank.iloc[0]:.2f}%", delta_color="off")
c4, c5, c6 = st.columns(3)
ult = d[d["data"] == d["data"].max()]
c4.metric("Desempregados (último trimestre)", f"{ult['desempregados'].sum():,.0f}".replace(",", "."),
          help="Soma de estoques trimestrais repetiria as mesmas pessoas; por isso usamos o último trimestre filtrado.")
c5.metric("Renda média nacional", f"R$ {d['renda_media'].mean():,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
c6.metric(f"Evolução {anual.index[0]}→{anual.index[-1]}", f"{anual.iloc[-1]:.2f}%", f"{delta:+.2f} p.p.", delta_color="inverse")

# ---------- Gráficos ----------
st.subheader("Evolução temporal")
tri = d.groupby("data")["taxa_desemprego"].mean()
fig, ax = plt.subplots(figsize=(12, 4))
ax.plot(tri.index, tri.values, color="#d9534f", lw=2)
ax.fill_between(tri.index, tri.values, alpha=.15, color="#d9534f")
ax.set_ylabel("Taxa média (%)")
st.pyplot(fig)
st.info("**Interpretação:** a série mostra dois picos: a recessão de 2015-16 e a pandemia de 2020-21, "
        "seguidos de queda em 2022. Use os filtros para isolar regiões ou estados.")

col_a, col_b = st.columns(2)
with col_a:
    st.subheader("Comparação por região")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=reg_rank.index, y=reg_rank.values, hue=reg_rank.index, palette="Reds_r", legend=False, ax=ax)
    for c in ax.containers:
        ax.bar_label(c, fmt="%.2f%%", padding=2)
    ax.set_xlabel(""); ax.set_ylabel("Taxa média (%)")
    st.pyplot(fig)
with col_b:
    st.subheader("Comparação por estado")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(x=uf_rank.index, y=uf_rank.values, hue=uf_rank.index, palette="Blues_r", legend=False, ax=ax)
    ax.set_xlabel(""); ax.set_ylabel("Taxa média (%)"); plt.setp(ax.get_xticklabels(), rotation=45)
    st.pyplot(fig)
st.info(f"**Interpretação:** no recorte atual, **{reg_rank.index[0]}** tem a maior taxa "
        f"({reg_rank.iloc[0]:.2f}%) e **{reg_rank.index[-1]}** a menor ({reg_rank.iloc[-1]:.2f}%): "
        f"diferença de {reg_rank.iloc[0] - reg_rank.iloc[-1]:.1f} p.p., o que indica desigualdade regional estrutural.")

col_c, col_d = st.columns(2)
with col_c:
    st.subheader("Renda × desemprego")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.scatterplot(data=d, x="renda_media", y="taxa_desemprego", hue="regiao", alpha=.7, ax=ax)
    ax.set_xlabel("Renda média (R$)"); ax.set_ylabel("Desemprego (%)")
    st.pyplot(fig)
    st.caption(f"Correlação renda × desemprego: {d['renda_media'].corr(d['taxa_desemprego']):.3f} | "
               f"inflação × desemprego: {d['inflacao'].corr(d['taxa_desemprego']):.3f}")
with col_d:
    st.subheader("Heatmap trimestral")
    piv = d.pivot_table(index="ano", columns="trimestre", values="taxa_desemprego", aggfunc="mean")
    fig, ax = plt.subplots(figsize=(6, 4))
    sns.heatmap(piv, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax)
    st.pyplot(fig)
st.info("**Interpretação:** as correlações próximas de zero indicam que, nesta base simulada, renda e inflação "
        "não explicam o desemprego. O heatmap evidencia 2016 e 2020-21 como os períodos mais críticos.")

# ---------- Tabela dinâmica ----------
st.subheader("Tabela dinâmica")
lin = st.selectbox("Linhas", ["regiao", "uf", "ano", "setor_predominante", "nivel_risco"])
col = st.selectbox("Colunas", ["trimestre", "ano", "regiao", "setor_predominante", "nivel_risco"], index=1)
val = st.selectbox("Valor", ["taxa_desemprego", "renda_media", "inflacao", "vagas_formais", "desempregados"])
if lin == col:
    st.warning("Escolha linhas e colunas diferentes.")
else:
    st.dataframe(d.pivot_table(index=lin, columns=col, values=val, aggfunc="mean", observed=True).round(2),
                 use_container_width=True)

# ---------- Conclusão ----------
st.subheader("Conclusão executiva")
st.success(
    "• O desemprego **caiu** de 9,97% (2015) para 8,43% (2024), apesar de dois choques (2015-16 e 2020-21).\n\n"
    "• A **desigualdade regional** é o principal achado: Nordeste (13,28%) vs. Sul (6,79%); os 5 estados com maior "
    "desemprego (CE, PB, BA, PE, MA) são nordestinos.\n\n"
    "• Renda e inflação **não** explicam o desemprego nesta base simulada.\n\n"
    "• **Recomendação:** priorizar políticas de emprego e qualificação no Nordeste e acompanhar o nível de risco."
)
