import os
from pathlib import Path

# chemin vers les ressources de l'application
PATH_APP = os.path.join(Path.home(), "Tenant Manager")
PATH_APP_DATA = os.path.join(PATH_APP, ".data")

# chemin vers le dossier destiner aux recus
MONTLY_RECEIPT_DIR = os.path.join(PATH_APP, "receipt montly")
ADVANCE_RECEIPT_DIR = os.path.join(PATH_APP, "receipt in advance")

# chemin vers le dossier des locataires enregistrer
USER_DIR = os.path.join(PATH_APP_DATA, "user")
# chemin vers le dossier des recus enregistrer
RECEIPT_DIR = os.path.join(PATH_APP_DATA, "receipt")

# Mois de l'annee
MONTH = ["Janvier",
         "Fevrier",
         "Mars",
         "Avril",
         "Mai",
         "Juin",
         "Juillet",
         "Aout",
         "Septembre",
         "Octobre",
         "Novembre",
         "Décembre"]
# texte d'introduction
INTRO_TEXT = """<html>
<head>
	<title></title>
</head>
<body>
<p style="text-align: center;">Tenant Manager</p>

<p>Tenant Manager est une application de gestion de locataire. Il permet de creer des recus personnaliser a des locataires avec un format deja defini. Pour une experience optimal, il est conseiller ajouter les utilisateurs avant de creer des recu.</p>

<p>&nbsp;Il y a deux categorie d&#39;utilisateur, les locataires et les gerants. C&#39;est le nom des gerants qui est afficher pour prouver la verasiter du recu.</p>

<p>&nbsp;Il existe egalement deux type de recu. Les avances et les recu mensuel. Les recu mensuels peuvent etre delivrer plusieurs fois, contrairement aux avances qui ne peuvent etre delivrer qu&#39;une fois a un meme locataire.</p>
</body>
</html>
"""
