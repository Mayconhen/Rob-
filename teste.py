import pandas as pd

planilha_checados = pd.read_excel('contatos_checados.xlsx')
dados = []
for numeroChecados in planilha_checados['Telefone']:
    dados.append(numeroChecados)

print(dados)