import streamlit as st
import pandas as pd

# Título do Aplicativo
st.title("CRM de Vendas")

# Função para carregar os dados
@st.cache
def load_data():
    data = {
        "Cliente": ["Alice", "Bob", "Carlos"],
        "Produto": ["Produto A", "Produto B", "Produto C"],
        "Valor": [100, 200, 300],
        "Data": ["2023-02-26", "2023-02-27", "2023-02-28"]
    }
    return pd.DataFrame(data)

# Carregar dados
df = load_data()

# Exibir Tabela
st.write("Tabela de Vendas")
st.dataframe(df)

# Formulário para Adicionar Nova Venda
with st.form("add_sale"):
    cliente = st.text_input("Cliente")
    produto = st.text_input("Produto")
    valor = st.number_input("Valor", min_value=0.0)
    data = st.date_input("Data")
    submitted = st.form_submit_button("Adicionar")

    if submitted:
        new_row = {"Cliente": cliente, "Produto": produto, "Valor": valor, "Data": data}
        df = df.append(new_row, ignore_index=True)
        st.success("Venda adicionada com sucesso!")
        st.dataframe(df)

# Botão para Exportar Dados
if st.button("Exportar para CSV"):
    df.to_csv("vendas.csv", index=False)
    st.success("Dados exportados para vendas.csv")

