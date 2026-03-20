import streamlit as st

# Usuários fixos (depois vamos melhorar isso)
USERS = {
    "admin": "1234",
    "user": "1234"
}

def login():
    st.subheader("🔐 Login")

    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        if username in USERS and USERS[username] == password:
            st.session_state["logado"] = True
            st.success("Login realizado com sucesso!")
            st.rerun()
        else:
            st.error("Usuário ou senha inválidos")