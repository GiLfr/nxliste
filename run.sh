py nxdld_gs2xlsx.py # py nxxlsx_loadgs.py << OLD version de nxdld_gs2xlsx.py
py nxhtm_delta.py
py nxgen_xlsx2md.py # py nxgen_mdfiles.py << OLD version de nxgen_xlsx2md.py

# Supression du fichier (et dépendances) après utilisation
if [ -f "Netflix.html" ];
then
    py nxupd_xlsx2gs.py
    rm Netflix.html
fi
if [ -d "Netflix_files" ];
then
    rm -r Netflix_files
fi
