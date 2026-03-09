import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Teste de Conexão Google Sheets")

# Criando a conexão
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Tenta ler a planilha sem especificar aba primeiro (para testar a URL)
    df = conn.read()
    st.success("Conexão bem-sucedida!")
    st.write("Aqui estão os dados encontrados:")
    st.dataframe(df)

except Exception as e:
    st.error("Ainda temos um problema no link das Secrets.")
    st.write(f"Erro técnico: {e}")
    st.info("Dica: Copie a URL da planilha e cole apenas até a parte do ID, ignorando o /edit.")
