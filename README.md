# README - Liste de mes séries sur Netflix

## Initialisation du dépôt

- Disposer des alias sous /users/<user>/.bashrc
- Lancer le script bash 'init_repo.sh'

## Programmes python

1. nxliste_selaccess.py: accès via Selenium à Netflix et positionnement sur "Ma Lsite"
_Sauvegarde manuelle de la page HTML sous "Netflix.html"_
2. nxxlsx_loadgs.py: accès à Google Sheet et récupération de **maListeNetflix** au format Excel
3. nxhtml_extractdelta.py: Chargement de **Netflix.html** sous pandas, et comparaison avec **maListeNetflix.xlsx** pour en extraire le delta dans **deltaNetflix.xslx**
_Ajout manuel dans Google Spreadsheet **maListeNetflix** du delta_
