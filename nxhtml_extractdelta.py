import pandas as pd
from bs4 import BeautifulSoup
# import re
import numpy as np
import xlsxwriter

# html = open('maListeNetflix.html','r')
# html = open('test.html','r')

dfi = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols='A:K')
# dfi = pd.read_excel('maListeNetflix.xlsx', index_col=None, sheet_name='Liste', usecols = "B,C")

html = open('Netflix.html','r', encoding="utf8")
soup = BeautifulSoup(html,'html.parser')
m1 = soup.findAll('p', {'class': 'fallback-text'})

soup2 = BeautifulSoup(html,'lxml')
lines = soup.findAll('div', attrs = {'class': 'rowContainer rowContainer_title_card'},limit=None)
# data = [[x.text for x in y.findAll('p', {'class': 'fallback-text'},limit=None)] for y in lines]
data = [x.text for x in soup.findAll('p', {'class': 'fallback-text'},limit=None)]
vign = [y['src'].split("/")[-1] for y in soup.findAll('img', {'class': 'boxart-image-in-padded-container'},limit=None)]
dfn = pd.DataFrame(data, columns = ['Titre'])
dfn['Vignette'] = pd.DataFrame(vign)

# dfs = df.sort_values(by='Titre')

print(dfi)
print(dfn)

dfd = dfi.merge(dfn, on='Titre', how = 'outer' ,indicator=True).loc[lambda x : x['_merge']=='right_only']
# print(dfd)

# dfr = df.compare(dfi)
# dfr = pd.merge(df, dfi, how="inner", on=["Titre", "Vignette"])

# Writing the data into the excel sheet
writer_obj = pd.ExcelWriter('deltaNetflix.xlsx',
                            engine='xlsxwriter')
dfd.to_excel(writer_obj, sheet_name='delta')
writer_obj.save()
print('Regarder le fichier deltaNetflix.xlsx.')