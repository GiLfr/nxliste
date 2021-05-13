import colorama
import coloredlogs
import logging
import pandas as pd
import xlsxwriter

colorama.init()
logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG')

logger.info("Génération des fichiers markdown dans l'arborescence docs...")

# lstNotes=['0', '0,5', '1', '1,5', '2', '2,5', '3', '3,5', '4', '4,5', '5']
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

# headerKS="Titre|Note|Sortie|Nb Episodes\n:---:|:---:|:---:|:---:\n"
# headerAS="Titre|Note|Sortie|Nb Episodes\n:---:|:---:|:---:|:---:\n"
# headerEC="Titre|Etat|Sortie|Nb Episodes\n:---:|:---:|:---:|:---:\n"
# headerKF="Titre|Note|Sortie\n:---:|:---:|:---:\n"
# headerAF="Titre|Note|Sortie\n:---:|:---:|:---:\n"
# mdKS="title: K-Séries\n\n#Séries Coréennes\n\n"+headerKS
# mdAS="title: Autres Séries\n\n#Autres séries (non Coréennes)\n\n"+headerAS
# mdEC="title: Séries en cours\n\n#Séries en cours\n\n"+headerEC
# mdKF="title: K-Films\n\n#Films Coréens\n\n"+headerKF
# mdAF="title: Autres Films\n\n#Autres Films (non Coréens)\n\n"+headerAF

header="Titre|Information\n:---:|:---\n"
mdIndex="title: Accueil\n\n#Accueil\n\n"
mdLast="##Derniers vus... \n\n"+header
mdEC="\n\n##En cours...\n\n"+header
mdS="title: Séries\n\n#Les Séries \n\n"+header
mdF="title: Films\n\n#Les Films \n\n"+header

dfx = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols='A:N')
dfx.sort_values(by=['Note', 'Titre'], ascending=[False, True], inplace=True)
df = dfx.set_index("Titre", drop=False)
for index, row in df.iterrows():
    if row['Note'] in dicoNotes:
        md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|Titre: **'+ str(row['Titre']) +'**<br/>Origine: **'+ str(row['Origine']) + '**<br/>Note: ' + dicoNotes[str(row['Note'])] +'<br/> Sortie en **'+str(int(row['Sortie']))+'**<br/>Nb. épisodes: **'+str(int(row['Episodes']))+'**<br/><br/>_'+str(row['F-Commentaire'])+'_\n'
        if row["Type"] == "Série":
            mdS += md
            # if row['Origine'] =="Corée du Sud":
            #     md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|['+ str(round(float(row['Note'].replace(',','.')),1))+'](){.petit } '+ dicoNotes[str(row['Note'])] +'|'+str(int(row['Sortie']))+'|'+str(int(row['Episodes']))+'\n'
            #     mdKS += md
            # else:
            #     md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|['+ str(round(float(row['Note'].replace(',','.')),1))+'](){.petit } '+ dicoNotes[str(row['Note'])] +'|'+str(int(row['Sortie']))+'|'+str(int(row['Episodes']))+'\n'
            #     mdAS += md
        elif  row["Type"] == "Film":
            mdF += md
            # if row['Origine'] =="Corée du Sud":
            #     md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|['+ str(round(float(row['Note'].replace(',','.')),1))+'](){.petit } '+ dicoNotes[str(row['Note'])] +'|'+str(int(row['Sortie']))+'\n'
            #     mdKF += md
            # else:
            #     md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|['+ str(round(float(row['Note'].replace(',','.')),1))+'](){.petit } '+ dicoNotes[str(row['Note'])] +'|'+str(int(row['Sortie']))+'\n'
            #     mdAF += md
    if row['Note'].lower().strip()[0:8] == "en cours":
        md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|Titre: **'+ str(row['Titre']) +'**<br/>Origine: **'+ str(row['Origine']) + '**<br/>Sortie en **'+str(int(row['Sortie']))+'**<br/>Nb. épisodes: **'+str(int(row['Episodes']))+'**<br/><br/>_'+str(row['F-Commentaire'])+'_\n'
        # md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|' + "en cours" +'|'+str(int(row['Sortie']))+'|'+str(int(row['Episodes']))+'\n'
        mdEC += md

dfx.sort_values(by=['FinVisionnage'], ascending=[False], inplace=True)
df = dfx.set_index("Titre", drop=False)
for index, row in df.head(5).iterrows():
    md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+')|Titre: **'+ str(row['Titre']) +'**<br/>Origine: **'+ str(row['Origine']) + '**<br/>Note: ' + dicoNotes[str(row['Note'])] +'<br/> Sortie en **'+str(int(row['Sortie']))+'**<br/>Nb. épisodes: **'+str(int(row['Episodes']))+'**<br/><br/>_'+str(row['F-Commentaire'])+'_\n'
    mdLast += md

# with open("docs/kserie.md", "w", encoding='utf-8') as f: 
#     f.write(mdKS) 

# with open("docs/aserie.md", "w", encoding='utf-8') as f: 
#     f.write(mdAS) 

# with open("docs/kfilm.md", "w", encoding='utf-8') as f: 
#     f.write(mdKF) 

# with open("docs/afilm.md", "w", encoding='utf-8') as f: 
#     f.write(mdAF) 

# with open("docs/kr/index.md", "w", encoding='utf-8') as f: 
#     f.write(mdKS) 

# with open("docs/kr/kfilm.md", "w", encoding='utf-8') as f: 
#     f.write(mdKF) 

mdIndex = mdIndex + mdLast + '\n\n' + mdEC
with open("docs/index.md", "w", encoding='utf-8') as f: 
    f.write(mdIndex)

with open("docs/film.md", "w", encoding='utf-8') as f: 
    f.write(mdF) 

with open("docs/serie.md", "w", encoding='utf-8') as f: 
    f.write(mdS) 

logger.info("Fin de la génération")
print('\x1b[6;30;42m' + 'Success!' + '\x1b[0m')