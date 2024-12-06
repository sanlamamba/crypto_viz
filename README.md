# CryptoViz

## Overview:
CryptoViz is a  crypto visualization tool designed for real-time market insights.

## Key Features:

 - Data Scraping: Python-based scrapers collect live and historical data from major cryptocurrency websites, ensuring high accuracy and up-to-date information.
- Data Processing: Kafka efficiently streams and processes the scraped data, enabling real-time updates and handling high-volume traffic.
- Data Storage: PostgreSQL (PSQL) serves as the robust backend database, offering scalability and secure storage for all processed data.
- API Integration: Quarkus API facilitates fast and lightweight interaction with the database, ensuring seamless communication between data storage and the visualization layer.
- Visualization: Grafana connects to the Quarkus API, delivering rich and interactive dashboards that provide actionable insights for cryptocurrency analysis.


 ## Prerequisites
Before starting, ensure you have the following installed on your system:

- Docker: For running the data flow and Grafana services.
- Java 17+: Required for the Quarkus API.
- Maven: For building and managing the Quarkus API dependencies.
- Python: If required for data scraping scripts.

### Start the Data Flow and Grafana


The data flow services and Grafana are managed via Docker Compose.

1. Navigate to the directory containing the `docker-compose.yml` file:
   ```bash
   cd data_flow
   ```

2. Run the following command to start the services:
   ```bash
   docker-compose up -d
   ```

3. Verify that the services are running:
   ```bash
   docker-compose ps
   ```

   **Included Services**:
   - **Kafka**: For streaming data.
   - **PostgreSQL**: For storing cryptocurrency data.
   - **Grafana**: For visualizing the data.


## 3. Run the Quarkus API in Development Mode

1. Navigate to the Quarkus API directory:
   ```bash
   cd back
   ```

2. Start the Quarkus API in development mode:
   ```bash
   ./mvnw quarkus:dev
   ```
   > **Note**: Use `mvn` if `mvnw` is not available:
   > ```bash
   > mvn quarkus:dev
   > ```

3. The API will be accessible at:
   ```
   http://localhost:8080
   ```
## Data Flow 
We utilize Beautiful Soup, a Python library, to scrape specific cryptocurrency information from different the source website.
Each scrappers have his file 


## BDD Table 


### Table `cryptocurrencies`

| **Champ**       | **Type**   | **Description**                                   |
|------------------|------------|---------------------------------------------------|
| `id`            | `UUID`     | Identifiant unique de la cryptomonnaie.           |
| `name`          | `VARCHAR`  | Nom complet de la cryptomonnaie (e.g., Bitcoin).  |
| `symbol`        | `VARCHAR`  | Symbole court (e.g., BTC, ETH).                   |

---

### Table `currency_data`

| **Champ**        | **Type**       | **Description**                                                |
|-------------------|----------------|----------------------------------------------------------------|
| `currency_id`    | `UUID`         | Référence à l'ID de la table `cryptocurrencies`.               |
| `price`          | `DECIMAL`      | Prix actuel de la cryptomonnaie.                               |
| `market_cap`     | `DECIMAL`      | Capitalisation boursière actuelle.                            |
| `updated_at`     | `TIMESTAMP`    | Date et heure de la dernière mise à jour.                     |
| `source`         | `VARCHAR`      | Source des données (e.g., site web ou API).                   |
| `trust_factor`   | `INTEGER`      | Indicateur de confiance des données (échelle arbitraire).      |

---

### Table `crypto_data_history`

| **Champ**        | **Type**       | **Description**                                                |
|-------------------|----------------|----------------------------------------------------------------|
| `id`             | `UUID`         | Identifiant unique pour chaque enregistrement historique.      |
| `currency_id`    | `UUID`         | Référence à l'ID de la table `cryptocurrencies`.               |
| `price`          | `DECIMAL`      | Prix de la cryptomonnaie à ce moment précis.                   |
| `market_cap`     | `DECIMAL`      | Capitalisation boursière à ce moment précis.                   |
| `timestamp`      | `TIMESTAMP`    | Horodatage des données historiques collectées.                 |
| `source`         | `VARCHAR`      | Source des données historiques (e.g., site web ou API).        |
| `trust_factor`   | `INTEGER`      | Indicateur de confiance des données historiques.               |
| `created_at`     | `TIMESTAMP`    | Date et heure d'enregistrement dans la base de données.        |

 ## API Quarkus
Endpoint documentation

---

### Documentation des Endpoints

| **Endpoint**                       | **Méthode** | **Description**                                                                 | **Paramètres**                     | **Exemple de Réponse**                                     |
|------------------------------------|-------------|---------------------------------------------------------------------------------|------------------------------------|-----------------------------------------------------------|
| **`/currencies`**                  | `GET`       | Récupère la liste de toutes les cryptomonnaies disponibles.                     | Aucune                             | `[{"id": "uuid", "name": "Bitcoin", "symbol": "BTC"}]`     |
| **`/currencies/current`**          | `GET`       | Récupère les données actuelles (prix et market cap) de toutes les cryptomonnaies.| Aucune                             | `[{"id": "uuid", "price": "40000", "market_cap": "800B"}]`|
| **`/{currencyName}/history`**      | `GET`       | Récupère les données historiques d'une cryptomonnaie donnée.                    | `currencyName` : Nom de la monnaie | `[{"timestamp": "2024-01-01", "price": "30000"}]`         |
| **`/{currencyName}/current`**      | `GET`       | Récupère les données actuelles d'une cryptomonnaie donnée.                      | `currencyName` : Nom de la monnaie | `{"id": "uuid", "price": "40000", "market_cap": "800B"}`  |


### Exemples de Réponses

#### 1. **Liste des cryptomonnaies** (`GET /currencies`)
```json
[
    {"id": "uuid1", "name": "Bitcoin", "symbol": "BTC", "price": "40000", "market_cap": "800B"},
    {"id": "uuid2", "name": "Ethereum", "symbol": "ETH", "price": "3000", "market_cap": "500B"}
]
```

#### 2. **Données actuelles de toutes les cryptomonnaies** (`GET /currencies/current`)
```json
[
    {"id": "uuid1", "name": "Bitcoin", "symbol": "BTC", "price": "40000", "market_cap": "800B"},
         {"id": "uuid2", "name": "Ethereum", "symbol": "ETH", "price": "3000", "market_cap": "500B"}
]
```

#### 3. **Données historiques pour une cryptomonnaie** (`GET /bitcoin/history`)
```json
[
    { "id": "uuid1", "name": "Bitcoin","timestamp": "2024-01-01T12:00:00Z", "price": "30000", "market_cap": "600B"},
    { "id": "uuid2","name": "Ethereum","timestamp": "2024-01-02T12:00:00Z", "price": "32000", "market_cap": "640B"}
]
```

#### 4. **Données actuelles pour une cryptomonnaie** (`GET /bitcoin/current`)
```json
{
    "id": "uuid1",
    "price": "40000",
    "market_cap": "800B",
    "source": "example.com",
    "trust_factor": 9
}
```

# Grafana
 - Liste des Cryptomonnaies
 - Time Series  des cryptos ( evolution du prix)
 - Bar chart  ( comparer le prix de plusieurs cryptos du top 10)
 - Price et Market Cap du Bitcoin
 - Price et Market Cap de Etherum
 - Jauge de trust factor ( BTC, ETH ? )

  
