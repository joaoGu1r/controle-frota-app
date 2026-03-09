import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Frota Setor", layout="centered")

# Título do App
st.title("🚗 Controle de Frota")

# 1. Tentativa de Conexão
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # 2. Lendo os dados (TTL=0 força o app a buscar dado novo sem cache agora)
    df_veiculos = conn.read(worksheet="veiculos", ttl=0)
    
    st.success("Conexão com a planilha estabelecida!")
    
    # 3. Interface de Identificação (Fora de um formulário por enquanto para evitar erros)
    nome = st.text_input("Nome Completo")
    cpf = st.text_input("CPF (Somente números)")
    
    # Criamos a lista de placas a partir da coluna 'placa' da planilha
    lista_placas = df_veiculos['placa'].tolist()
    placa_selecionada = st.selectbox("Selecione o Veículo", lista_placas)

    if st.button("Acessar Painel"):
        if nome and cpf:
            st.session_state.nome = nome
            st.session_state.cpf = cpf
            st.session_state.placa = placa_selecionada
            st.write(f"Bem-vindo, {nome}! Você selecionou o carro {placa_selecionada}.")
        else:
            st.error("Preencha todos os campos.")

except Exception as e:
    st.error("Erro de Conexão!")
    st.write("O erro detalhado é:", e)
    st.info("Verifique se o link da planilha nas 'Secrets' está correto e se a aba se chama 'veiculos'.")
