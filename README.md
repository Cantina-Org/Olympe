# HoloTable

# HoloTable est actuellement en refonte totale ! Il est très fortement recommandé de ne pas l'installer !

HoloTable est l'outil d'administration et le Single Sign On de la suite de logiciel opensource **Cantina**

### ⚠️: HoloTable est encore à un stade de développement avancé ! L'installer en production comporte donc de nombreux risques potentiellement irréversibles ! L'équipe de Cantina ne sera en aucun cas responsable des dommages crées et vous incite à attendre une version plus aboutie ! À vos risques et périls 😆 !

***

## Contribuer :

### Étape 1:
Cloner votre [fork](https://github.com/Cantina-Org/HoloTable/fork) de HoloTable.

### Étapes 2:
Créer un fichier `config.json` à la racine du projet HoloTable.

### Étapes 3:
Remplisser le fichier `config.json` avec ça: 
```json
{
  "database": [{
    "username": "db_database",
    "password": "db_password",
    "address": "db_address",
    "port": 3306
  }],
  "modules": [{
    "name": "holotable",
    "port": 3000,
    "maintenance": false,
    "debug_mode": false
  }]
}
``` 
Compléter les champs de la catégorie `database` avec les identifiants de votre base de données de teste.

### Étapes 4:
Lancer le fichier `app.py` via votre éditeur de code. (Vous devez exécuter le fichier depuis le dossier du projet). 

### Étapes 5:
Rendez-vous sur la page `[host:port]/` pour visualiser le service.

***

