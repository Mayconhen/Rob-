from importacoes import * 

class excluiragendamento:  
    def removeragendamento(self, numero=None, codigo_imovel=None):
        SCOPES = ['https://www.googleapis.com/auth/calendar', 'https://www.googleapis.com/auth/calendar.events']
        SERVICE_ACCOUNT_FILE = 'credentials.json'
        from collections import defaultdict
        credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

        # Crie um objeto de serviço do Google Calendar
        service = build('calendar', 'v3', credentials=credentials)

        # Defina o ID da agenda
        calendar_id = 'itaimoveis7@gmail.com'

        now = datetime.datetime.utcnow()
        start_date = now.date()  # Data de hoje
        end_date = start_date + datetime.timedelta(days=60)  # Data daqui a um ano

        ## Listando eventos que possuem 'Agendado' na descrição
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_date.isoformat() + 'T00:00:00Z',
            timeMax=end_date.isoformat() + 'T23:59:59Z',
            singleEvents=True,
            orderBy='startTime',
            q=f'Agendado,{numero},{codigo_imovel}'  # Filtro para eventos com a descrição "agendado"
        ).execute()

        # Criando a lista do index e a lista dos horários
        index = defaultdict(list)
        index2 = defaultdict(list)

        # declarando variavel dos eventos
        events = events_result.get('items', [])

        # verificando se há datas, caso tenha ele vai pro else...
        if not events:
            print('Nenhum evento com a descrição "agendado" encontrado nos próximos 60 dias.')
        else:
            print('Eventos com a descrição "agendado" nos próximos 60 dias:')
            # Criando a lista com os eventos
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                end = event['end'].get('dateTime', event['end'].get('date'))
                traco = '-'
                horario_inicial = start[0:19]
                horario_final = end[11:19]
                horario = horario_inicial + traco + horario_final
                id_evento = event['id']
                index2[id_evento].append(event)
                index[horario].append(event)
                # pegando a lista com index criado, adicionando e numerando nas duas variáveis 
                eventos = (list(enumerate(index.keys(), 0)))
                eventos_id = (list(enumerate(index2.keys(), 0)))

            if not eventos:
                print("Não há datas disponiveis")
            else:
                # indexação para acessar o item desejado na lista
                index_desejado = str(eventos_id[0])
                index_texto = index_desejado[5:31]

                event = service.events().get(calendarId='itaimoveis7@gmail.com', eventId=index_texto).execute()
                # Corpo do novo evento(transformando numa data disponivel)

                try:
                    service.events().delete(calendarId=calendar_id, eventId=index_texto).execute()
                    print("Evento excluído com sucesso!")
                except Exception as e:
                    print(f"Erro ao excluir o evento: {e}")
                                 
            event = {
                        'summary': f'Data Disponível,{codigo_imovel}',
                        'description': f'disponivel,{codigo_imovel}',
                        'start': {
                            'dateTime': start,
                            'timeZone': 'America/Sao_Paulo',
                        },
                        'colorId': '1',
                        'end': {
                            'dateTime': end,
                            'timeZone': 'America/Sao_Paulo',
                        },
                            }

            event = service.events().insert(calendarId=calendar_id, body=event).execute()