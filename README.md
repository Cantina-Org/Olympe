# Olympe

# Olympe est actuellement en refonte totale ! Il est très fortement recommandé de ne pas l'installer !

Olympe est l'outils d'administration en ligne de la suite cantina

### ⚠️: Installer Olympe peut causer des problèmes sur votre machine si vous faites de mauvaises manipulations ! À vos risques et périls 😆 !

***

## Contribuer :

#### Attention : l'installation de l'outil [Olympe](https://github.com/Cantina-Org/Olympe) (conseillé via [Ouranos](https://github.com/Cantina-Org/Ouranos)) est obligatoire ! (Sinon c'est un peu comme avoir une voiture sans les roues 😇.)

### Étape 1:
Cloner votre [fork](https://github.com/Cantina-Org/Olympe/fork) de Olympe.

### Étapes 2:
Créer un fichier `config.json` à la racine du projet Olympe.

### Étapes 3:
Remplisser le fichier `config.json` avec ça: 
```json
{
    "database": [
        {
            "database_username": "",
            "database_password": "",
            "database_addresse": "",
            "database_port": ""
        }
    ],
    "port": 3000
}
``` 
Compléter les champs de la catégorie `database` avec les identifiants de votre base de données.


### Étapes 4:
Lancer le fichier `app.py` via votre éditeur de code. (Vous devez exécuter le fichier depuis le dossier du projet). 

### Étapes 5:
Rendez-vous sur la page `[host:port]/` pour visualiser le service.

***

