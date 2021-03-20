import pandas as pd

import xlsxwriter

lstNotes=['0', '0,5', '1', '1,5', '2', '2,5', '3', '3,5', '4', '4,5', '5']

header="Titre|Note|Sortie|Nb Episodes\n:---|:---:|:---:|:---:\n"
mdKS="title: K-Séries\n\n#Séries Coréennes\n\n"+header
mdKF="title: K-Films\n\n#Films Coréens\n\n"+header

dfx = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols='A:K')
dfx.sort_values(by=['Note', 'Titre'], ascending=[False, True], inplace=True)
df = dfx.set_index("Titre", drop=False)
for index, row in df.iterrows():
    if row['Note'] in lstNotes:
        if row['Origine'] =="Corée du Sud":
            md=str(row['Titre'])+'|'+str(row['Note'])+' :material-star:{ .gold .heart } |'+str(int(row['Sortie']))+'|'+str(int(row['Episodes']))+'\n'
            if row["Type"] == "Série":
                mdKS += md
            elif  row["Type"] == "Film":
                mdKF += md

with open("docs/index.md", "w", encoding='utf-8') as f: 
    f.write(mdKS) 

with open("docs/kfilm.md", "w", encoding='utf-8') as f: 
    f.write(mdKF) 