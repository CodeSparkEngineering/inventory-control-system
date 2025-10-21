
import streamlit as st
from datetime import datetime

# Inicializa o estado da sessão
if 'estoque' not in st.session_state:
    st.session_state.estoque = {
        "Mouse": 0,
        "Teclado": 0,
        "Monitor": 0
    }
if 'movimentacoes' not in st.session_state:
    st.session_state.movimentacoes = []

# Título e informações do autor
st.set_page_config(page_title="Controle de Estoque", layout="wide")
st.markdown("<h1 style='text-align: center;'>📦 Sistema de Controle de Estoque</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center;'>Israel Vieira - RU 3935417</h4>", unsafe_allow_html=True)
st.markdown("---")

# Seção de cadastro de produto
st.subheader("🆕 Cadastrar Novo Produto")
with st.form("form_cadastro"):
    col1, col2 = st.columns([3, 1])
    with col1:
        novo_produto = st.text_input("Nome do novo produto")
    with col2:
        cadastrar = st.form_submit_button("Cadastrar")
    if cadastrar:
        if novo_produto:
            if novo_produto not in st.session_state.estoque:
                st.session_state.estoque[novo_produto] = 0
                st.success(f"Produto '{novo_produto}' cadastrado com sucesso!")
            else:
                st.warning("Produto já cadastrado.")
        else:
            st.error("Digite um nome válido para o produto.")

st.markdown("---")

# Seção de entrada e saída
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Entrada de Produto")
    with st.form("form_entrada"):
        produto_entrada = st.selectbox("Produto", list(st.session_state.estoque.keys()), key="entrada")
        quantidade_entrada = st.number_input("Quantidade recebida", min_value=1, step=1)
        responsavel_entrada = st.text_input("Responsável pela entrada")
        registrar_entrada = st.form_submit_button("Registrar Entrada")
        if registrar_entrada:
            st.session_state.estoque[produto_entrada] += quantidade_entrada
            data = datetime.now()
            st.session_state.movimentacoes.append((data, responsavel_entrada, produto_entrada, quantidade_entrada, "entrada"))
            st.success(f"Entrada de {quantidade_entrada} unidades de '{produto_entrada}' registrada.")

with col2:
    st.subheader("📤 Saída de Produto")
    with st.form("form_saida"):
        produto_saida = st.selectbox("Produto", list(st.session_state.estoque.keys()), key="saida")
        quantidade_saida = st.number_input("Quantidade a retirar", min_value=1, step=1)
        responsavel_saida = st.text_input("Responsável pela saída")
        registrar_saida = st.form_submit_button("Registrar Saída")
        if registrar_saida:
            if st.session_state.estoque[produto_saida] >= quantidade_saida:
                st.session_state.estoque[produto_saida] -= quantidade_saida
                data = datetime.now()
                st.session_state.movimentacoes.append((data, responsavel_saida, produto_saida, quantidade_saida, "saída"))
                st.success(f"Saída de {quantidade_saida} unidades de '{produto_saida}' registrada.")
            else:
                st.error(f"Estoque insuficiente para o produto '{produto_saida}'.")

st.markdown("---")

# Exibir estoque atual
st.subheader("📊 Estoque Atual")
if st.session_state.estoque:
    estoque_col1, estoque_col2 = st.columns(2)
    with estoque_col1:
        for nome, qtd in st.session_state.estoque.items():
            st.markdown(f"**{nome}**: {qtd} unidades")
else:
    st.info("Nenhum produto cadastrado.")

st.markdown("---")

# Exibir movimentações
st.subheader("📝 Histórico de Movimentações")
if st.session_state.movimentacoes:
    for mov in reversed(st.session_state.movimentacoes):
        data, responsavel, nome, quantidade, tipo = mov
        st.markdown(f"- `{data.strftime('%d/%m/%Y %H:%M:%S')}` | **{tipo.upper()}** | {nome} | {quantidade} unidades | Responsável: {responsavel}")
else:
    st.info("Nenhuma movimentação registrada ainda.")
