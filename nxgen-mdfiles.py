import pandas as pd

import xlsxwriter

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

header="Titre|Note|Sortie|Nb Episodes\n:---:|:---:|:---:|:---:\n"
mdKS="title: K-Séries\n\n#Séries Coréennes\n\n"+header
mdKF="title: K-Films\n\n#Films Coréens\n\n"+header

dfx = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols='A:K')
dfx.sort_values(by=['Note', 'Titre'], ascending=[False, True], inplace=True)
df = dfx.set_index("Titre", drop=False)
for index, row in df.iterrows():
    if row['Note'] in dicoNotes:
        if row['Origine'] =="Corée du Sud":
            md='![Affiche de '+str(row['Titre'])+'](images/nx/'+str(row['Vignette'])+'){width: 100px}|['+ str(round(float(row['Note'].replace(',','.')),1))+'](){.petit } '+ dicoNotes[str(row['Note'])] +'|'+str(int(row['Sortie']))+'|'+str(int(row['Episodes']))+'\n'
            if row["Type"] == "Série":
                mdKS += md
            elif  row["Type"] == "Film":
                mdKF += md

with open("docs/index.md", "w", encoding='utf-8') as f: 
    f.write(mdKS) 

with open("docs/kfilm.md", "w", encoding='utf-8') as f: 
    f.write(mdKF) 

# with open("docs/kr/index.md", "w", encoding='utf-8') as f: 
#     f.write(mdKS) 

# with open("docs/kr/kfilm.md", "w", encoding='utf-8') as f: 
#     f.write(mdKF) 