import { ApiService } from "@/data/apiService";
import React from "react";

const CurrencyHistory: React.FC<{ currencyName: string }> = ({ currencyName }) => {
  const { data, loading, error } = ApiService.useCurrencyHistory(currencyName);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Historical Data for {currencyName}</h2>
      <ul>
        {data?.map((entry) => (
          <li key={entry.timestamp}>
            {entry.timestamp}: {entry.price}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CurrencyHistory;
