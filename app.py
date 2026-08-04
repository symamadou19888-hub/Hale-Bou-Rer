from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import sqlite3
import os
import time

dernieres_publications = {}
DELAI_MINIMUM = 120  # secondes entre deux publications par IP

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def enregistrer_signalement(type_signalement):
    ip = request.remote_addr
    maintenant = time.time()

    if ip in dernieres_publications:
        temps_ecoule = maintenant - dernieres_publications[ip]
        if temps_ecoule < DELAI_MINIMUM:
            return False

    dernieres_publications[ip] = maintenant

    prenom = request.form.get("prenom")
    age = request.form.get("age")
    sexe = request.form.get("sexe")
    ville = request.form.get("ville")

    zone = request.form.get("zone")
    description = request.form.get("description")
    telephone = request.form.get("telephone")
    latitude = request.form.get("latitude") or None
    longitude = request.form.get("longitude") or None

    photo = request.files.get("photo")
    nom_photo = None

    if photo and photo.filename:
        nom_photo = secure_filename(photo.filename)
        photo.save("uploads/" + nom_photo)

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO signalements
        (type, photo, zone, description, telephone, latitude, longitude, statut, prenom, age, sexe, ville)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            type_signalement,
            nom_photo,
            zone,
            description,
            telephone,
            latitude,
            longitude,
            "actif" if MODE_TEST else "en_attente",
            prenom,
            age,
            sexe,
            ville
        )
    )

    conn.commit()
    conn.close()


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


@app.route("/")
def accueil():
    conn = sqlite3.connect("database.db")
    nb_aujourdhui = conn.execute(
        "SELECT COUNT(*) FROM signalements WHERE statut='actif' AND date(date_creation) = date('now')"
    ).fetchone()[0]
    conn.close()
    return render_template("index.html", nb_aujourdhui=nb_aujourdhui)


@app.route("/trouve", methods=["GET", "POST"])
def trouve():
    if request.method == "POST":
        resultat = enregistrer_signalement("trouve")
        if resultat is False:
            return render_template("trouve.html", erreur_spam="Veuillez patienter avant de publier un nouveau signalement.")
        return redirect("/")
    return render_template("trouve.html")


@app.route("/perdu", methods=["GET", "POST"])
def perdu():
    if request.method == "POST":
        resultat = enregistrer_signalement("perdu")
        if resultat is False:
            return render_template("perdu.html", erreur_spam="Veuillez patienter avant de publier un nouveau signalement.")
        return redirect("/")
    return render_template("perdu.html")


@app.route("/signalements")
def signalements():
    filtre = request.args.get("filtre")
    recherche = request.args.get("recherche", "").strip()
    prenom = request.args.get("prenom", "").strip()
    ville = request.args.get("ville", "").strip()
    age = request.args.get("age", "").strip()
    sexe = request.args.get("sexe", "").strip()

    conn = sqlite3.connect("database.db")

    requete = "SELECT * FROM signalements WHERE statut='actif'"
    parametres = []

    if filtre in ("trouve", "perdu"):
        requete += " AND type=?"
        parametres.append(filtre)

    if recherche:
        requete += " AND (zone LIKE ? OR prenom LIKE ? OR ville LIKE ? OR age LIKE ? OR sexe LIKE ? OR description LIKE ?)"
        parametres.extend([
            f"%{recherche}%",
            f"%{recherche}%",
            f"%{recherche}%",
            f"%{recherche}%",
            f"%{recherche}%",
            f"%{recherche}%"
        ])

    if prenom:
        requete += " AND prenom LIKE ?"
        parametres.append(f"%{prenom}%")

    if ville:
        requete += " AND ville LIKE ?"
        parametres.append(f"%{ville}%")

    if age:
        requete += " AND age LIKE ?"
        parametres.append(f"%{age}%")

    if sexe:
        requete += " AND sexe=?"
        parametres.append(sexe)

    requete += " ORDER BY id DESC"

    signalements = conn.execute(requete, parametres).fetchall()
    conn.close()

    return render_template(
        "signalements.html",
        signalements=signalements,
        recherche=recherche,
        filtre=filtre
    )


@app.route("/api/dernier-id")
def api_dernier_id():
    conn = sqlite3.connect("database.db")
    result = conn.execute("SELECT MAX(id) FROM signalements WHERE statut='actif'").fetchone()
    conn.close()
    dernier_id = result[0] if result[0] else 0
    return {"dernier_id": dernier_id}


@app.route("/resolu/<int:id>", methods=["POST"])
def resolu(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM signalements WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/signalements")


MOT_DE_PASSE_ADMIN = os.getenv("MOT_DE_PASSE_ADMIN")

MODE_TEST = True  # True = publication directe sans moderation, False = moderation normale

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        mot_de_passe = request.form.get("mot_de_passe")
        if mot_de_passe != MOT_DE_PASSE_ADMIN:
            return render_template("admin_login.html", erreur="Mot de passe incorrect")

        conn = sqlite3.connect("database.db")
        en_attente = conn.execute(
            "SELECT * FROM signalements WHERE statut='en_attente' ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return render_template("admin.html", signalements=en_attente, mot_de_passe=mot_de_passe)

    return render_template("admin_login.html", erreur=None)


@app.route("/admin/valider/<int:id>", methods=["POST"])
def admin_valider(id):
    mot_de_passe = request.form.get("mot_de_passe")
    if mot_de_passe != MOT_DE_PASSE_ADMIN:
        return redirect("/admin")

    conn = sqlite3.connect("database.db")
    conn.execute("UPDATE signalements SET statut='actif' WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")


@app.route("/admin/rejeter/<int:id>", methods=["POST"])
def admin_rejeter(id):
    mot_de_passe = request.form.get("mot_de_passe")
    if mot_de_passe != MOT_DE_PASSE_ADMIN:
        return redirect("/admin")

    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM signalements WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/admin")




@app.route("/detail/<int:id>")
def detail(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM signalements WHERE id=?", (id,))
    signalement = cursor.fetchone()
    conn.close()

    if signalement is None:
        return "Signalement introuvable", 404

    return render_template("detail.html", signalement=signalement)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
