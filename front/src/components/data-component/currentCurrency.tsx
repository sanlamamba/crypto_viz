import { ApiService } from "@/data/apiService";
import React from "react";

const CurrencyDetails: React.FC<{ currencyName: string }> = ({ currencyName }) => {
  const { data, loading, error } = ApiService.useCurrentCurrency(currencyName);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Currency Details: {currencyName}</h2>
      <p>Price: {data?.price}</p>
      <p>Market Cap: {data?.marketCap}</p>
    </div>
  );
};

export default CurrencyDetails;
