# import re
import colorama
import coloredlogs
import logging
# import numpy as np
import pandas as pd
import shutil
import xlsxwriter
from bs4 import BeautifulSoup
from termcolor import colored
from pathlib import Path
import os
import datetime

current_time = datetime.datetime.now()
timestamp_wp = current_time.timestamp()
timestamp = str(timestamp_wp).replace(".", "_")

colorama.init()
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

# logger.debug("this is a debugging message")
# logger.info("this is an informational message")
# logger.warning("this is a warning message")
# logger.error("this is an error message")
# logger.critical("this is a critical message")

# class bcolors:
#     HEADER = '\033[95m'
#     OKBLUE = '\033[94m'
#     OKCYAN = '\033[96m'
#     OKGREEN = '\033[92m'
#     WARNING = '\033[93m'
#     FAIL = '\033[91m'
#     ENDC = '\033[0m'
#     BOLD = '\033[1m'
#     UNDERLINE = '\033[4m'

# html = open('maListeNetflix.html','r')
# html = open('test.html','r')

dfi = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols='A:L')
# dfi = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols = "B,C")

html = open('Netflix.html', 'r', encoding="utf8")
soup = BeautifulSoup(html, 'html.parser')
m1 = soup.findAll('p', {'class': 'fallback-text'})

soup2 = BeautifulSoup(html, 'lxml')
lines = soup.findAll('div', attrs={'class': 'rowContainer rowContainer_title_card'}, limit=None)
# data = [[x.text for x in y.findAll('p', {'class': 'fallback-text'},limit=None)] for y in lines]
data = [x.text for x in soup.findAll('p', {'class': 'fallback-text'}, limit=None)]
# vign = [y['src'].split("/")[-1] for y in soup.findAll('img', {'class': 'boxart-image-in-padded-container'}, limit=None)]
vign = [Path(y['src']).stem for y in soup.findAll('img', {'class': 'boxart-image-in-padded-container'}, limit=None)]

dfn = pd.DataFrame(data, columns=['Titre'])
dfn['Vignette'] = pd.DataFrame(vign)

# dfs = df.sort_values(by='Titre')

# print(dfi)
# print(dfn)

dfd = dfi.merge(dfn, on='Titre', how='outer', indicator=True).loc[lambda x: x['_merge'] == 'right_only']
dfr = dfd.drop(columns=['Unnamed: 0', 'Vignette_x', 'Type', 'Origine', 'Sortie', 'Saison',
            'Episodes', 'Note', 'FinVisionnage', 'Deadline', 'F-Commentaire', '_merge'])
dfr["Type"] = "Série"
dfr["Origine"] = "Corée du Sud"
dfr["Sortie"] = "2022"
dfr["Saison"] = "1"
dfr["Episodes"] = "16"
dfr["Note"] = "à voir..."
dfr["FinVisionnage"] = ""
dfr["Deadline"] = ""
dfr["F-Commentaire"] = "!CONTROL INFOS!"
# print(dfr)
# print("# nouveauté: ", len(dfr.index))
# dfr = df.compare(dfi)
# dfr = pd.merge(df, dfi, how="inner", on=["Titre", "Vignette"])

# Copie des nouvelles vignettes
newname_vignette = []
try:
    for image in dfr['Vignette_y']:
        path = Path(image)
        img_name = os.path.splitext(path.stem)[0]
        img_ext  = path.suffix
        newname = img_name[:30] + "_" + timestamp + img_ext
        nvFichier = shutil.copy('Netflix_files/'+image, 'docs/images/nx/'+newname)
        newname_vignette.append(newname)
    logger.info("Copie de {} Vignettes".format(len(dfr.index)))
except FileExistsError:
    logger.error("Erreur sur fichier dans la copie des Vignettes")
except:
    logger.error("Erreur inconnue dans la copie des Vignettes")

dfr['Vignette_y'] = pd.DataFrame(newname_vignette)

# Boucle sur les nouveautés (à ajouter dans la liste)
# for index, row in dfd.iterrows():
#     print("Titre: ",row["Titre"])
#     print("Vignette: ",row["Vignette_y"])


# OLD VERSION
# # Writing the data into the excel sheet
# writer_obj = pd.ExcelWriter('deltaNetflix.xlsx',
#                             engine='xlsxwriter')
# dfr.to_excel(writer_obj, sheet_name='delta')
# writer_obj.save()

# NEW VERSION
with pd.ExcelWriter('deltaNetflix.xlsx') as writer:
    dfr.to_excel(writer, sheet_name='delta')


# print(bcolors.HEADER + 'Regarder le fichier deltaNetflix.xlsx.'+bcolors.ENDC)
# print(colored('Regarder le fichier deltaNetflix.xlsx.','green', attrs=['reverse', 'blink']))
logger.info("Stocker dans le fichier deltaNetflix.xlsx")
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')
