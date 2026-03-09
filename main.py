import streamlit as st

st.title("🚗 Controle de Frota - Setor")
st.write("O app está online! Próximo passo: Conectar a Planilha.")

nome = st.text_input("Nome do Motorista")
cpf = st.text_input("CPF")

if st.button("Acessar Sistema"):
    st.success(f"Olá {nome}, sistema em desenvolvimento!")
