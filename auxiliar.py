import pandas as pd
from importacoes import *
import requests

def encaminharMensagem(mensagem, numero):
    mensagemWP = f"O contato {numero}, acionou o suporte com a seguinte mensagem:\n\n"
    mensagemWP += mensagem
    enviarMensagem(mensagem=mensagemWP, numero="21992193853")

def verificarProcesso(numero):
    while True:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            for index, _ in enumerate(contatos_processo["Telefone"]):
                if str(contatos_processo["Telefone"][index]) == str(numero):
                    return contatos_processo["Processo"][index], index

def excluirProcessoUnico(numero):
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        dados = []
        for index, _ in enumerate(contatos_processo["Telefone"]):
            if str(numero) == str(contatos_processo["Telefone"][index]):
                print(index)
                dados.append(index)
        if len(dados) > 1:
            for indice in range(len(dados)):
                if indice == 0:
                    continue
                else:
                    contatos_processo = contatos_processo.drop(dados[indice])
                    contatos_processo.to_excel('contatos_processo.xlsx', index=False)
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            for index, _ in enumerate(contatos_processo["Telefone"]):
                if str(numero) == str(contatos_processo["Telefone"][index]):
                    return index
        return False
    

def excluirProcesso(imovel, numero):
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        for index, _ in enumerate(contatos_processo["Telefone"]):
            if str(numero) == str(contatos_processo["Telefone"][index]) and str(imovel) != str(contatos_processo["codImovel"][index]):
                contatos_processo = contatos_processo.drop(index)
                contatos_processo.to_excel('contatos_processo.xlsx', index=False)

def contarImoveis(numero):
        array = []
        contatos = pd.read_excel("contatos.xlsx")
        for index, contato in enumerate(contatos["Telefone"]):
            if str(contato) == numero:
                dados = {}
                dados["Código do imóvel"] = contatos["Código do imóvel"][index]
                link = str(contatos["link"][index]).split(",")
                dados["link"] = link[1]
                dados["index"] = index
                array.append(dados)
        return array

def pegarIndex(numero, indexImovel):
        imoveis = []
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        for index, _ in enumerate(contatos_processo["Telefone"]):
            dados = {}
            if str(contatos_processo["Telefone"][index]) == str(numero):
                dados["index"] = index
                dados["imovel"] = contatos_processo["codImovel"][index]
                imoveis.append(dados)
        for _ in imoveis[int(indexImovel)]:
            for indexThird, _ in enumerate(contatos_processo["Telefone"]):
                if str(imoveis[int(indexImovel)]["imovel"]) == str(contatos_processo["codImovel"][indexThird]) and str(numero == str(contatos_processo["Telefone"][indexThird])):
                    return indexThird
    

