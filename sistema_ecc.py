import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ====================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================
st.set_page_config(
    page_title="Sistema de Vendas",
    page_icon="💍",
    layout="wide"
)

# ====================================
# ARQUIVOS
# ====================================
ARQUIVO = "vendas.csv"
ARQUIVO_PRODUTOS = "produtos.csv"
ARQUIVO_CASAIS = "casais.csv"

# ====================================
# COLUNAS
# ====================================
colunas = [
    "Data",
    "Tipo",
    "Produto",
    "Valor Unitario",
    "Quantidade",
    "Valor Total",
    "Casal",
    "Equipe",
    "Status"
]

# ====================================
# CRIAR CSV VENDAS
# ====================================
if not Path(ARQUIVO).exists():

    pd.DataFrame(
        columns=colunas
    ).to_csv(
        ARQUIVO,
        index=False
    )

# ====================================
# CRIAR CSV PRODUTOS
# ====================================
if not Path(ARQUIVO_PRODUTOS).exists():

    pd.DataFrame(
        columns=["Produto", "Valor"]
    ).to_csv(
        ARQUIVO_PRODUTOS,
        index=False
    )

# ====================================
# CRIAR CSV CASAIS
# ====================================
if not Path(ARQUIVO_CASAIS).exists():

    pd.DataFrame(
        columns=["Casal", "Equipe"]
    ).to_csv(
        ARQUIVO_CASAIS,
        index=False
    )

# ====================================
# CARREGAR DADOS
# ====================================
df = pd.read_csv(ARQUIVO)

df_produtos = pd.read_csv(
    ARQUIVO_PRODUTOS
)

df_casais = pd.read_csv(
    ARQUIVO_CASAIS
)

# ====================================
# TÍTULO
# ====================================
st.title("💍 Vendas ECC 2026")

st.markdown("---")

# ====================================
# ABAS
# ====================================
aba1, aba2, aba3, aba4 = st.tabs([
    "🧾 Venda para Casal",
    "💵 Pagamento na Hora",
    "📦 Cadastro de Produtos",
    "👩‍❤️‍👨 Cadastro de Casais"
])

# ====================================
# ABA 1 - VENDA PARA CASAL
# ====================================
with aba1:

    st.subheader("🧾 Venda para Casal")

    with st.form("form_venda_casal"):

        col1, col2 = st.columns(2)

        # ====================================
        # PRODUTOS
        # ====================================
        lista_produtos = (
            df_produtos["Produto"]
            .dropna()
            .tolist()
        )

        produto = st.selectbox(
            "Selecione o Produto",
            options=[""] + lista_produtos
        )

        valor_unitario = 0.0

        if produto != "":

            valor_unitario = float(
                df_produtos[
                    df_produtos["Produto"] == produto
                ]["Valor"].values[0]
            )

        with col1:

            st.text_input(
                "Valor Unitário",
                value=f"R$ {valor_unitario:.2f}",
                disabled=True
            )

        with col2:

            quantidade = st.number_input(
                "Quantidade",
                min_value=1,
                step=1
            )

        # ====================================
        # CASAIS
        # ====================================
        lista_casais = (
            df_casais["Casal"]
            .dropna()
            .tolist()
        )

        casal = st.selectbox(
            "Selecione o Casal",
            options=[""] + lista_casais
        )

        equipe = ""

        if casal != "":

            equipe = (
                df_casais[
                    df_casais["Casal"] == casal
                ]["Equipe"]
                .values[0]
            )

        st.text_input(
            "Equipe",
            value=equipe,
            disabled=True
        )

        # ====================================
        # TOTAL
        # ====================================
        valor_total = (
            valor_unitario * quantidade
        )

        st.info(
            f"Valor Total: R$ {valor_total:.2f}"
        )

        salvar = st.form_submit_button(
            "Salvar Venda"
        )

        # ====================================
        # VALIDAÇÃO
        # ====================================
        if salvar:

            if (
                produto == ""
                or casal == ""
                or quantidade <= 0
            ):

                st.error(
                    "Preencha todos os campos!"
                )

            else:

                nova_venda = {
                    "Data": datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                    "Tipo": "Fiado",
                    "Produto": produto,
                    "Valor Unitario": valor_unitario,
                    "Quantidade": quantidade,
                    "Valor Total": valor_total,
                    "Casal": casal,
                    "Equipe": equipe,
                    "Status": "Pendente"
                }

                df = pd.concat(
                    [
                        df,
                        pd.DataFrame([nova_venda])
                    ],
                    ignore_index=True
                )

                df.to_csv(
                    ARQUIVO,
                    index=False
                )

                st.success(
                    "Venda salva com sucesso!"
                )

                st.rerun()

