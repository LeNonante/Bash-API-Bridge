# Guide d'Utilisation - API-Bash Bridge

Bienvenue dans la documentation d'API-Bash Bridge. Cette application vous permet de déclencher des commandes système (Bash, Shell) via de simples requêtes HTTP sécurisées.
## 🚀 Première Connexion et Configuration

L'application se lance par défaut sur le port 5000. Pour changer ce port, veuillez ajouter la variable `PORT=XXXX` avec XXXX le port souhaité dans le fichier `.env` à la racine du projet. Si le fichier n'exxiste pas (application encore jamais éxécutée), vous pouvez le créer. 

Lors du tout premier lancement de l'application, vous serez automatiquement redirigé vers la page de création du compte administrateur.

![Image page d'enregistrement](/static/docs/register.png)

- **Préfixe API :** Définissez le préfixe de base pour toutes vos routes (par défaut : bashapi).

    Exemple : Si vous mettez v1, vos URLs ressembleront à http://IP_SERVEUR:PORT/v1/ma-route.

- **Mot de passe Administrateur :** Choisissez un mot de passe fort. Il servira uniquement à accéder à l'interface web de l'administrateur avec le username 'admin'.

Cliquez sur Créer le compte.

Lors de sa création l'application est crée en mode "Whitelist". Plus de détails dans la section "Paramètres et Sécurité -> Filtrage IP" 

*Note : Une fois le compte créé, vous serez redirigé vers la page de connexion.*

## 🖥️ Le Tableau de Bord (Dashboard)

Une fois connecté, vous arrivez sur le tableau de bord principal. C'est ici que vous gérez vos endpoints.

![Image page principale](/static/docs/dashboard.png)

- **Mises à jour :** Lorsqu'une nouvelle version de l'application est disponible, un bouton est visible. Cliquez dessus pour mettre à jour l'application.

- **Statistiques :** Vue rapide sur le nombre de routes actives et inactives.

- **Barre de recherche :** Filtrez vos routes par nom, méthode, tag ou commande.

- Liste des routes :

    - **Toggle (Interrupteur) :** Activez ou désactivez une route instantanément sans la supprimer.

    - **Bouton Copier :** Copie l'URL complète de l'endpoint dans votre presse-papier.

    - **Bouton Éditer :** Ouvre les détails de la route.

## 🛠️ Créer et Gérer des Routes
### Ajouter une nouvelle route

Cliquez sur le bouton Ajouter une route en haut à droite du dashboard.

![Image page de nouvelle route](/static/docs/new_path.png)

- **Méthode HTTP :** Choisissez le verbe HTTP qui déclenchera l'action (généralement POST ou GET).

- **Endpoint Path :** Le chemin de l'URL (ex: deploy/mon-site).

    - **Attention :** Ne mettez pas le préfixe API ici, il est ajouté automatiquement.

- **Tags :** Entre les étiquettes associées à cette route, séparées par des virgules. 

- **Script Bash :** Entrez les commandes à exécuter.

    - Vous pouvez écrire plusieurs lignes.

    - L'application enchaînera les commandes avec des && (l'exécution s'arrête si une commande échoue).

- **Description :** (Optionnel) Un mémo pour vous rappeler à quoi sert cette route.

- **Retourner la sortie de la commande :** Si coché, le texte affiché par votre script (via `echo`, `cat`, etc.) sera renvoyé dans le corps de la réponse API. Utile pour récupérer des informations (ex: version d'un logiciel, contenu d'un fichier).

- **Token :** Un token de sécurité est généré automatiquement (voir section Sécurité).

### Tester une route (Sandbox)

Dans la page d'édition d'une route, vous disposez d'un bouton Tester.

![Image sortie de test de commandes](/static/docs/test.png)

- Cela exécute réellement la commande sur le serveur.

- Le retour standard (stdout) et les erreurs (stderr) s'affichent directement dans l'interface web.

- Idéal pour débugger vos scripts sans ouvrir un terminal SSH.

### Zone de Danger

En bas de la page d'édition :

- **Générer un nouveau token :** Invalide l'ancien token immédiatement. N'oubliez pas de mettre à jour vos applications tierces (Stream Deck, n8n, etc.).

- **Supprimer la route :** Action irréversible.

## 🔀 Paramètres Dynamiques

Vous pouvez rendre vos scripts interactifs en leur passant des paramètres lors de l'appel API (via l'URL ou un corps JSON).