def enviarEmail(data, numero, linkImovel):
    email = 'itaimoveis7@gmail.com'
    senha = 'qrcswpxbuienlyze'

    msg= EmailMessage()
    msg['Subject'] = 'Agendamento feito'
    msg['From'] = 'itaimoveis7@gmail.com'
    msg['To'] = 'itaimoveis7@gmail.com'
    mensagem_html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                width: 100%;
                height: 100%;
            }}
            .container {{
                padding: 20px;
                background-color: #fff;
                border-radius: 5px;
                box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
                width: 60%;
                height: 60%;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Agendamento feito</h1>
            <p>Olá, Gostaria de compartilhar uma ótima notícia! Um novo horário foi agendado com sucesso através do nosso robô de WhatsApp. Abaixo estão os detalhes do agendamento:</p>
            <ul>
                <li>Data e Horário: {data}</li>
                <li>Contato do Cliente: {numero}</li>
                <li>Link do imóvel: {linkImovel}</li>
            </ul>
            <p>Atenciosamente,<br>Robô Ita Imóveis</p>
        </div>
    </body>
    </html>
    """

    msg.add_alternative(mensagem_html, subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email, senha)
        smtp.send_message(msg)

def tratarData(data):
    dataFormatada = f"{data[8:10]}/{data[5:7]}/{data[0:4]} às {data[11:16]}\n"
    return dataFormatada

def tratarDatas(datas):
    datasFormatadas = ""
    for data in datas:
        dataFormatada = f"*{data[0]}* - {data[1][8:10]}/{data[1][5:7]}/{data[1][0:4]} às {data[1][11:16]}\n"
        datasFormatadas += dataFormatada
    return datasFormatadas

def gerenciarProcesso(processo, mensagem, numero, index, datas=None, quantidade=False, multiplos=True, reagendamento=False, erroAgendamento=False):
    match processo:
        case 1:

            print("Entrei no um")
            mensagem = f"Olá, tudo bem? verificamos que você buscou um imóvel no nosso ZAP imóveis.\nDeseja realizar uma visita?\n1 - Sim\n2 - Não"
            enviarMensagem(mensagem=mensagem, numero=str(numero))
            atualizarPlanilha(processo=2, index=index)

        case 2:
            print("Entrei no dois")
            if reagendamento == True or erroAgendamento != False:
                mensagem = "1" 
            if str(mensagem) == "1":
                imoveis = contarImoveis(numero)
                if len(imoveis) == 1 and erroAgendamento != False:
                    gerenciarProcesso(processo=3, numero=numero, index=index, mensagem=mensagem, multiplos=False)
                else:
                    enviarMensagem(mensagem="Pra qual imóvel você deseja agendar?\nAguarde trazendo os imóveis...\n", numero=numero)
                    for indexImov, imovel in enumerate(imoveis):
                        mensagemImovel = f"{imovel['link']}\n\n{indexImov} - {imovel['Código do imóvel']}\n"
                        if indexImov + 1 < len(imoveis):
                            mensagemImovel += f"Aguarde trazendo os imóveis...\n"
                        else:
                            mensagemImovel += f"Todos os imóveis disponíveis acima!\n"
                        enviarMensagem(mensagem=mensagemImovel, numero=numero)
                        atualizarPlanilha(processo=3, index=index)
            elif str(mensagem) == "2":
                indexUnico = excluirProcessoUnico(numero)
                atualizarPlanilha(processo=7, index=index if indexUnico == False else indexUnico)
                gerenciarProcesso(processo=7, numero=numero, index=index if indexUnico == False else indexUnico, mensagem=mensagem)
            else:
                enviarMensagem(mensagem="Opção inválida! Por favor escolha uma das opções acima.\n", numero=numero)

        case 3:

            print("Entrei no três")
            if multiplos == True:
                try:
                    indexImovel = pegarIndex(numero, mensagem)
                except Exception as e:
                    print(e)
                    print("ERRO CONTROLADO 3 PRIMEIRA EXCEPTION")
                    enviarMensagem(mensagem="Opção inválida! Por favor escolha uma das opções acima.\n", numero=numero)
                    return None
            codImovel = pegarDados(codImovel=True, index=indexImovel if multiplos == True else index)
            try:
                objeto_retorna_data = RetornarData()
                print(codImovel)
                datas = objeto_retorna_data.retornar_datas(codigo_imovel=codImovel)
                tamanhoData = len(datas)
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO 3 SEGUNDA EXCEPTION")
                enviarMensagem(mensagem=f"Sem datas disponiveis pro imóvel {codImovel}\nPor favor, tente outro dia!", numero=numero)
                atualizarPlanilha(processo=1, index=index)
                return None
            datasWP = tratarDatas(datas)
            mensagemWP = f"Escolha uma das datas abaixo!\nEscolha o número em negrito para selecionar a data\n\n"
            mensagemWP += datasWP
            enviarMensagem(mensagem=mensagemWP, numero=numero)
            excluirProcesso(codImovel, numero)
            inserirPlanilha(quantidade=tamanhoData, index=index)
            atualizarPlanilha(processo=4, index=index)

        case 4:

            print("Entrei no quatro")
            codImovel = str(pegarDados(codImovel=True, index=index, numero=numero))
            try:
                objeto_retorna_data = RetornarData()
                datas = objeto_retorna_data.retornar_datas(codigo_imovel=codImovel)
                quantidade = int(pegarDados(index=index, quantidade=quantidade, numero=numero))
                if len(datas) != quantidade:
                    enviarMensagem(mensagem="Peço perdão, mas houve alterações na lista de datas!\n", numero=numero)
                    atualizarPlanilha(processo=3, index=index)
                    gerenciarProcesso(processo=3, numero=numero, mensagem=mensagem, index=index, erroAgendamento=True)
                    return None
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO 4 PRIMEIRA EXCEPTION")
                enviarMensagem(mensagem="Peço perdão, mas houve alterações na lista de datas!\n", numero=numero)
                enviarMensagem(mensagem=f"Sem datas disponiveis pro imóvel {codImovel}\nPor favor, tente outro dia!", numero=numero)
                atualizarPlanilha(processo=1, index=index)
                return None
            try:
                dataEmail = f"{(datas[int(mensagem)][1])[8:10]}/{(datas[int(mensagem)][1])[5:7]}/{(datas[int(mensagem)][1])[0:4]} às {(datas[int(mensagem)][1])[11:16]}"
                data = f"{str((datas[int(mensagem)][1])[0:9])} {str((datas[int(mensagem)][1])[11:16])}"
                inserirPlanilha(data=data, index=index)
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO 4 SEGUNDA EXCEPTION")
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)
                return None
            try:
                objeto_retorna_data.retornar_datas(opcao=int(mensagem), enviar=True, codigo_imovel=codImovel, numero=numero)
            except Exception as e:
                print(e)
                print("ERRO CONTROLADO TERCEIRA EXCEPTION")
                enviarMensagem(mensagem="Opção inválida! Por favor escolha uma das datas acima.\n", numero=numero)
                return None
            enviarMensagem(mensagem="Data confirmada!\nAtendimento encerrado!", numero=numero)
            linkImovel = pegarDados(linkImovel=True, index=index)
            enviarEmail(dataEmail, numero, linkImovel)
            atualizarPlanilha(processo=5, index=index)

        case 5:

            codImovel = pegarDados(codImovel=True, index=index, numero=numero)
            if str(mensagem) == "1":
                inserirPlanilha(confirmado=True, index=index)
                enviarMensagem(mensagem=f'O contato {numero} confirmou a presença no imóvel: {codImovel}', numero="21966652864")
                enviarMensagem(mensagem=f'Presença confirmada! :)', numero=numero)
            elif str(mensagem) == "2":
                inserirPlanilha(confirmado=False, index=index)
                enviarMensagem(mensagem=f'Deseja remarcar a visitação?\n1 - Sim\n2 - Não', numero=numero)
                atualizarPlanilha(processo=6, index=index)
            else:
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)
           
        case 6:

   
            codImovel = pegarDados(codImovel=True, index=index, numero=numero)
            if str(mensagem) == "1":
                objeto_excluir_data = excluiragendamento()
                objeto_excluir_data.removeragendamento(numero=numero, codigo_imovel=codImovel)
                inserirPlanilha(confirmado=True, index=index)
                enviarMensagem(mensagem=f'O contato {numero} reagendou a presença no imóvel: {codImovel}', numero="21992193853")
                atualizarPlanilha(processo=2, index=index)
                gerenciarProcesso(processo=2, numero=numero, mensagem=mensagem, index=index, reagendamento=True)
            elif str(mensagem) == "2":
                objeto_excluir_data = excluiragendamento()
                objeto_excluir_data.removeragendamento(numero=numero, codigo_imovel=codImovel)
                inserirPlanilha(confirmado=False, index=index)
                enviarMensagem(mensagem=f'O contato {numero} cancelou a presença no imóvel: {codImovel}', numero="21992193853")
                atualizarPlanilha(processo=9, index=index)
            else:
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)

                
        case 7:

            enviarMensagem(mensagem="Deseja deixar uma mensagem para o suporte?\n1 - Sim\n2 - Não", numero=numero)
            atualizarPlanilha(processo=8, index=index)

            
        case 8:
                
            if str(mensagem) == "1":
                inserirPlanilha(suporte=True, index=index)
                atualizarPlanilha(processo=9, index=index)
                enviarMensagem(mensagem="Obrigado pelo contato! ;)\nBasta digitar sua duvida e um atendente vai te responder!", numero=numero)
            elif str(mensagem) == "2":
                enviarMensagem(mensagem="Obrigado pelo contato! ;)", numero=numero)
                atualizarPlanilha(processo=9, index=index)
            else:
                enviarMensagem(mensagem=f'Opção inválida! Por favor, escolha uma das opções acima.', numero=numero)

        case 9:
            
            x = pegarDados(suporte=True, index=index, numero=numero)
            if x == True:
                encaminharMensagem(mensagem, numero)
            else:
                gerenciarProcesso(processo=1, numero=numero, mensagem=mensagem, index=index)



def enviarMensagem(mensagem, numero):
    url = "https://v5.chatpro.com.br/chatpro-d0b7106b49/api/v1/send_message"
    payload = {
    "number": numero,
    "message": mensagem
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "bae32d2b04cd8a37a2e9bf70d458ffa0"
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def atualizarPlanilha(processo, index):
    
        print("Atualizar")
        contatos_processo = pd.read_excel("contatos_processo.xlsx")
        contatos_processo.at[index, "Processo"] = processo
        contatos_processo.to_excel('contatos_processo.xlsx', index=False)


def inserirPlanilha(data=None, index=None, quantidade=None, confirmado=None, codImovel=None, linkImovel=None, suporte=None, notifica=None, notificado=None):

   
        print("INSERIR PLANILHA")
        if data != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "Data"] = data
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)

        if quantidade != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "Quantidade"] = quantidade
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)

        if confirmado != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "Confirmado"] = confirmado
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)

        if codImovel != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "codImovel"] = codImovel
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)

        if linkImovel != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "linkImovel"] = linkImovel
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)

        if suporte != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "suporte"] = suporte
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)
        
        if notifica != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "notifica"] = notifica
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)

        if notificado != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            contatos_processo.at[index, "notificado"] = notificado
            contatos_processo.to_excel('contatos_processo.xlsx', index=False)


def pegarDados(data=None, index=None, quantidade=None, confirmado=None, codImovel=None, linkImovel=None, suporte=None, notifica=None, notificado=None, numero=None):
        if data != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "Data"]

        if quantidade != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "Quantidade"]
            
        if confirmado != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "Confirmado"]
        
        if codImovel != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "codImovel"]
        
        if linkImovel != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "linkImovel"]
        
        if suporte != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "suporte"]
        
        if notifica != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "notifica"]
        
        if notificado != None:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            return contatos_processo.at[index, "notificado"]


def integrarPlanilhas():
    try:
        dadosArray = []
        contatos_checados = pd.read_excel("contatos_checados.xlsx")
        try:
            contatos_processo = pd.read_excel("contatos_processo.xlsx")
            for indexProcesso, _ in enumerate(contatos_processo["Telefone"]):
                dadosProcesso = {
                    'Telefone': contatos_processo["Telefone"][indexProcesso],
                    'Processo': contatos_processo["Processo"][indexProcesso],
                    'Data': contatos_processo["Data"][indexProcesso],
                    'Confirmado': contatos_processo["Confirmado"][indexProcesso],
                    'Quantidade': contatos_processo["Quantidade"][indexProcesso],
                    'codImovel': contatos_processo["codImovel"][indexProcesso],
                    'linkImovel': contatos_processo["linkImovel"][indexProcesso],
                    'suporte': contatos_processo["suporte"][indexProcesso],
                    'notifica': contatos_processo["notifica"][indexProcesso],
                    'notificado': contatos_processo["notificado"][indexProcesso]
                }
                dadosArray.append(dadosProcesso)
        except Exception as e:
            dados = {
                    'Telefone': "0",
                    'Processo': "0",
                    'Data': "Não",
                    'Confirmado': "Não",
                    'Quantidade': "0",
                    'codImovel': "Não",
                    'linkImovel': "Não",
                    'suporte': "Não",
                    'notifica': "Não",
                    'notificado': "Não"
                }

            dadosArray.append(dados)

            plan = pd.DataFrame(dadosArray)

            plan.to_excel("contatos_processo.xlsx", index=False)

            contatos_processo = pd.read_excel("contatos_processo.xlsx")

        for index, item in enumerate(contatos_checados["Telefone"]):
            if item == 1:
                continue
            if item not in [i for i in contatos_processo["Telefone"]]:
                dados = {
                    'Telefone': item,
                    'Processo': 2,
                    'Data': "Não",
                    'Confirmado': "Não",
                    'Quantidade': "0",
                    'codImovel': contatos_checados['Código do imóvel'][index],
                    'linkImovel': contatos_checados['link'][index],
                    'suporte': "Não",
                    'notifica': "Não",
                    'notificado': "Não"
                }

                dadosArray.append(dados)

        if len(dadosArray) > 0:
            plan = pd.DataFrame(dadosArray)

            plan.to_excel("contatos_processo.xlsx", index=False)

    except Exception as e:
        print(e)
        print("ERRO CONTROLADO")
        time.sleep(2)
        integrarPlanilhas()
    

def mensagemRecebida(json):
    dados = json
    if dados["Type"] == "receveid_message":
        mensagem = dados["Body"]["Text"]
        numero = (dados["Body"]["Info"]["RemoteJid"])[2:13]
        processoIndex = verificarProcesso(numero)
        gerenciarProcesso(processo=processoIndex[0], mensagem=mensagem, numero=numero, index=processoIndex[1]) if processoIndex != None else None
        
        

