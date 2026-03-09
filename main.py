import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- CONFIGURAÇÃO ---
st.set_page_config(page_title="Frota Setor", layout="centered")
conn = st.connection("gsheets", type=GSheetsConnection)

# --- FUNÇÕES DE DADOS ---
def carregar_veiculos():
    return conn.read(worksheet="veiculos", ttl="1m") # ttl=1m atualiza a cada minuto

def registrar_viagem(dados):
    # Aqui adicionamos a linha na aba 'logs_viagens'
    conn.create(worksheet="logs_viagens", data=dados)
    st.cache_data.clear() # Limpa o cache para ler o dado novo

# --- INTERFACE DE LOGIN ---
if 'motorista_autenticado' not in st.session_state:
    st.title("🚗 Identificação do Condutor")
    with st.form("login"):
        nome = st.text_input("Nome Completo")
        cpf = st.text_input("CPF (Somente números)")
        placa = st.selectbox("Veículo", carregar_veiculos()['placa'])
        entrar = st.form_submit_button("Iniciar Turno")
        
        if entrar and nome and cpf:
            st.session_state.motorista_autenticado = True
            st.session_state.nome = nome
            st.session_state.cpf = cpf
            st.session_state.placa = placa
            st.rerun()
else:
    # --- PAINEL DE CONTROLE DO MOTORISTA ---
    st.title(f"Olá, {st.session_state.nome}!")
    st.info(f"Veículo Atual: **{st.session_state.placa}**")
    
    # Busca o KM atual do veículo na planilha
    df_v = carregar_veiculos()
    km_sistema = df_v[df_v['placa'] == st.session_state.placa]['km_atual'].values[0]

    aba1, aba2 = st.tabs(["🚀 Iniciar Viagem", "🏁 Finalizar Viagem"])

    with aba1:
        st.subheader("Registrar Saída")
        origem = st.text_input("Local de Saída", value="Sede")
        km_saida = st.number_input("Confirme o KM de Saída", value=int(km_sistema))
        destino_previsto = st.text_input("Destino")
        
        if st.button("Confirmar Saída"):
            # Aqui simulamos o início (num sistema real, salvaríamos o status 'Em Trânsito')
            st.success(f"Viagem iniciada! Saída de {origem} com {km_saida} KM.")
            st.balloons()

    with aba2:
        st.subheader("Registrar Chegada")
        km_chegada = st.number_input("KM de Chegada", min_value=int(km_sistema))
        local_chegada = st.text_input("Local de Chegada")
        
        if st.button("Finalizar e Salvar"):
            if km_chegada > km_sistema:
                distancia = km_chegada - km_sistema
                st.write(f"✅ Viagem concluída! Você percorreu {distancia} km.")
                # O PRÓXIMO PASSO será a função que envia esses dados para a aba 'logs_viagens'
            else:
                st.error("O KM de chegada não pode ser menor ou igual ao de saída!")

    if st.button("Sair / Trocar Motorista"):
        del st.session_state.motorista_autenticado
        st.rerun()
