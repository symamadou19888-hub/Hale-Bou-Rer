with open("static/css/style.css", "r", encoding="utf-8") as f:
    css = f.read()

ancien_form = '''form {
    background: white;
    padding: 20px;
    border-radius: 12px;
    max-width: 500px;
    margin: auto;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}'''

nouveau_form = '''form {
    background: white;
    padding: 24px;
    border-radius: 20px;
    max-width: 500px;
    margin: auto;
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}'''

ancien_carte = '''.carte-signalement {
    background: white;
    max-width: 500px;
    margin: 20px auto;
    padding: 20px;
    border-radius: 18px;
    text-align: left;
    box-shadow: 0 4px 12px rgba(0,0,0,0.12);
}'''

nouveau_carte = '''.carte-signalement {
    background: white;
    max-width: 500px;
    margin: 20px auto;
    padding: 22px;
    border-radius: 20px;
    text-align: left;
    box-shadow: 0 4px 16px rgba(0,0,0,0.1);
    transition: transform 0.15s ease;
}

.carte-signalement:active {
    transform: scale(0.99);
}'''

ancien_body_h1 = '''body h1 {
    margin-top: 20px;
}'''

nouveau_body_h1 = '''body h1 {
    margin-top: 20px;
    color: #2E7D32;
    font-size: 26px;
}'''

remplacements = [
    (ancien_form, nouveau_form),
    (ancien_carte, nouveau_carte),
    (ancien_body_h1, nouveau_body_h1),
]

tout_ok = True
for ancien, nouveau in remplacements:
    if ancien in css:
        css = css.replace(ancien, nouveau)
    else:
        print("ERREUR : bloc non trouve ->", ancien[:40])
        tout_ok = False

if tout_ok:
    with open("static/css/style.css", "w", encoding="utf-8") as f:
        f.write(css)
    print("Design pages harmonise avec succes")
