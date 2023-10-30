from selenium import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from imap_tools import *
import time
from pandas import * 
import pandas
from selenium.common.exceptions import NoSuchElementException
import imaplib
import email
from email.header import decode_header
from exportar import exportar
import os
import email
import re
from bs4 import BeautifulSoup
import requests
from enviaremail import automatizar_email
from automacao_planilha import planilhauto
import requests
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import datetime
from google.oauth2 import service_account
from agendar_data import RetornarData
import locale
from collections import defaultdict
from agendar_data import RetornarData
from excluir_agendamento import excluiragendamento
from email.message import EmailMessage
import smtplib
