with open("templates/signalements.html", "r", encoding="utf-8") as f:
    contenu = f.read()

ancien = '''<div class="filtre-boutons" style="text-align:center; margin-bottom:20px;">
    <a href="/signalements"><button>Tous</button></a>
    <a href="/signalements?filtre=trouve"><button>🟢 Trouvés</button></a>
    <a href="/signalements?filtre=perdu"><button>🟠 Perdus</button></a>
</div>'''

nouveau = '''<div class="filtre-boutons" style="text-align:center; margin-bottom:20px;">
    <a href="/signalements"><button>Tous</button></a>
    <a href="/signalements?filtre=trouve"><button>🟢 Trouvés</button></a>
    <a href="/signalements?filtre=perdu"><button>🟠 Perdus</button></a>
</div>

<form method="GET" action="/signalements" style="text-align:center; margin-bottom:20px;">
    {% if filtre %}<input type="hidden" name="filtre" value="{{ filtre }}">{% endif %}
    <input type="text" name="recherche" placeholder="🔍 Rechercher par quartier..." value="{{ recherche or '' }}" style="width:80%; max-width:400px; padding:12px; border-radius:20px; border:1px solid #ccc;">
</form>'''

if ancien in contenu:
    contenu = contenu.replace(ancien, nouveau)
    with open("templates/signalements.html", "w", encoding="utf-8") as f:
        f.write(contenu)
    print("Champ de recherche ajouté avec succès")
else:
    print("ERREUR : bloc non trouvé")
