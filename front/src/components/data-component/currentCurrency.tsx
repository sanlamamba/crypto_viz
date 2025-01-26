import { ApiService } from "@/data/apiService";
import React from "react";
import { PriceCard } from "../price-card";

const CurrencyDetails: React.FC<{ currencyName: string }> = ({ currencyName }) => {
  const { data, loading, error } = ApiService.useCurrentCurrency(currencyName);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <PriceCard currencyName={currencyName} currencyPrice={data?.price} />
      <PriceCard currencyName={currencyName} currencyPrice={data?.marketCap} />
    </div>
  );
};

export default CurrencyDetails;
