import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

# ====================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================
st.set_page_config(
    page_title="Sistema de Vendas",
    page_icon="👩‍❤️‍👨",
    layout="wide"
)

# ====================================
# ARQUIVO CSV
# ====================================
ARQUIVO = "vendas.csv"

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
# CRIA CSV SE NÃO EXISTIR
# ====================================
if not Path(ARQUIVO).exists():
    pd.DataFrame(columns=colunas).to_csv(ARQUIVO, index=False)

# ====================================
# CARREGA DADOS
# ====================================
df = pd.read_csv(ARQUIVO)

# ====================================
# TÍTULO
# ====================================
st.title("👩‍❤️‍👨 Vendas ECC 2026")

st.markdown("---")

# ====================================
# ABAS
# ====================================
aba1, aba2 = st.tabs([
    "🧾 Venda para Casal",
    "💵 Pagamento na Hora"
])

# ====================================
# ABA 1 - VENDA PARA CASAL
# ====================================
with aba1:

    st.subheader("Venda para Casal")

    with st.form("form_casal"):

        col1, col2 = st.columns(2)

        with col1:

            produto = st.text_input(
                "Nome do Produto"
            )

            valor_unitario = st.number_input(
                "Valor Unitário",
                min_value=0.0,
                step=0.5,
                format="%.2f"
            )

        with col2:

            quantidade = st.number_input(
                "Quantidade",
                min_value=1,
                step=1
            )

            casal = st.text_input(
                "Nome do Casal"
            )

            equipe = st.text_input(
                "Equipe do Casal"
            )

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
                not produto.strip()
                or valor_unitario <= 0
                or quantidade <= 0
                or not casal.strip()
                or not equipe.strip()
            ):

                st.error(
                    "Preencha todos os campos corretamente!"
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

# ====================================
# ABA 2 - PAGAMENTO NA HORA
# ====================================
with aba2:

    st.subheader("Pagamento na Hora")

    with st.form("form_pagamento"):

        col1, col2 = st.columns(2)

        with col1:

            produto_pg = st.text_input(
                "Produto"
            )

            valor_unitario_pg = st.number_input(
                "Valor Unitário ",
                min_value=0.0,
                step=0.5,
                format="%.2f"
            )

        with col2:

            quantidade_pg = st.number_input(
                "Quantidade ",
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

        # ====================================
        # VALIDAÇÃO
        # ====================================
        if salvar_pg:

            if (
                not produto_pg.strip()
                or valor_unitario_pg <= 0
                or quantidade_pg <= 0
            ):

                st.error(
                    "Preencha todos os campos corretamente!"
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
                    "Pagamento salvo com sucesso!"
                )

# ====================================
# RESUMO GERAL
# ====================================
st.markdown("---")

st.subheader("📊 Resumo Geral")

if not df.empty:

    # TOTAL A RECEBER
    total_geral = (
        df[
            df["Status"] == "Pendente"
        ]["Valor Total"].sum()
    )

    # TOTAL FIADO
    total_fiado = (
        df[
            (df["Tipo"] == "Fiado") &
            (df["Status"] == "Pendente")
        ]["Valor Total"].sum()
    )

    # TOTAL PAGO NA HORA
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
# HISTÓRICO DE VENDAS
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

        # SOMENTE PENDENTES
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

        # ====================================
        # BAIXA DE PAGAMENTO
        # ====================================
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
                    "Pagamento baixado com sucesso!"
                )

                st.rerun()

    else:

        st.warning(
            "Nenhuma compra encontrada."
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

# ====================================
# EXCLUIR VENDA COM SENHA
# ====================================
st.markdown("---")

st.subheader("🗑️ Excluir Venda")

SENHA_EXCLUSAO = "2026"

if not df.empty:

    venda_selecionada = st.selectbox(
        "Selecione a venda para excluir",
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

            df = df.drop(venda_selecionada)

            df.to_csv(
                ARQUIVO,
                index=False
            )

            st.success(
                "Venda excluída com sucesso!"
            )

            st.rerun()

        else:

            st.error("Senha incorreta!")

else:

    st.info("Nenhuma venda cadastrada.")