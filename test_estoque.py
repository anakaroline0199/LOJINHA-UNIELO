import pandas as pd

arquivo_excel = 'LOJINHA UNIELO.xlsx'
nome_aba = 'total de produtos'

df = pd.read_excel(arquivo_excel, sheet_name=nome_aba)

print("Testando leitura da planilha:")
print(df)