import streamlit as st
import pandas as pd

def main():
    st.title("Lojinha Unielo - Compra de Produtos por Categoria")

    # Carregar planilha e limpar nomes das colunas
    df = pd.read_excel("LOJINHA UNIELO.xlsx", sheet_name="TOTAL DE PRODUTOS")
    df.columns = df.columns.str.strip()

    # Converter colunas numéricas
    df["Preço Interno"] = pd.to_numeric(df["Preço Interno"], errors="coerce").fillna(0)
    df["Quantidade"] = pd.to_numeric(df["Quantidade"], errors="coerce").fillna(0)

    categorias_fix = [
        "HIGIENE E COSMETICOS",
        "ALIMENTICIO",
        "ELETRO",
        "PILHAS E BATERIAS",
        "LIMPEZA",
        "UTILIDADE"
    ]

    categorias = ["Todas"] + categorias_fix

    tabs = st.tabs(categorias)

    valor_total_geral = 0
    produtos_selecionados = {}

    for idx, categoria in enumerate(categorias):
        with tabs[idx]:
            st.write(f"### Produtos da categoria: {categoria}")

            if categoria == "Todas":
                df_cat = df
            else:
                df_cat = df[df["Categoria"].astype(str).str.upper() == categoria]

            if df_cat.empty:
                st.write("Nenhum produto disponível nessa categoria.")
            else:
                valor_total_categoria = 0
                for i, row in df_cat.iterrows():
                    produto = row["Produto"]
                    estoque = int(row["Quantidade"])
                    preco = row["Preço Interno"]

                    if estoque > 0:
                        col1, col2 = st.columns([4,1])
                        with col1:
                            st.markdown(f"**{produto}**  \nEstoque: *{estoque}*  \nPreço: **R$ {preco:,.2f}**")
                        with col2:
                            qtd = st.number_input(
                                "", min_value=0, max_value=estoque, value=0, key=f"qtd_{categoria}_{i}"
                            )
                        if qtd > 0:
                            valor_total_categoria += qtd * preco
                            produtos_selecionados[produto] = qtd
                    else:
                        st.markdown(f"**{produto}** - *Sem estoque disponível*")
                st.markdown(f"**Subtotal categoria {categoria}: R$ {valor_total_categoria:,.2f}**")
                valor_total_geral += valor_total_categoria

    st.markdown("---")
    st.write(f"## Valor total geral da compra: R$ {valor_total_geral:,.2f}")

    comprovante = st.file_uploader("Anexe o comprovante do PIX (obrigatório)", type=["jpg", "jpeg", "png", "pdf"])

    finalizar = st.button("Finalizar Compra", disabled=(comprovante is None))

    if finalizar:
        if valor_total_geral == 0:
            st.error("Selecione ao menos um produto com quantidade maior que zero.")
        else:
            st.success("Compra finalizada com sucesso!")
            # Aqui você pode salvar o pedido, enviar email, etc.

    st.markdown("---")
    st.caption("Sistema interno - Lojinha UnieLo")

if __name__ == "__main__":
    main()