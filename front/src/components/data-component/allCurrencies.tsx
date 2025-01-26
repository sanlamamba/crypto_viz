import { ApiService } from "@/data/apiService";
import React from "react";

const AllCurrencies: React.FC = () => {
  const { data, loading, error } = ApiService.useCurrencies()
console.log(data, error)
  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>All Currencies</h2>
      <ul>
        {data?.map((currency) => (
          <li key={currency.id}>
          {currency.id} - {currency.name} - {currency.symbol}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default AllCurrencies;
