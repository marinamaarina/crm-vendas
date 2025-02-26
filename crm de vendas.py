import streamlit as st
import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("crm.db")
cursor = conn.cursor()

# Criar tabela se não existir
cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    contato TEXT,
                    status TEXT
                )''')
conn.commit()

# Título
title = "CRM de Vendas - Sacolas e Sacos de Lixo"
st.title(title)

# Formulário para adicionar lead
st.subheader("Adicionar Novo Lead")
nome = st.text_input("Nome da Empresa")
contato = st.text_input("Contato (WhatsApp/E-mail)")
status = st.selectbox("Status", ["Novo Lead", "Em negociação", "Fechado", "Perdido"])

if st.button("Adicionar Lead"):
    cursor.execute("INSERT INTO leads (nome, contato, status) VALUES (?, ?, ?)",
                   (nome, contato, status))
    conn.commit()
    st.success("Lead adicionado com sucesso!")
    st.experimental_rerun()

# Mostrar leads cadastrados
st.subheader("Leads Cadastrados")
cursor.execute("SELECT * FROM leads")
leads = cursor.fetchall()

for lead in leads:
    st.write(f"📌 {lead[1]} - {lead[2]} | Status: {lead[3]}")
    
    # Opção para atualizar status
    novo_status = st.selectbox(f"Atualizar Status de {lead[1]}", ["Novo Lead", "Em negociação", "Fechado", "Perdido"], key=lead[0])
    if st.button(f"Atualizar {lead[1]}", key=f"update_{lead[0]}"):
        cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (novo_status, lead[0]))
        conn.commit()
        st.success("Status atualizado!")
        st.experimental_rerun()
    
    # Opção para excluir lead
    if st.button(f"Excluir {lead[1]}", key=f"delete_{lead[0]}"):
        cursor.execute("DELETE FROM leads WHERE id = ?", (lead[0],))
        conn.commit()
        st.warning("Lead removido!")
        st.experimental_rerun()

# Fechar conexão
conn.close()
