import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Frota Setor", page_icon="🚗")

# --- CONEXÃO COM O GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNÇÃO PARA CARREGAR DADOS ---
def carregar_dados():
    # Lê a aba 'veiculos' (certifique-se que o nome na planilha está igual)
    return conn.read(worksheet="veiculos")

# --- INTERFACE ---
st.title("🚗 Controle de Frota - Conectado!")

try:
    df_veiculos = carregar_dados()
    
    st.subheader("Veículos Disponíveis")
    # Mostra apenas as colunas importantes para o motorista ver
    st.dataframe(df_veiculos[['placa', 'modelo', 'km_atual', 'status']], use_container_width=True)

    # Formulário de Identificação
    with st.form("identificacao"):
        st.write("### Identifique-se para iniciar")
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF (apenas números)")
        veiculo_selecionado = st.selectbox("Selecione o Veículo", df_veiculos['placa'].tolist())
        
        btn_entrar = st.form_submit_button("Acessar Painel do Veículo")

    if btn_entrar:
        if nome and cpf:
            st.success(f"Motorista {nome} identificado! Veículo: {veiculo_selecionado}")
            # Próximo passo será a lógica de check-in/check-out aqui
        else:
            st.warning("Por favor, preencha nome e CPF.")

except Exception as e:
    st.error("Erro ao conectar com a planilha. Verifique se o link nas Secrets está correto!")
    st.info("Dica: O nome da aba na planilha deve ser 'veiculos' (minúsculo).")
