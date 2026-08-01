with open("templates/signalements.html", "r", encoding="utf-8") as f:
    contenu = f.read()

ancien = '''<p><b>📞 Contact :</b> {{ signalement[5] }}</p>'''

nouveau = '''<p><b>📞 Contact :</b> Disponible auprès de l'administration après validation.</p>'''

if ancien in contenu:
    contenu = contenu.replace(ancien, nouveau)
    with open("templates/signalements.html", "w", encoding="utf-8") as f:
        f.write(contenu)
    print("Numero masque avec succes")
else:
    print("ERREUR : bloc non trouve")
