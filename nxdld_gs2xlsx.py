import colorama
import coloredlogs
import logging
import os
import sys
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

logger.info("Analyse du fichier HTML (Ma Liste - Netflix) ...")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'local/mygs-1612688472909-c6c8d4eab650.json'
RANGE_NAME = 'A:Q'

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
# request = service.spreadsheets().values().append(
#     spreadsheetId=spreadsheet_id, 
#     range=sheet_nom, 
#     valueInputOption='USER_ENTERED', 
#     insertDataOption='INSERT_ROWS', 
#     body={"values": df.values.tolist()}
#     )
request = service.spreadsheets().values().get(
    spreadsheetId=spreadsheet_id,
    range=RANGE_NAME)

response = request.execute()
# print(response)

values_input = response.get('values', [])
if not values_input:
    logger.error("Pas de données trouvées")
    print('\x1b[6;30;41m' + 'Echec!' + '\x1b[0m')
    sys.exit()

df=pd.DataFrame(values_input[1:], columns=values_input[0])

# Writing the data into the excel sheet
writer_obj = pd.ExcelWriter('maListeNetflix.xlsx',
                            engine='xlsxwriter')
df.to_excel(writer_obj, sheet_name='Liste')
writer_obj.save()

logger.info("Le fichier maListeNetflix.xlsx est chargé")
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')