# NPM Offline Package Downloader

Outil simple pour télécharger des paquets NPM et leurs dépendances pour un usage offline.
Génère une archive `.tar.gz` prête à être importée dans un environnement offline.

## Utilisation

1. Préparer le `package.json` et générer le `package-lock.json` :

```bash
npm install --package-lock-only --legacy-peer-deps
```

2. Construire l’image Docker :

```bash
make build
```

3. Exécuter le container :

```bash
make run
```

> Résultat : `npm_packages_downloaded/npm_packages_downloaded.tar` contenant tous les paquets NPM téléchargés.

4. Nettoyer (optionnel) :

```bash
make clean    # supprime le dossier de sortie
make purge    # supprime le dossier + l'image Docker
```


## Crédits

Fork du projet https://github.com/AnthonyVdsa/NPM-Offline-Package-Downloader