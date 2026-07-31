from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

import sqlite3
import os

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def enregistrer_signalement(type_signalement):
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
        (type, photo, zone, description, telephone, latitude, longitude, statut)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (type_signalement, nom_photo, zone, description, telephone, latitude, longitude, "en_attente")
    )

    conn.commit()
    conn.close()


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory("uploads", filename)


@app.route("/")
def accueil():
    return render_template("index.html")


@app.route("/trouve", methods=["GET", "POST"])
def trouve():
    if request.method == "POST":
        enregistrer_signalement("trouve")
        return redirect("/")
    return render_template("trouve.html")


@app.route("/perdu", methods=["GET", "POST"])
def perdu():
    if request.method == "POST":
        enregistrer_signalement("perdu")
        return redirect("/")
    return render_template("perdu.html")


@app.route("/signalements")
def signalements():
    filtre = request.args.get("filtre")
    recherche = request.args.get("recherche", "").strip()

    conn = sqlite3.connect("database.db")

    requete = "SELECT * FROM signalements WHERE statut='actif'"
    parametres = []

    if filtre in ("trouve", "perdu"):
        requete += " AND type=?"
        parametres.append(filtre)

    if recherche:
        requete += " AND zone LIKE ?"
        parametres.append(f"%{recherche}%")

    requete += " ORDER BY id DESC"

    signalements = conn.execute(requete, parametres).fetchall()
    conn.close()
    return render_template("signalements.html", signalements=signalements, recherche=recherche, filtre=filtre)


@app.route("/resolu/<int:id>", methods=["POST"])
def resolu(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM signalements WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/signalements")


MOT_DE_PASSE_ADMIN = os.getenv("MOT_DE_PASSE_ADMIN")

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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
