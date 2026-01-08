# NPM Offline Package Downloader

Outil simple pour télécharger des paquets NPM et leurs dépendances pour un usage offline.
Génère une archive `.tar.gz` prête à être importée dans un environnement sans internet.

## Pré-requis

*   **Docker** (et Docker Compose) installé et lancé.
*   **Make** (uniquement pour Linux/macOS).
*   Avoir le fichier `package.json` à la racine du projet.

## Installation et Préparation

**Récupérez le projet et placez-vous dans le dossier :**

    ```bash
    git clone https://github.com/UnDesSix/NPM-Offline-Package-Downloader
    cd NPM-Offline-Package-Downloader
    ```



---

## Utilisation

### 🐧 Linux / macOS

La commande `make` par défaut se charge de construire l'image et de lancer le téléchargement :

```bash
make
```

> **Nettoyage (optionnel) :**
> *   `make clean` : Supprime le dossier de sortie.
> *   `make purge` : Supprime le dossier et l'image Docker.

### 🪟 Windows

Utilisez **Docker Compose** (via PowerShell ou CMD) :

1.  **Construire l’image :**
    ```bash
    docker compose build
    ```

2.  **Lancer le téléchargement :**
    ```bash
    docker compose up
    ```

---

## Résultat

Une fois le processus terminé, vous trouverez l'archive contenant tous les paquets dans le dossier :

📂 `out/packages_npm.tar.gz`

## Crédits

Fork du projet [AnthonyVdsa/NPM-Offline-Package-Downloader](https://github.com/AnthonyVdsa/NPM-Offline-Package-Downloader).