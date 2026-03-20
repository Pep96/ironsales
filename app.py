import streamlit as st
import pandas as pd
from datetime import datetime
from auth import login

st.set_page_config(page_title="IronSales", layout="wide")

# ====== LOGO ======
st.image("logo.png", width=150)

# ====== TÍTULO ======
st.markdown("## 🚀 IronSales")
st.caption("Controle inteligente de vendas")

# ====== CONTROLE DE LOGIN ======
if "logado" not in st.session_state:
    st.session_state["logado"] = False

if not st.session_state["logado"]:
    login()
    st.stop()

# ====== BANCO ======
try:
    df = pd.read_csv("data/vendas.csv")
except:
    df = pd.DataFrame(columns=["cliente", "valor", "status", "data"])
    df.to_csv("data/vendas.csv", index=False)

# ====== MENU ======
menu = st.sidebar.selectbox("Menu", ["Dashboard", "Nova Venda", "Pipeline"])

# ====== DASHBOARD ======
if menu == "Dashboard":
    st.subheader("📊 Visão Geral")

    total = df["valor"].sum()
    fechadas = df[df["status"] == "Fechado"].shape[0]

    col1, col2 = st.columns(2)
    col1.metric("💰 Total em vendas", f"R$ {total}")
    col2.metric("✅ Vendas fechadas", fechadas)

    # 📊 gráfico melhorado
    if not df.empty:
        st.bar_chart(df.groupby("status")["valor"].sum())

    # 🚨 ALERTAS
    st.subheader("🚨 Alertas")

    df["data"] = pd.to_datetime(df["data"], errors='coerce')
    df["dias"] = (pd.Timestamp.now() - df["data"]).dt.days

    alertas = df[(df["status"] != "Fechado") & (df["dias"] > 3)]

    if not alertas.empty:
        st.warning(f"⚠️ {len(alertas)} vendas estão paradas há mais de 3 dias!")
        st.dataframe(alertas)
    else:
        st.success("Tudo sob controle! 🚀")

# ====== NOVA VENDA ======
elif menu == "Nova Venda":
    st.subheader("➕ Adicionar Venda")

    cliente = st.text_input("Cliente")
    valor = st.number_input("Valor", min_value=0.0)
    status = st.selectbox("Status", ["Lead", "Negociação", "Fechado"])

    if st.button("Salvar"):
        nova = pd.DataFrame([[cliente, valor, status, datetime.now()]],
                            columns=df.columns)

        df = pd.concat([df, nova], ignore_index=True)
        df.to_csv("data/vendas.csv", index=False)

        st.success("Venda salva!")

# ====== PIPELINE ======
elif menu == "Pipeline":
    st.subheader("📌 Pipeline de Vendas")

    col1, col2, col3 = st.columns(3)

    col1.write("### 🟡 Lead")
    col1.dataframe(df[df["status"] == "Lead"])

    col2.write("### 🟠 Negociação")
    col2.dataframe(df[df["status"] == "Negociação"])

    col3.write("### 🟢 Fechado")
    col3.dataframe(df[df["status"] == "Fechado"])