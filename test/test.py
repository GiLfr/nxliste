import pathlib

nxfile = pathlib.Path("Netflix.html")
if not nxfile.exists():
    print("Pas de fichier Netflix.html à traiter !")
    # raise TypeError("Pas de fichier Netflix.html à traiter !")  # Provoque une erreur
    # raise SystemExit()                                          # Provoque une erreur
    quit(0)

print("pas bon !!!!!!!!!!!!!!!!")
