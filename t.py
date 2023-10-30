import pandas as pd
from datetime import datetime, timedelta
import app
import time

def excluirProcessoUnico(numero):
    try:
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        dados = []
        for index, _ in enumerate(contatos_processo["Telefone"]):
            if str(numero) == str(contatos_processo["Telefone"][index]):
                print(index)
                print("ADICIONANDO NO ARRAY")
                dados.append(index)
        if len(dados) > 1:
            for indice in range(len(dados)):
                print(indice)
                print(dados[indice])
                if indice == 0:
                    continue
                else:
                    print("Excluido")
                    contatos_processo = contatos_processo.drop(dados[indice])
                    contatos_processo.to_excel('contatos_processo.xlsx', index=False)
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            for index, _ in enumerate(contatos_processo["Telefone"]):
                if str(numero) == str(contatos_processo["Telefone"][index]):
                    return index
        return False
    except Exception as e:
        print(e)
        print("ERRO CONTROLADO")
        time.sleep(2)
        excluirProcessoUnico(numero)

app.integrarPlanilhas()
excluirProcessoUnico("21992193853")