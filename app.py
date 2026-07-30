from flask import Flask, render_template, request, redirect

import sqlite3

app = Flask(__name__)

def enregistrer_signalement(type_signalement):
    zone = request.form.get("zone")
    description = request.form.get("description")
    telephone = request.form.get("telephone")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO signalements
        (type, zone, description, telephone)
        VALUES (?, ?, ?, ?)
        """,
        (type_signalement, zone, description, telephone)
    )

    conn.commit()
    conn.close()


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