### 1. Rédaction du script
L'application convertit automatiquement les paramètres reçus en **variables d'environnement** :
* Le nom du paramètre est mis en **majuscules**.
* Le préfixe `PARAM_` est ajouté.

**Exemple :** Si vous envoyez `nomdossier`, la variable sera `PARAM_NOMDOSSIER`.

**Syntaxe selon votre OS :**
* **Linux (Bash) :** Utilisez `$PARAM_VOTRE_VARIABLE` (ex: `mkdir "$PARAM_NOMDOSSIER"`)
* **Windows (CMD) :** Utilisez `%PARAM_VOTRE_VARIABLE%` (ex: `mkdir "%PARAM_NOMDOSSIER%"`)

### 2. Envoi des paramètres
Vous pouvez passer les valeurs de deux manières lors de votre requête HTTP :

* **Dans l'URL :**
    `http://votre-serveur:PORT/bashapi/ma-route?nomdossier=projet_alpha`

* **Dans le corps JSON (POST uniquement) :**
    ```json
    {
      "nom": "projet_alpha"
    }
    ```


## 🔌 Comment appeler l'API

Pour déclencher vos commandes depuis un outil externe, vous devez effectuer une requête HTTP avec les critères suivants :

- **URL :** Celle copiée depuis le dashboard.

- **Méthode :** Celle définie dans la route (GET, POST, etc.).

- **Authentification :** Obligatoire via un Bearer Token.

**Exemple avec cURL :**

Supposons une route /deploy avec le token mon_token.
```Bash
curl -X POST http://votre-serveur:5000/bashapi/deploy \
     -H "Authorization: Bearer mon_token" \
     -H "Content-Type: application/json" \
     -d '{"branche": "main", "version": "1.2.0"}'
```
### Où trouver le Token ?

Le token est récupérable uniquement dans la page Éditer la route ou lors de la création. Utilisez le bouton "Copier" situé dans la zone "Détails" ou "Zone de Danger".

- **Sécurité :** Les tokens sont stockés de manière hachée (chiffrée) dans la base de données. Il est impossible de retrouver un token enregistré. Ainsi, lorsque vous copiez un token depuis la page d'édition d'une route, un nouveau token est généré ce qui invalide les anciens tokens de cette route. (Cela n'est pas le cas sur la page de création d'une route. Vous pouvez copier le token autant de fois que vous le souhaitez).

### Format de réponse

Par défaut, l'API renvoie :
```json
{
  "message": "Commande exécutée: ...",
  "status": 0
}
```

Si l'option **"Retourner la sortie"** est activée pour la route, un champ `output` s'ajoute :

```json
{
  "message": "Commande exécutée: cat mon_fichier.txt",
  "status": 0,
  "output": "Contenu du fichier texte..."
}
```
## 📰 Logs et Audit

L'application enregistre toutes les tentatives d'accès. Une page de l'interface permet de surveiller l'activité de l'API en direct.

![Image page de logs](/static/docs/logs.png)

- **Les logs contiennent :** Date, IP source, Route appelée, Statut (Succès/Échec/Non autorisé) et un ID de requête unique pour le traçage.
- **Coloration syntaxique :** Les lignes sont colorées selon leur importance (Info, Warnin, Error). De plus, l'état du resultat de la requete est coloré (Echec/Succes).
- **Exporter logs :** Télécharge le fichier api-activity.log. (Une archive ZIP peut remplacer le fichier de logs si plusieurs fichiers de logs existent).

Les logs contiennet uniquement les tentatives d'accès à l'API, et non à l'interface.

