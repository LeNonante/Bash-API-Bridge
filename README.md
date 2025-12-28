# API-Bash Bridge

**Transformez vos requêtes HTTP en commandes Shell.**

API-Bash Bridge est une application légère basée sur **Flask** qui permet d'exécuter des commandes système (Bash, Shell, CMD) via une API REST. 

C'est l'outil idéal pour piloter un serveur, lancer des scripts de maintenance, ou redémarrer des services à distance, notamment via un **Elgato Stream Deck** (avec un plugin HTTP) ou des automatisations domotiques.

---

## Fonctionnalités

* **Routing Dynamique :** Ajoutez ou modifiez des routes via une interface web sans redémarrer le serveur.
* **Gestion fine des liaisons :** Activez et désactivez des  liaisons routes API / commandes en un seul clic.
* **Sécurisé :** Protection des routes sensibles via **Bearer Token** (hashé, jamais stocké en clair). La connexion à l'interface se faiut également via un mot de passe administrateur défini à la première connexion.
* **Multi-OS :** Fonctionne sur **Linux** (idéal serveur) et **Windows** (dev/local).
* **Prefix API Configurable :** Changez le préfixe de base (ex: `/api/v1`) depuis l'interface.
* **Importation et exportation de configuration :** Exportez et téléchargez votre configuration dans un fichier JSON puis importer là dans une autre instance de l'application pour récuperer les routes configurées.

---

## Installation & Démarrage avec Systemd
Etant donné que l'application doit executer des commandes systèmes, elle ne peut pas être contenerisée. Voici comment la déployer avec Systemd sur Linux.

Il est recommandé d'installer les applications tierces dans /opt/nom_app. c'est la procédure qui sera expliquée ci-dessous.
```bash
sudo mkdir /opt/api-bash-bridge #Création du dossier
sudo chown -R NOMUSER:NOMUSER /opt/api-bash-bridge #/!\ Remplacer NOMUSER par le nom de votre utilisateur linux
cd /opt/api-bash-bridge #Se déplacer dans le dossier
git clone https://github.com/LeNonante/Bash-API-Bridge.git . #Copie du contenu du repo dans ce dossier

python3 -m venv venv #Création d'un environnement virtuel
./venv/bin/pip install -r requirements.txt #Installation des modules python

sudo ln -s /opt/NOMAPP/NOMAPP.service /etc/systemd/system/NOMAPP.service #Lier le fichier Systemd du repo à un raccopurcis dans les fichiers system du serveur

sudo systemctl daemon-reload #Dire à systemd de lire la nouvelle config
sudo systemctl enable api-bash-bridge #Activer le démarrage automatique au boot
sudo systemctl start api-bash-bridge #Démarrer maintenant
```
---

## Avertissement de Sécurité
ATTENTION : Cette application permet d'exécuter des commandes shell sur la machine hôte.
- Ne l'exposez JAMAIS directement sur internet (port forwarding) sans protection adéquate.
- Utilisez un VPN, un Tunnel Cloudflare (avec authentification Access) ou un proxy inverse (Nginx) avec authentification basic/IP whitelist.
- Soyez prudent avec les commandes que vous configurez dans commandes.json.
---

## Auteur
Projet par LeNonante - Aurélien Musset.

---

## Licence
Projet distribué sous licence MIT. Voir le fichier `LICENSE`.