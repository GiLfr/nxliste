import colorama
import coloredlogs
import logging
import os
import sys
import pandas as pd
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow, Flow
from google.auth.transport.requests import Request
from google.oauth2 import service_account
# from googleapiclient import discovery

colorama.init()
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

logger.info("Génération du catalogue des tableaux ...")

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'local/mygs-1612688472909-c6c8d4eab650.json'
RANGE_NAME = 'A:W'

credentials = None
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# id de mon google sheet
spreadsheet_id = '1R5BnkwmZsRk3g4gL2GiCgfmFTLPahJeGE01YBRudYi0'

service = build('sheets', 'v4', credentials=credentials, cache_discovery=False)

sheet_id = '615388927'  # Liste
sheet_nom = 'Listing des tableaux'  # Liste

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

# rep=r"F:\\Images\\Personnel\\Divers\\Tableaux_Bischwiller\\"
# rep=r"F:/Images/Personnel/Divers/Tableaux_Bischwiller/"
rep = r'local/tableaux/'
header = '\nPhoto|Information\n:---:|:---\n'
# sdp='\newpage'
sdp = '\n<div style="page-break-after: always;"></div>\n'

md = '# Liste des tableaux de Bischwiller\n'

df = pd.DataFrame(values_input, columns=values_input[0])

# Suppression de la 1ère ligne (ligne de titre)
# df.iloc[1:, :]
df.drop(index=0, axis=0, inplace=True)
df_mask = df[df['Attribué_Nelly'] == '1']

for index, ligne in df_mask.iterrows():
    md += sdp
    md += header
    photo = '![Photo ' + str(ligne['Num_Photo']).strip() + '](' + rep + 'TAB_' + str(ligne['Num_Photo']).strip() + '.jpg)'
    info = 'Numéro ligne: '+str(ligne['Num_Ligne']).strip()+'<br/>'
    info += 'Numéro photo: '+str(ligne['Num_Photo']).strip()+'<br/>'
    info += '_Localisation_'+'<br/>'
    info += '       Etage: **'+str(ligne['Etage']).strip()+'**<br/>'
    info += '       Pièce: **'+str(ligne['Pièce']).strip()+'**<br/>'
    info += 'Regroupement: **'+str(ligne['Regroupement']).strip()+'**<br/>'
    info += 'Description : **'+str(ligne['Description']).strip()+'**<br/>'
    info += 'Format      : **'+str(ligne['Format']).strip()+'**<br/>'
    info += 'Dimension   : **'+str(ligne['Dimension']).strip()+'cm**<br/>'

    md += photo+'|'+info+'\n'

    if str(ligne['Commentaires']) != 'None':
        md += '\n\n'+str(ligne['Commentaires'])+'\n\n'
    else:
        md += '\n\n\n\n'

    if ligne['Num_Photo_bis'] != 'X':
        md += '\n\n---\n\n'
        md += '\n\n_Souhaité par_\n\n'
        sh = []
        if str(ligne['Souhait_Nelly']).strip() == '1':
            sh.append('Nelly')
        if str(ligne['Souhait_Hugues']).strip() == '1':
            sh.append('Hugues')
        if str(ligne['Souhait_Gilles']).strip() == '1':
            sh.append('Gilles')
        if str(ligne['Souhait_Christiane']).strip() == '1':
            sh.append('Christiane')
        if str(ligne['Souhait_Véronique']).strip() == '1':
            sh.append('Véronique')
        if str(ligne['Souhait_Isabelle']).strip() == '1':
            sh.append('Isabelle')
        if str(ligne['Souhait_Poussy']).strip() == '1':
            sh.append('Poussy')
        if str(ligne['Souhait_David']).strip() == '1':
            sh.append('David')
        if str(ligne['Souhait_Magali']).strip() == '1':
            sh.append('Magali')
        md += "**"+", ".join(sh)+"**"
        md += '\n\n---\n\n'
        md += '\n\n_Attribué à_\n\n'
        sh = []
        if str(ligne['Attribué_Nelly']).strip() == '1':
            sh.append('Nelly')
        if str(ligne['Attribué_Christiane']).strip() == '1':
            sh.append('Christiane')
        if str(ligne['Attribué_Poussy']).strip() == '1':
            sh.append('Poussy')
        md += "**"+", ".join(sh)+"**"

with open("Les_tableaux_de_Nelly.md", "w", encoding='utf-8') as f:
    f.write(md)

# # Writing the data into the excel sheet
# writer_obj = pd.ExcelWriter('Les_tableaux_de_Bisch.xlsx',
#                             engine='xlsxwriter')
# df.to_excel(writer_obj, sheet_name='Liste')
# writer_obj.save()

logger.info("Le fichier Les_tableaux_de_Bisch.xlsx est chargé")
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
