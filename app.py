from flask import Flask, request
import threading
from importacoes import *
import auxiliar
import schedule
from datetime import datetime, timedelta
import pandas as pd

app = Flask(__name__)

#DESENVOLVENDO WEBHOOK#

# def arquivo_em_uso(nome_arquivo):
#     for processo in psutil.process_iter(['pid', 'open_files']):
#         try:
#             arquivos_abertos = processo.info['open_files']
#             for arquivo in arquivos_abertos:
#                 if arquivo.path == nome_arquivo:
#                     return True
#         except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#             pass
#     return False

def enviarNotificacao():
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    now = datetime.strptime(now, "%Y-%m-%d %H:%M")

    doisDias = now + timedelta(days=2)
    umDia = now + timedelta(days=1)
    umaHora = now + timedelta(hours=1)
    meiaHora = now + timedelta(minutes=30)
    contatos_processo = pd.read_excel("contatos_processo.xlsx")

    for index, data in enumerate(contatos_processo["Data"]):
        
        notificar = False
        processoNotificacao = 0
        codMovel = contatos_processo["codImovel"][index]
        try:
            data = datetime.strptime(data, "%Y-%m-%d %H:%M")
        except Exception as e:
            # print(e)
            # print("ERRO CONTROLADO")
            continue

        if doisDias >= data or umDia >= data or umaHora >= data or meiaHora >= data:
            notificar = True

        if doisDias >= data:
            processoNotificacao = 1
        if umDia >= data:
            processoNotificacao = 2
        if umaHora >= data:
            processoNotificacao = 3
        if meiaHora >= data:
            processoNotificacao = 4

        if notificar == True:
            data = auxiliar.tratarData(data.strftime("%Y-%m-%d %H:%M:%S"))
            time.sleep(1)
            notificaGet = auxiliar.pegarDados(notifica=True, index=index)
            print(notificaGet)
            notificacaoGet = auxiliar.pegarDados(notifica=True, index=index)
            print(notificacaoGet)
            match processoNotificacao:
                case 1:
                    if notificacaoGet == 'Não':
                        auxiliar.inserirPlanilha(notifica="1", index=index)
                        auxiliar.inserirPlanilha(notificado="Sim", index=index)
                        auxiliar.enviarMensagem(mensagem=f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', numero=int(contatos_processo["Telefone"][index]))
                case 2:
                    if notificacaoGet == 'Não' or int(notificaGet) > 2:
                        auxiliar.inserirPlanilha(notifica="2", index=index)
                        auxiliar.inserirPlanilha(notificado="Sim", index=index)
                        auxiliar.enviarMensagem(mensagem=f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', numero=str(contatos_processo["Telefone"][index]))
                case 3:
                    if notificacaoGet == 'Não' or int(notificaGet) > 3:
                        auxiliar.inserirPlanilha(notifica="3", index=index)
                        auxiliar.inserirPlanilha(notificado="Sim", index=index)
                        auxiliar.enviarMensagem(mensagem=f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', numero=str(contatos_processo["Telefone"][index]))
                case 4:
                    if notificacaoGet == 'Não' or int(notificaGet) > 3:
                        auxiliar.inserirPlanilha(notifica="4", index=index)
                        auxiliar.inserirPlanilha(notificado="Sim", index=index)
                        auxiliar.enviarMensagem(mensagem=f'Você confirma a visitação ao imóvel: {codMovel} no dia {data}?\n1 - Sim\n2 - Não', numero=str(contatos_processo["Telefone"][index]))


def exportarContatos():
    objeto_exportar = exportar()
    objeto_exportar.exportacao_contatos()
    objeto_enviaremail = automatizar_email()
    objeto_enviaremail.enviar_email()

def integrarPlanilhas():
    objeto_automacao_planilha = planilhauto()
    objeto_automacao_planilha.automacao_planilha()
    auxiliar.integrarPlanilhas()
    
def verificarProcessos():
    while True:
        schedule.run_pending()
        time.sleep(10)

def iniciarServer():
    app.run(port=80)


lock = threading.Lock()

@app.route("/chat", methods=['POST'])
def chat():
    try:
        verifica = request.json
        if verifica["Type"] == "receveid_message":
            numero = (verifica["Body"]["Info"]["RemoteJid"])[2:13]
            processoIndex = auxiliar.verificarProcesso(numero)
            if processoIndex != None:
                with lock:
                    thread = threading.Thread(target=auxiliar.mensagemRecebida, args=(request.json,))
                    thread.daemon = True
                    thread.start()
    except Exception as e:
        return "Não interessa"
    return "Concluído"


@app.route("/", methods=['POST'])
def index():
    return "ROBO EM FUNCIONAMENTO"

if __name__ == "__main__":
    # schedule.every(60).minutes.do(exportarContatos)
    # schedule.every(70).minutes.do(integrarPlanilhas)
    # schedule.every(1).minute.do(enviarNotificacao)
    # with lock:
    #     y = threading.Thread(target=verificarProcessos)
    #     y.start()
    # exportarContatos()
    integrarPlanilhas()
    enviarNotificacao()
    iniciarServer()
    