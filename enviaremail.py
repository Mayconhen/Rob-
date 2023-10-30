from importacoes import *

class automatizar_email:
    def enviar_email(self):
        while True:
            # Configurações do servidor IMAP e autenticação
            IMAP_SERVER = 'imap.gmail.com'
            USERNAME = 'itaimoveis7@gmail.com'
            PASSWORD = 'pjmupogavhxlwmyk'
            # Conectar ao servidor IMAP
            mail = imaplib.IMAP4_SSL(IMAP_SERVER)
            mail.login(USERNAME, PASSWORD)
            mail.select('CanalPro')
            status, email_ids = mail.search(None, '1')
            
            # Verificando se encontrou algum e-mail
            if email_ids[0]:
                first_email_id = email_ids[0].split()[0]  # Pega o ID do primeiro e-mail
                status, msg_data = mail.fetch(first_email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])

                # Encontrar partes HTML no e-mail
                html_parts = [part for part in msg.walk() if part.get_content_type() == 'text/html']

                first_valid_url = None
                for part in html_parts:
                    html_content = part.get_payload(decode=True).decode('utf-8')
                    soup = BeautifulSoup(html_content, 'html.parser')
                    
                    for link in soup.find_all('a', href=True):
                        url = link['href']
                        if re.match(r'^https?://', url):
                            first_valid_url = url
                            break  # Sai do loop quando encontrar a primeira URL válida
                    if first_valid_url:
                        break
                link = (url)
                nome_do_arquivo = "contatos.xlsx"  # Nome que você deseja dar ao arquivo local
                print(url)
                response = requests.get(link)
                if response.status_code == 200:
                    with open(nome_do_arquivo, 'wb') as f:
                        f.write(response.content)
                    mail.store(first_email_id, '+FLAGS', '(\Deleted)')
                    mail.expunge()  # Efetivamente excluir o e-mail
                    mail.logout()
                    break
                else:
                    None
            else:
                time.sleep(15)
                mail.logout()
                print("E-mail não encontrado...")
                break
                # Não se esqueça de encerrar a conexão após concluir
            
            