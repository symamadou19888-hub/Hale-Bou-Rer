with open("app.py", "r", encoding="utf-8") as f:
    contenu = f.read()

ancien = '''load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))'''

nouveau = '''load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


@app.route("/service-worker.js")
def service_worker():
    response = send_from_directory("static", "service-worker.js")
    response.headers["Service-Worker-Allowed"] = "/"
    response.headers["Content-Type"] = "application/javascript"
    return response'''

if ancien not in contenu:
    print("ERREUR : marqueur introuvable")
else:
    contenu = contenu.replace(ancien, nouveau, 1)
    with open("app.py", "w", encoding="utf-8") as f:
        f.write(contenu)
    print("OK : route service-worker.js ajoutée")
