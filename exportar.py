from importacoes import *

class exportar:
    def exportacao_contatos(self):
        ##CONFIGURANDO JANELA##
        servico = Service(ChromeDriverManager().install())
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--headless=new")
        # chrome_options.add_argument("--window-size=1920,1080")
        janela = webdriver.Chrome(service=servico, options=chrome_options)

        link = 'https://canalpro.grupozap.com/ZAP_OLX/0/leads/messages'
        username = 'itaimoveis7@gmail.com'
        password = 'rj103fab'

        ##APAGANDO TODOS OS EMAILS
        IMAP_SERVER = 'imap.gmail.com'
        USERNAME = 'itaimoveis7@gmail.com'
        PASSWORD = 'pjmupogavhxlwmyk'
        MARCADOR = 'CanalPro'
        # Conectar ao servidor IMAP
        # Conectar-se ao servidor IMAP do seu provedor de email usando SSL
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(USERNAME, PASSWORD)
        import imapclient
        with imapclient.IMAPClient(IMAP_SERVER) as client:
            client.login(USERNAME, PASSWORD)
    
            # Selecionar o marcador (label) desejado
            client.select_folder(MARCADOR)
        
            # Buscar os IDs de todos os emails no marcador
            email_ids = client.search()
        
            if email_ids:
                # Marcar todos os emails no marcador como excluídos
                client.delete_messages(email_ids)


        ##LOGANDO NO SITE E EXPORTANDO DADOS
        janela.get(link)

        while True:
            try:
                logar_usuario = janela.find_element('xpath', '//*[@id="app"]/div[2]/div/div/div/div/section[1]/div/section/form/div[1]/div/div[2]/div/div/input')
                logar_usuario.send_keys(username)
                break
            except NoSuchElementException:
                None
                
        while True:
            try:
                logar_senha = janela.find_element('xpath', '//*[@id="app"]/div[2]/div/div/div/div/section[1]/div/section/form/div[2]/div/div[2]/div/div/input')
                logar_senha.send_keys(password)
                break
            except NoSuchElementException:
                None   

        botao_logar = janela.find_element('xpath', '//*[@id="app"]/div[2]/div/div/div/div/section[1]/div/section/form/button').click()

        while True:
            try:
                janela.execute_script("document.getElementById('privacy-term-alert').style.display='none'")
                break
            except Exception as e:
                None   

        while True:
            try:
                botao_exportar = janela.find_element('xpath', '//*[@id="top-page"]/div/div[1]/div/div[3]/button').click()
                break
            except Exception as e:
                None   

        while True:
            try: 
                botao_exportar2 = janela.find_element('xpath', '//*[@id="top-page"]/div/div[1]/div/div/div[3]/button[2]').click()
                break
            except Exception as e:
                None  

    