import React from "react";
import AllCurrentCurrencies from "./data-component/allCurrentCurrencies";
import CurrencyDetails from "./data-component/currentCurrency";
import CurrencyHistory from "./data-component/CurrencyHistory";

const CurrencyDashboard: React.FC<{ currencyName?: string }> = ({ currencyName }) => {
  return (
    <div className="space-y-6">
      <AllCurrentCurrencies />

      {currencyName ? (
        <>
          <CurrencyDetails currencyName={currencyName} />
          <CurrencyHistory currencyName={currencyName} />
        </>
      ) : (
        <p className="text-center text-gray-500">Select a cryptocurrency to view its details.</p>
      )}
    </div>
  );
};

export default CurrencyDashboard;
