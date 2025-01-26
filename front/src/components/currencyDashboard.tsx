import React from "react";
import AllCurrentCurrencies from "./data-component/allCurrentCurrencies";
import CurrencyDetails from "./data-component/CurrentCurrencyPrice";
import CurrencyHistory from "./data-component/CurrencyHistory";
import { Card } from "./ui/card";

const CurrencyDashboard: React.FC<{ currencyName?: string }> = ({ currencyName }) => {
  return (
    <div>
      {currencyName ? (
        <div className="grid grid-cols-6 grid-rows-5 gap-4">
          <div className="col-span-2 row-span-3">
            <CurrencyDetails currencyName={currencyName} />
          </div>
          <div className="col-span-3 row-span-5 col-start-4">
            <CurrencyHistory currencyName={currencyName} />
          </div>
        </div>
      ) : (
        <p className="text-center text-gray-500">
          Select a cryptocurrency to view its details.
        </p>
      )}

      {/* Render AllCurrentCurrencies outside the grid */}
      <div className="col-span-5 row-span-4">
        <Card className="p-4">
        <AllCurrentCurrencies />
        </Card>
      </div>
    </div>
  );
};

export default CurrencyDashboard;
