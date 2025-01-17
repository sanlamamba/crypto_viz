import React, { useEffect, useState } from "react";
import { ApiService } from "@/data/apiService";
import {  CryptoDataHistory, CurrencyData } from "@/data/interface/coin";

const CurrencyDashboard: React.FC<{ currencyName: string }> = ({ currencyName }) => {
  const [currentData, setCurrentData] = useState<CurrencyData | null>(null);
  const [historyData, setHistoryData] = useState<CryptoDataHistory[] | null>(null);
  const [currencies, setCurrencies] = useState<CurrencyData[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCurrencyData = async () => {
      setLoading(true);
      setError(null);

      try {
        const current = await ApiService.getCurrentCurrency(currencyName);
        const history = await ApiService.getCurrencyHistory(currencyName);
        const availableCurrencies = await ApiService.getCurrencies();

         console.log(current)
         console.log(history)
         console.log(availableCurrencies)
        setCurrentData(current);
        setHistoryData(history);
        setCurrencies(availableCurrencies);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchCurrencyData();
  }, [currencyName]);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h1>Cryptocurrency Dashboard</h1>
      <h2>Current Data for {currencyName}:</h2>
      <pre>{JSON.stringify(currentData, null, 2)}</pre>

      <h2>History Data:</h2>
      <pre>{JSON.stringify(historyData, null, 2)}</pre>

      <h2>Available Currencies:</h2>
      <ul>
        {currencies?.map((currency) => (
          <li key={currency.currency_id}>
            Market Cap: {currency.market_cap} 
            Price : ({currency.price})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CurrencyDashboard;
