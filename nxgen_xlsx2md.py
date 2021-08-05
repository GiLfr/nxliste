import colorama
import coloredlogs
import datetime
import logging
import numpy as np
import pandas as pd
import re
import xlsxwriter


def bloc_vign(enreg):
    # Affichage de la vignette
    vign='![Affiche de '+str(enreg['Titre'])+'](images/nx/'+str(enreg['Vignette'])+')<br/>'
    # Retrait de la série/du film
    retrait=''
    if re.findall(r"[\d]{1,2}/[\d]{1,2}/[\d]{4}", str(enreg['Deadline'])) :
        date_retrait=pd.to_datetime(enreg['Deadline'], format="%d/%m/%Y")
        # Affectaton icone de retrait
        retrait=':material-television:'
        if enreg['Plateform'] == 'Netflix':
            retrait=':material-netflix:{ .rouge }'
        elif enreg['Plateform'] == 'Amazon Prime':
            retrait=':material-amazon:{ .turquoise }'
        elif enreg['Plateform'] == 'Viki':
            retrait=':fontawesome-brands-korvue:'
        # Test de la deadline
        if date_retrait > datetime.datetime.now():
            retrait+='<span style="color:darkred" class="blink">'
            retrait+=' ATTENTION ! - Dernier jour sur '+ enreg['Plateform'] + ' le ' + str(enreg['Deadline'])
            retrait+='</span>'
        else:
            retrait+='<span style="color:darkorange">'
            retrait+='Retiré de '+ enreg['Plateform'] + ' le ' + str(enreg['Deadline'])
            retrait+='</span>'
    if retrait != '':
        vign+=retrait
    return vign + '|'


def bloc_info(enreg):
    # Palmarès si classé
    topicone=''
    if not (pd.isna(enreg['TOP10'])) :
        topicone=':material-numeric-'+ str(int(enreg['TOP10'])) +'-circle:'
        if int(enreg['TOP10']) == 1:
            topicone+='{.num_gold}'
        elif int(enreg['TOP10']) == 2:
            topicone+='{.num_silver}'
        elif int(enreg['TOP10']) == 3:
            topicone+='{.num_copper}'
    # Le titre
    titrex2 = str(enreg['F-Titre'])
    if str(enreg['F-Titre']) != str(enreg['Titre']) :
        titrex2 += ' / ' + str(enreg['Titre'])
    if str(enreg['K-Titre']) != "nan" :
        titrex2 += ' / ' + str(enreg['K-Titre'])
    # les sous-titres disponible en KR (:material-subtitles-outline:)
    soustitre=''
    if str(enreg['CoreenCC']) == "Oui":
        soustitre=':kr: sous-titres en coréens'
    # Le bloc d'info
    if topicone == '':
        info=''
    else:
        info='Palmarès: ' + topicone + '<br/>'
    info+=enreg['Type']+' : **'+ titrex2 +'**<br/>'
    info+='Origine: **'+ str(enreg['Origine']) + '**<br/>'
    if enreg['Note'] in dicoNotes:
        info+='Note: ' + dicoNotes[str(enreg['Note'])] +'<br/>'
    info+='Sortie en **'+str(int(enreg['Sortie']))+'**<br/>'
    if enreg['Type'] != 'Film':
        info+='Nb. épisodes: **'+str(int(enreg['Episodes']))+'**<br/>'
    if soustitre != '':
        info+=soustitre+'<br/>'
    info+='<br/>_'+str(enreg['F-Commentaire']).strip()+'_'
    info+='\n' # retour à la ligne du tableau md
    # Output de la fonction
    return info


colorama.init()
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

logger.info("Génération des fichiers markdown dans l'arborescence docs...")

