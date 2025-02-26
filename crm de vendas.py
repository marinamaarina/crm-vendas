import streamlit as st
import sqlite3

def get_connection():
    return sqlite3.connect(":memory:", check_same_thread=False)

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS leads (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT,
                        contato TEXT,
                        status TEXT
                    )''')
    conn.commit()
    conn.close()

def add_lead(nome, contato, status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO leads (nome, contato, status) VALUES (?, ?, ?)",
                   (nome, contato, status))
    conn.commit()
    conn.close()

def get_leads():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leads")
    leads = cursor.fetchall()
    conn.close()
    return leads

def update_status(lead_id, novo_status):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE leads SET status = ? WHERE id = ?", (novo_status, lead_id))
    conn.commit()
    conn.close()

def delete_lead(lead_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
    conn.commit()
    conn.close()

st.title("CRM de Vendas - Sacolas e Sacos de Lixo")

create_table()

st.subheader("Adicionar Novo Lead")
nome = st.text_input("Nome da Empresa")
contato = st.text_input("Contato (WhatsApp/E-mail)")
status = st.selectbox("Status", ["Novo Lead", "Em negociação", "Fechado", "Perdido"])

if st.button("Adicionar Lead"):
    add_lead(nome, contato, status)
    st.success("Lead adicionado com sucesso!")
    st.experimental_rerun()

st.subheader("Leads Cadastrados")
leads = get_leads()

for lead in leads:
    st.write(f"📌 {lead[1]} - {lead[2]} | Status: {lead[3]}")
    novo_status = st.selectbox(f"Atualizar Status de {lead[1]}", ["Novo Lead", "Em negociação", "Fechado", "Perdido"], key=lead[0])
    if st.button(f"Atualizar {lead[1]}", key=f"update_{lead[0]}"):
        update_status(lead[0], novo_status)
        st.success("Status atualizado!")
        st.experimental_rerun()
    if st.button(f"Excluir {lead[1]}", key=f"delete_{lead[0]}"):
        delete_lead(lead[0])
        st.warning("Lead removido!")
        st.experimental_rerun()
