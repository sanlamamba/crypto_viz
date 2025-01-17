import { CurrencyData, CryptoDataHistory } from "./interface/coin";

const BASE_URL = "http://localhost:8080/http";

export class ApiService {
  /**
   * Fetch the current data for a specific currency.
   * @param currencyName - The name of the currency.
   * @returns A Promise resolving to CurrencyData.
   */
  static async getCurrentCurrency(currencyName: string): Promise<CurrencyData> {
    return this.fetchData<CurrencyData>(`${BASE_URL}/${currencyName}/current`);
  }

  /**
   * Fetch the historical data for a specific currency.
   * @param currencyName - The name of the currency.
   * @returns A Promise resolving to CryptoDataHistory.
   */
  static async getCurrencyHistory(currencyName: string): Promise<CryptoDataHistory[]> {
    return this.fetchData<CryptoDataHistory[]>(`${BASE_URL}/${currencyName}/history`);
  }

  /**
   * Fetch the list of all available currencies.
   * @returns A Promise resolving to an array of currency names (strings).
   */
  static async getCurrencies(): Promise<CurrencyData[]> {
    return this.fetchData<CurrencyData[]>(`${BASE_URL}/currencies`);
  }

  /**
   * Generic fetch method to retrieve data from the API.
   * @param url - The URL to fetch data from.
   * @returns A Promise resolving to the data of type T.
   */
  private static async fetchData<T>(url: string): Promise<T> {
    try {
      const response = await fetch(url);
      console.log(`Fetching: ${url}`);
      console.log(`Response status: ${response.status}`);
      if (!response.ok) {
        console.error(`Error: HTTP status ${response.status}`);
        throw new Error(`HTTP error! Status: ${response.status}`);
      }
      const data = await response.json();
      console.log(`Data from ${url}:`, data);
      return data;
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  }
  
}