# ====================================
# ABA 2 - PAGAMENTO NA HORA
# ====================================
with aba2:

    st.subheader("💵 Pagamento na Hora")

    with st.form("form_pagamento"):

        col1, col2 = st.columns(2)

        # ====================================
        # PRODUTOS
        # ====================================
        lista_produtos_pg = (
            df_produtos["Produto"]
            .dropna()
            .tolist()
        )

        produto_pg = st.selectbox(
            "Selecione o Produto",
            options=[""] + lista_produtos_pg
        )

        valor_unitario_pg = 0.0

        if produto_pg != "":

            valor_unitario_pg = float(
                df_produtos[
                    df_produtos["Produto"] == produto_pg
                ]["Valor"].values[0]
            )

        with col1:

            st.text_input(
                "Valor Unitário",
                value=f"R$ {valor_unitario_pg:.2f}",
                disabled=True
            )

        with col2:

            quantidade_pg = st.number_input(
                "Quantidade",
                min_value=1,
                step=1
            )

        valor_total_pg = (
            valor_unitario_pg * quantidade_pg
        )

        st.info(
            f"Valor Total: R$ {valor_total_pg:.2f}"
        )

        salvar_pg = st.form_submit_button(
            "Salvar Pagamento"
        )

        if salvar_pg:

            if (
                produto_pg == ""
                or quantidade_pg <= 0
            ):

                st.error(
                    "Preencha todos os campos!"
                )

            else:

                nova_venda = {
                    "Data": datetime.now().strftime(
                        "%d/%m/%Y %H:%M"
                    ),
                    "Tipo": "Pago na Hora",
                    "Produto": produto_pg,
                    "Valor Unitario": valor_unitario_pg,
                    "Quantidade": quantidade_pg,
                    "Valor Total": valor_total_pg,
                    "Casal": "",
                    "Equipe": "",
                    "Status": "Pago"
                }

                df = pd.concat(
                    [
                        df,
                        pd.DataFrame([nova_venda])
                    ],
                    ignore_index=True
                )

                df.to_csv(
                    ARQUIVO,
                    index=False
                )

                st.success(
                    "Pagamento salvo!"
                )

                st.rerun()

# ====================================
# ABA 3 - CADASTRO PRODUTOS
# ====================================
with aba3:

    st.subheader("📦 Cadastro de Produtos")

    with st.form("form_produto"):

        nome_produto = st.text_input(
            "Nome do Produto"
        )

        valor_produto = st.number_input(
            "Valor do Produto",
            min_value=0.0,
            step=0.5,
            format="%.2f"
        )

        salvar_produto = st.form_submit_button(
            "Salvar Produto"
        )

        if salvar_produto:

            if (
                not nome_produto.strip()
                or valor_produto <= 0
            ):

                st.error(
                    "Preencha todos os campos!"
                )

            else:

                novo_produto = {
                    "Produto": nome_produto,
                    "Valor": valor_produto
                }

                df_produtos = pd.concat(
                    [
                        df_produtos,
                        pd.DataFrame([novo_produto])
                    ],
                    ignore_index=True
                )

                df_produtos.to_csv(
                    ARQUIVO_PRODUTOS,
                    index=False
                )

                st.success(
                    "Produto cadastrado!"
                )

                st.rerun()

    st.dataframe(
        df_produtos,
        width="stretch"
    )

# ====================================
# ABA 4 - CADASTRO CASAIS
# ====================================
with aba4:

    st.subheader(
        "👩‍❤️‍👨 Cadastro de Casais"
    )

    with st.form("form_casal_cadastro"):

        nome_casal = st.text_input(
            "Nome do Casal"
        )

        equipe_casal = st.text_input(
            "Equipe"
        )

        salvar_casal = st.form_submit_button(
            "Salvar Casal"
        )

        if salvar_casal:

            if (
                not nome_casal.strip()
                or not equipe_casal.strip()
            ):

                st.error(
                    "Preencha todos os campos!"
                )

            else:

                novo_casal = {
                    "Casal": nome_casal,
                    "Equipe": equipe_casal
                }

                df_casais = pd.concat(
                    [
                        df_casais,
                        pd.DataFrame([novo_casal])
                    ],
                    ignore_index=True
                )

                df_casais.to_csv(
                    ARQUIVO_CASAIS,
                    index=False
                )

                st.success(
                    "Casal cadastrado!"
                )

                st.rerun()

    st.dataframe(
        df_casais,
        width="stretch"
    )

