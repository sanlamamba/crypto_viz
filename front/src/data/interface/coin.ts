// Interface for the `cryptocurrencies` table
export interface Cryptocurrency {
    id: string; // UUID
    name: string; // Full name of the cryptocurrency
    symbol: string; // Short symbol (e.g., BTC, ETH)
  }
  
  // Interface for the `currency_data` table
  export interface CurrencyData {
    currencyId: string; // UUID - Reference to `cryptocurrencies.id`
    price: number; // Current price of the cryptocurrency
    marketCap: number; // Current market capitalization
    updated_at: string; // ISO 8601 date-time format
    source: string; // Data source (e.g., CoinMarketCap, Binance)
    trustFactor: number; // Confidence indicator (e.g., 0–100 scale)
  }
  
  // Interface for the `crypto_data_history` table
  export interface CryptoDataHistory {
    id: string; // UUID - Unique ID for historical record
    currency_id: string; // UUID - Reference to `cryptocurrencies.id`
    price: number; // Historical price of the cryptocurrency
    marketCap: number; // Historical market capitalization
    timestamp: string; // ISO 8601 date-time format - When data was collected
    source: string; // Data source (e.g., CoinMarketCap, Binance)
    trustFactor: number; // Confidence indicator (e.g., 0–100 scale)
    created_at: string; // ISO 8601 date-time format - When data was added to the database
  }

  export  interface MergedCryptoData {
    id: string;
    name: string;
    symbol: string;
    price: number;
    marketCap: number;
    updated_at: string;
    source: string;
    trustFactor: number;
  }
  
  // Combined interface for the entire data structure
  export interface CryptoData {
    cryptocurrencies: Cryptocurrency[]; // Array of cryptocurrencies
    currency_data: CurrencyData[]; // Array of current data for cryptocurrencies
    crypto_data_history: CryptoDataHistory[]; // Array of historical data for cryptocurrencies
  }
  