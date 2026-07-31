from flask import Flask, render_template, request, redirect, send_from_directory
from werkzeug.utils import secure_filename

import sqlite3

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
        (type, photo, zone, description, telephone, latitude, longitude)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (type_signalement, nom_photo, zone, description, telephone, latitude, longitude)
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
    conn = sqlite3.connect("database.db")
    signalements = conn.execute("SELECT * FROM signalements ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("signalements.html", signalements=signalements)


@app.route("/resolu/<int:id>", methods=["POST"])
def resolu(id):
    conn = sqlite3.connect("database.db")
    conn.execute("DELETE FROM signalements WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/signalements")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