## 👤 Gestion des utilisateurs
Si vous êtes connectés au compte administrateur, vous avez accès à l'onglet de gestion des utilisateurs. 

![Image page d'utilisateurs'](/static/docs/users.png)

Sur cette page, il est possible d'ajouter un utilisateur en lui donnant un nom et un mot de passe. Si aucun mot de passe n'est renseigné, il sera généré aléatoirement.

Il est egalement possible de supprimer des comptes utilisateurs (ne fonctionne pas pour l'administrateur) ou de reinitialiser le mot de pase d'un compte (le mot de passe généré ne sera affiché qu'une fois, veillez à bien le copier).

## ⚙️ Paramètres et Sécurité

Accessible via le menu Paramètres.

![Image page de paramètres](/static/docs/settings.png)

### 1. Changement du mot de passe administrateur

- La demande d'un nouveau mot de passe administrateur requiert la vérification du mot de passe actuel.

### 2. Gestion de la double authentification (A2F/OTP)

- **Activation de l'A2F :** Si l'A2F est désactivée, il est possible de l'activer. Le QR code à scanner avec une application d'authentification apparait. Veillez à le scanner avant de recharger la page, car il disparaitra.

- **Régénération du code :** Il est possible de demander un nouveau code d'A2F, pour invalider l'ancien. Cette action requiert la validation du mot de passe administrateur.

- **Désactivation de l'A2F :** Si l'A2F est activée, il est possible de la désactiver. Cette action requiert la validation du mot de passe administrateur.

### 3. Sauvegarde et Migration

- **Exporter commandes.json :** Télécharge un fichier JSON contenant toute votre configuration (routes, commandes, hash des tokens).
- **Importer :** Permet de restaurer une configuration ou de la dupliquer sur un autre serveur.

> **Attention :** Seules les routes (avec commandes, token hashé, et état) sont exportées. Les listes (blacklist et whitelist) ne sont pas exportées ici (voir plus bas).

### 4. Filtrage IP (Whitelist / Blacklist)

Vous pouvez restreindre l'accès à l'API (et non à l'interface admin) selon l'adresse IP de l'appelant.

![Gestion de la Whitelist et Blacklist](/static/docs/list.png)

- **Mode Whitelist (Recommandé) :**

    - Seules les IPs listées peuvent appeler l'API.

    - Toutes les autres sont bloquées (Erreur 503).

    - Idéal si vous connaissez l'IP fixe de votre serveur domotique ou de votre poste de travail.

- **Mode Blacklist :**

    - Tout le monde peut accéder à l'API (si le token est bon).

    - Seules les IPs listées sont bloquées.

*Note : Vous pouvez ajouter une description pour chaque IP (ex: "Serveur Home Assistant") et les activer/désactiver individuellement via un interrupteur.*

Tout comme les commandes, il est possible d'exporter et importer un fichier de configuration de la blacklist et la whitelist.

### 5. Protection Anti-Bruteforce (Rate Limiting)

Pour protéger l'application contre les attaques par force brute et la surcharge, des limites de requêtes sont appliquées :

- **Connexion :** Maximum **5 tentatives par minute**. Au-delà, l'accès est bloqué temporairement.
- **API :** Les appels aux routes API sont limités à **60 requêtes par minute** par IP (par défaut).

En cas de dépassement, l'application renvoie une erreur HTTP **429 Too Many Requests**.

### ⚠️ Bonnes Pratiques

- **Utilisateur Système :** Les commandes Bash sont exécutées avec les permissions de l'utilisateur Linux qui a lancé le service api-bash-bridge. Évitez de lancer l'application en tant que root.

- **Timeout :** Les commandes ont un timeout forcé de 60 secondes. Pour des tâches longues, lancez un script en arrière-plan (ex: nohup mon_script.sh &).

- **Exposition :** N'exposez jamais cette application directement sur Internet sans HTTPS (via un Reverse Proxy comme Nginx ou Apache).