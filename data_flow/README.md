# 🪙 **CryptoViz : Surveillez les Cryptomonnaies en Temps Réel** 🚀

Bienvenue dans **CryptoViz**, votre solution tout-en-un pour la collecte, le traitement et la visualisation des données de cryptomonnaies. Que vous soyez un passionné de crypto, un analyste de données ou un développeur curieux de l'univers des cryptomonnaies, ce projet est fait pour vous ! 💡

---

## 🌟 **Fonctionnalités Principales**

- **Scraping en Temps Réel :**
  - Collectez des données en temps réel depuis des sources fiables telles que **CoinGecko** et **CoinMarketCap**.
  - Extrayez des informations comme les prix, les capitalisations boursières, et plus encore. 📊

- **Traitement et Validation des Données :**
  - Normalisez les données pour garantir leur cohérence et évitez les doublons.
  - Validez les données collectées pour assurer leur précision. ✅

- **Intégration Kafka :**
  - Gérez les flux de données en temps réel avec **Apache Kafka** en tant que producteur/consommateur.
  - Architecture basée sur des microservices pour une meilleure scalabilité. ⚡

- **Base de Données PostgreSQL :**
  - Stockez les données en temps réel et les données historiques dans une base de données relationnelle.
  - Utilisez des migrations **Alembic** pour maintenir la structure de la base à jour. 📂

- **Visualisation des Données :**
  - Intégration prête avec **Grafana** pour créer des tableaux de bord visuels en temps réel. 📈

- **Planification et Multithreading :**
  - Exécutez des tâches à intervalles réguliers grâce au **scheduler**.
  - **Multithreading** pour exécuter plusieurs tâches simultanément, optimisant ainsi la performance. 🕒

---

## 🛠️ **Structure du Projet**

Le projet est organisé de manière claire pour faciliter la compréhension et la collaboration. Voici un aperçu :

```
/data_flow/
├── README.md               # Documentation principale
├── docker-compose.yml      # Configuration des services Docker (Kafka, PostgreSQL, Grafana)
├── requirements.txt        # Liste des dépendances Python
├── src/                    # Code source principal
│   ├── scrapers/           # Scripts pour extraire les données de CoinGecko et CoinMarketCap
│   ├── kafka_helper/       # Gestion des producteurs et consommateurs Kafka
│   ├── dbConfig/           # Configuration de la base de données et modèles SQLAlchemy
│   ├── utils/              # Outils divers (validation, logging, scheduling, etc.)
│   ├── migrations/         # Scripts de migration Alembic
│   └── main.py             # Point d'entrée principal de l'application
├── tests/                  # Tests unitaires
└── data/                   # Données et logs
```

---

## 🚀 **Comment Démarrer ?**

### 1. **Prérequis**

- **Python 3.12+** 🐍
- **Docker & Docker Compose** 🐳
- **PostgreSQL et Kafka**