dicoNotes={
    '0':   ':material-star:{.grey }:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }',
    '0,5': ':material-star-half-full:{.gold .heart}:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }',
    '1':   ':material-star:{.gold .heart}:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }',
    '1,5': ':material-star:{.gold }:material-star-half-full:{.gold .heart}:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }',
    '2':   ':material-star:{.gold }:material-star:{.gold .heart}:material-star:{.grey }:material-star:{.grey }:material-star:{.grey }',
    '2,5': ':material-star:{.gold }:material-star:{.gold }:material-star-half-full:{.gold .heart}:material-star:{.grey }:material-star:{.grey }',
    '3':   ':material-star:{.gold }:material-star:{.gold }:material-star:{.gold .heart}:material-star:{.grey }:material-star:{.grey }',
    '3,5': ':material-star:{.gold }:material-star:{.gold }:material-star:{.gold }:material-star-half-full:{.gold .heart}:material-star:{.grey }',
    '4':   ':material-star:{.gold }:material-star:{.gold }:material-star:{.gold }:material-star:{.gold .heart}:material-star:{.grey }',
    '4,5': ':material-star:{.gold }:material-star:{.gold }:material-star:{.gold }:material-star:{.gold }:material-star-half-full:{.gold .heart}',
    '5':   ':material-star:{.gold }:material-star:{.gold }:material-star:{.gold }:material-star:{.gold }:material-star:{.gold .heart}'
}

header="Affiche|Information\n:---:|:---\n"
mdIndex="title: Accueil\n\n#Accueil\n\n"
mdLast="##Derniers vus\n\n"+header
mdEC="\n\n##En cours...\n\n"+header
md10="\n\n##Top 10\n\n"+header
mdS="title: Séries\n\n#Les Séries\n_(par pays et par ordre alphabétique)_"
mdF="title: Films\n\n#Les Films\n_(par pays et par ordre alphabétique)_"
mdD="title: Documentaires\n\n#Les Documentaires\n_(par pays et par ordre alphabétique)_"
mdE="title: Emmissions\n\n#Les Emissions\n_(par pays et par ordre alphabétique)_"
OrigineS = ''
OrigineF = ''
OrigineD = ''
OrigineE = ''

dfx = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols='B:R')
dfx.sort_values(by=['Type','Origine','Titre'], ascending=[True, True, True], inplace=True)
df = dfx.set_index("Titre", drop=False)
for index, row in df.iterrows():
    if row['Note'] in dicoNotes:
        md=bloc_vign(row)
        md+=bloc_info(row)
        if row["Type"] == "Série":
            if OrigineS != row['Origine']:
                mdS +="\n\n##" + row['Origine'] + "\n\n"+header
            mdS += md
            OrigineS = row["Origine"] 
        elif  row["Type"] == "Film":
            if OrigineF != row['Origine']:
                mdF +="\n\n##" + row['Origine'] + "\n\n"+header
            mdF += md
            OrigineF = row["Origine"] 
        elif  row["Type"] == "Documentaire":
            if OrigineD != row['Origine']:
                mdD +="\n\n##" + row['Origine'] + "\n\n"+header
            mdD += md
            OrigineD = row["Origine"] 
        elif  row["Type"] == "Emission":
            if OrigineE != row['Origine']:
                mdE +="\n\n##" + row['Origine'] + "\n\n"+header
            mdE += md
            OrigineE = row["Origine"] 
    if row['Note'].lower().strip()[0:8] == "en cours":
        md=bloc_vign(row)
        md+=bloc_info(row)
        mdEC += md

dfx['FinVisionnage'] = pd.to_datetime(dfx['FinVisionnage'], format="%d/%m/%Y")
dfx.sort_values(by=['FinVisionnage'], ascending=[False], inplace=True)
df = dfx.set_index("Titre", drop=False)
for index, row in df.head(10).iterrows():
    md=bloc_vign(row)
    md+=bloc_info(row)
    mdLast += md

dfx.sort_values(by=['TOP10'], ascending=[True], inplace=True)
df = dfx.set_index("Titre", drop=False)
for index, row in df.head(10).iterrows():
    md=bloc_vign(row)
    md+=bloc_info(row)
    md10 += md

mdIndex = mdIndex + mdLast + '\n\n' + mdEC  + '\n\n' + md10
with open("docs/index.md", "w", encoding='utf-8') as f: 
    f.write(mdIndex)

with open("docs/film.md", "w", encoding='utf-8') as f: 
    f.write(mdF) 

with open("docs/serie.md", "w", encoding='utf-8') as f: 
    f.write(mdS) 

with open("docs/documentaire.md", "w", encoding='utf-8') as f: 
    f.write(mdD) 

# with open("docs/emission.md", "w", encoding='utf-8') as f: 
#     f.write(mdE) 

logger.info("Fin de la génération")
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')