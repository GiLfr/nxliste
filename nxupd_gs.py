import colorama
import coloredlogs
import logging
import os
import pandas as pd
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow,Flow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
# from googleapiclient import discovery

colorama.init()
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')
# logger.debug("this is a debugging message")
# logger.info("this is an informational message")
# logger.warning("this is a warning message")
# logger.error("this is an error message")
# logger.critical("this is a critical message")

logger.info("Chargement de deltaNetflix.xlsx dans Pandas")

try:
    df = pd.read_excel('deltaNetflix.xlsx', index_col=None, sheet_name='delta', usecols='B:I')
except:
    logger.critical("Erreur de lecture sur le fichier deltaNetflix.xlsx")

# print(df)

# SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'local/mygs-1612688472909-c6c8d4eab650.json'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# id de mon google sheet
spreadsheet_id='1TwcW3o3zUz2uYpG2on1-LSZCSb3P7UDtZZV4XuzsVuk'

service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

sheet_id = '0' # Liste
sheet_nom = 'Liste' # Liste
# sheet_id = '254132304' # Test
# sheet_nom = 'Test' # Test

# Call the Sheets API
request = service.spreadsheets().values().append(
    spreadsheetId=spreadsheet_id, 
    range=sheet_nom, 
    valueInputOption='USER_ENTERED', 
    insertDataOption='INSERT_ROWS', 
    body={"values": df.values.tolist()}
    )
response = request.execute()
logger.info(response)

logger.info("MAJ du Google Spreadsheet effectué à partir du delta")
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')