# ====================================
# RESUMO GERAL
# ====================================
st.markdown("---")

st.subheader("📊 Resumo Geral")

if not df.empty:

    total_geral = (
        df[
            df["Status"] == "Pendente"
        ]["Valor Total"].sum()
    )

    total_fiado = (
        df[
            (df["Tipo"] == "Fiado") &
            (df["Status"] == "Pendente")
        ]["Valor Total"].sum()
    )

    total_pago = (
        df[
            df["Tipo"] == "Pago na Hora"
        ]["Valor Total"].sum()
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total a Receber",
        f"R$ {total_geral:.2f}"
    )

    col2.metric(
        "🧾 Total Fiado",
        f"R$ {total_fiado:.2f}"
    )

    col3.metric(
        "💵 Pago na Hora",
        f"R$ {total_pago:.2f}"
    )

else:

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💰 Total a Receber",
        "R$ 0,00"
    )

    col2.metric(
        "🧾 Total Fiado",
        "R$ 0,00"
    )

    col3.metric(
        "💵 Pago na Hora",
        "R$ 0,00"
    )

# ====================================
# HISTÓRICO
# ====================================
st.markdown("---")

st.subheader("📋 Histórico de Vendas")

if not df.empty:

    st.dataframe(
        df,
        width="stretch"
    )

else:

    st.warning(
        "Nenhuma venda cadastrada."
    )

# ====================================
# CONSULTA POR CASAL
# ====================================
st.markdown("---")

st.subheader("🔎 Consulta por Casal")

pesquisa = st.text_input(
    "Digite o nome do casal"
)

if pesquisa:

    resultado = df[
        df["Casal"]
        .astype(str)
        .str.contains(
            pesquisa,
            case=False,
            na=False
        )
    ]

    if not resultado.empty:

        pendentes = resultado[
            resultado["Status"] == "Pendente"
        ]

        total_pendente = (
            pendentes["Valor Total"]
            .sum()
        )

        st.info(
            f"Total pendente: R$ {total_pendente:.2f}"
        )

        st.dataframe(
            resultado,
            width="stretch"
        )

        if total_pendente > 0:

            if st.button(
                "✅ Dar baixa no pagamento"
            ):

                df.loc[
                    df["Casal"]
                    .astype(str)
                    .str.contains(
                        pesquisa,
                        case=False,
                        na=False
                    ),
                    "Status"
                ] = "Pago"

                df.to_csv(
                    ARQUIVO,
                    index=False
                )

                st.success(
                    "Pagamento baixado!"
                )

                st.rerun()

    else:

        st.warning(
            "Nenhuma compra encontrada."
        )

# ====================================
# EXCLUIR VENDA
# ====================================
st.markdown("---")

st.subheader("🗑️ Excluir Venda")

SENHA_EXCLUSAO = "1234"

if not df.empty:

    venda_selecionada = st.selectbox(
        "Selecione a venda",
        df.index,
        format_func=lambda x:
            f"{df.loc[x, 'Data']} | "
            f"{df.loc[x, 'Produto']} | "
            f"{df.loc[x, 'Casal']} | "
            f"R$ {df.loc[x, 'Valor Total']:.2f}"
    )

    senha = st.text_input(
        "Digite a senha",
        type="password"
    )

    if st.button("Excluir Venda"):

        if senha == SENHA_EXCLUSAO:

            df = df.drop(
                venda_selecionada
            )

            df.to_csv(
                ARQUIVO,
                index=False
            )

            st.success(
                "Venda excluída!"
            )

            st.rerun()

        else:

            st.error(
                "Senha incorreta!"
            )

else:

    st.info(
        "Nenhuma venda cadastrada."
    )

# ====================================
# EXPORTAR CSV
# ====================================
st.markdown("---")

st.download_button(
    label="📥 Baixar Relatório CSV",
    data=df.to_csv(index=False).encode(
        "utf-8"
    ),
    file_name="relatorio_vendas.csv",
    mime="text/csv"
)