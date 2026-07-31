def enregistrer_signalement(type_signalement):
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
            "en_attente",
            prenom,
            age,
            sexe,
            ville
        )
    )

    conn.commit()
    conn.close()
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
