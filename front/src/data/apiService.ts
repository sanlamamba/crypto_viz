import { useFetchData } from "@/hooks/useFetchData";
import { CurrencyData, CryptoDataHistory, Cryptocurrency } from "./interface/coin";

const BASE_URL = "http://localhost:8080/http";

export const ApiService = {
  /**
   * Hook to fetch current data for a specific currency.
   */
  useCurrentCurrency(currencyName: string) {
    const url = `${BASE_URL}/${currencyName}/current`;
    return useFetchData<CurrencyData>(url);
  },

  /**
   * Hook to fetch historical data for a specific currency.
   */
  useCurrencyHistory(currencyName: string) {
    const url = `${BASE_URL}/${currencyName}/history`;
    return useFetchData<CryptoDataHistory[]>(url);
  },

  /**
   * Hook to fetch all available currencies.
   */
  useCurrencies() {
    const url = `${BASE_URL}/currencies`;
    return useFetchData<Cryptocurrency[]>(url);
  },

  /**
   * Hook to fetch current data for all currencies.
   */
  useAllCurrentCurrencies() {
    const url = `${BASE_URL}/currencies/current`;
    return useFetchData<CurrencyData[]>(url);
  },
};