### 2. **Installation**

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/sanlamamba/crypto_viz.git
   cd crypto_viz/data_flow
   ```

2. **Créez un environnement virtuel et installez les dépendances** :
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Démarrez les services Docker** :
   ```bash
   docker-compose up -d
   ```

### 3. **Exécution**

- **Lancer le programme principal** :
   ```bash
   python src/main.py
   ```

---

## 🔍 **Tests**

1. **Assurez-vous que les services sont en cours d'exécution** (Kafka, PostgreSQL).
2. **Lancez les tests unitaires avec pytest** :
   ```bash
   pytest tests/
   ```

---

## 🐳 **Services via Docker**

Ce projet utilise **Docker** pour simplifier l'instanciation des différents services nécessaires :

- **PostgreSQL** : Base de données pour stocker les données des cryptomonnaies.
- **Kafka** : Utilisé pour la gestion des flux de données en temps réel.
- **Grafana** : Pour la visualisation et le suivi des données via des tableaux de bord.

Lancer tous ces services est aussi simple que d'exécuter :
```bash
docker-compose up -d
```
Cela assurera que tout est prêt et correctement configuré pour commencer à scraper et traiter les données. 🚀

---

## 🤝 **Contribuer**

Les contributions sont les bienvenues ! Pour contribuer :

1. **Forkez le projet**.
2. **Créez une branche pour vos modifications** :
   ```bash
   git checkout -b feature/ma-feature
   ```
3. **Faites vos commits** et soumettez une **Pull Request**.

Nous sommes ouverts aux idées et suggestions pour améliorer le projet. Chaque contribution compte ! 💪

---

## 🛡️ **Sécurité et Bonnes Pratiques**

- **Variables d'environnement** : Utilisez des variables d'environnement pour gérer les informations sensibles telles que les clés API et les mots de passe. Par exemple, créez un fichier `.env` pour stocker ces informations et assurez-vous de l'ajouter au `.gitignore`.
- **Logs** : Le projet enregistre toutes les actions importantes, facilitant ainsi la détection des problèmes. Les logs sont configurés via `logging_config.py` et sont enregistrés dans le dossier `data/logs`.
- **Tests** : Toujours ajouter des tests pour tout nouveau code écrit, afin de garantir la qualité et la stabilité du projet.
- **Bonnes pratiques pour Docker** : Veillez à limiter les permissions des conteneurs Docker et à surveiller les images utilisées afin de minimiser les risques de sécurité.

---

## ⚙️ **Détails Techniques et Architecture**

- **Scrapers** : Les scrapers pour **CoinGecko** et **CoinMarketCap** sont développés avec **BeautifulSoup** et **requests**, permettant une extraction fiable des données en temps réel.
  - **Scrape Coingecko** : Utilise un soup pour naviguer dans les tables HTML afin d'extraire les noms, les prix, les capitalisations des cryptomonnaies et plus encore.
  - **Scrape CoinMarketCap** : Utilise un sélecteur CSS avec **BeautifulSoup** pour extraire les données pertinentes avec des sélecteurs personnalisés.

- **Kafka Integration** : Le système est basé sur une architecture à événements utilisant **Kafka**.
  - **Producteur Kafka** : Normalise les données et les envoie vers le topic Kafka `crypto_viz`.
  - **Consommateur Kafka** : Récupère les messages pour les traiter et les stocker dans la base de données.
  - Kafka est configuré pour fonctionner avec un broker accessible en local via Docker, facilitant le développement.

- **Base de Données** : La base de données **PostgreSQL** est structurée pour séparer les données actuelles et historiques des cryptomonnaies.

| Modèle                  | Description                                                                                     |
|-------------------------|-------------------------------------------------------------------------------------------------|
| **currencies**          | Contient les informations statiques des cryptomonnaies (nom, symbole).                         |
| **currency_data**       | Stocke les données en temps réel (prix actuel, capitalisation).                                |
| **currency_data_history** | Archive les données historiques, assurant une traçabilité des variations des cryptomonnaies.    |

  - Les données sont mises à jour toutes les minutes, les anciennes valeurs étant archivées dans la table `currency_data_history`.

- **Migrations Alembic** : Les changements de structure de base de données sont gérés avec **Alembic**.
  - Cela permet de suivre et d'appliquer des mises à jour de schéma de base de données de manière ordonnée et collaborative.
  - Les fichiers de migration sont bien organisés, permettant d'historier les changements.

- **Normalisation des Données** : La classe `DataNormalizer` permet de regrouper les données collectées, de résoudre les conflits potentiels et de normaliser le format final avant l'insertion en base.
  - **Résolution des Conflits** : Utilise des stratégies telles que le choix de la valeur majoritaire ou celle avec le meilleur facteur de confiance.
  - **Formatage Standardisé** : Le format final inclut des informations telles que le nom, le prix, la source, et le facteur de confiance pour garantir la cohérence des données.

- **Multithreading** : Le module `threading` est utilisé pour exécuter des tâches comme le scraping et la consommation Kafka de manière concurrente.
  - Cela augmente l'efficacité du processus en utilisant plusieurs threads pour exécuter les tâches parallèlement.
  - Le script `threading.py` encapsule la logique pour faciliter l'utilisation des threads dans le projet.

- **Planification des Tâches** : Le **scheduler** intégré à l'aide de la bibliothèque `schedule` permet de définir des intervalles réguliers pour la collecte des données.
  - Le programme principal est configuré pour exécuter un scraping des données toutes les minutes.
  - Les tâches planifiées sont gérées de manière à garantir une collecte continue sans interruption.

- **Flux de Données** :
  - **Scraping** : Le processus de scraping est exécuté toutes les minutes, extrayant les données depuis CoinGecko et CoinMarketCap.
  - **Normalisation** : Les données sont ensuite normalisées pour éviter les conflits et garantir la qualité des données.
  - **Production Kafka** : Une fois les données prêtes, elles sont envoyées dans un topic Kafka via un producteur Kafka.
  - **Consommation et Stockage** : Un consommateur Kafka récupère les données, les traite et les stocke dans la base de données PostgreSQL, en les archivant si nécessaire.

- **Producteur et Consommateur** :
  - **Producteur** : Le producteur Kafka, défini dans `kafka_helper/producer.py`, envoie les données normalisées dans le topic Kafka `crypto_viz`.
  - **Consommateur** : Le consommateur, défini dans `kafka_helper/consumer.py`, écoute ce topic, traite les messages entrants et les insère dans la base de données. La fonction `process_data` est utilisée pour gérer le traitement des données avant l'insertion.

---

## 📧 **Contact**

Pour toute question, suggestion ou simplement pour dire bonjour, contactez-nous via [GitHub](https://github.com/sanlamamba). Nous serions ravis d'échanger avec vous ! 😊

Merci d'avoir choisi **CryptoViz** pour explorer le monde des cryptomonnaies. Nous espérons que ce projet vous aidera à comprendre et analyser l'univers fascinant des cryptos d'une manière simple et efficace. 🚀

---

✨ **Bon Scraping !** ✨

