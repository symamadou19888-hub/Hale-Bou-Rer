with open("templates/profil.html", "r") as f:
    contenu = f.read()

ancien = '''.ligne-info .icone {
    width: 34px;
    height: 34px;
    border-radius: 10px;
    background: #F7F5F0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 16px;
    flex-shrink: 0;
}
.ligne-info .texte .label {
    font-size: 11px;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.ligne-info .texte .valeur {
    font-size: 15px;
    color: #1A1A1A;
    font-weight: 500;
}'''

nouveau = '''.ligne-info .icone {
    width: 42px;
    height: 42px;
    border-radius: 12px;
    background: #F7F5F0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 19px;
    flex-shrink: 0;
}
.ligne-info .texte {
    flex: 1;
    min-width: 0;
}
.ligne-info .texte .label {
    font-size: 11px;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.ligne-info .texte .valeur {
    font-size: 15px;
    color: #1A1A1A;
    font-weight: 500;
    word-break: break-word;
    overflow-wrap: break-word;
}'''

if ancien not in contenu:
    print("ERREUR : bloc non trouve, aucune modification faite")
else:
    contenu = contenu.replace(ancien, nouveau, 1)
    with open("templates/profil.html", "w") as f:
        f.write(contenu)
    print("OK : profil corrige avec succes")
