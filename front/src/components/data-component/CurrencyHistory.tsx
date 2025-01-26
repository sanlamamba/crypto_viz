import { ApiService } from "@/data/apiService";
import React from "react";
import { LineChartComponent } from "../charts/line-chart";

const CurrencyHistory: React.FC<{ currencyName: string }> = ({ currencyName }) => {
  const { data, loading, error } = ApiService.useCurrencyHistory(currencyName);

  if (loading) return <p>Loading...</p>;
  if (error) return <p>Error: {error}</p>;

  return (
    <div>
      <h2>Historical Data for {currencyName}</h2>
      <LineChartComponent  currencyHistoryData={data} currencyName={currencyName} />
    </div>
  );
};

export default CurrencyHistory;
