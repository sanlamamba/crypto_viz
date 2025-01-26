

import CurrencyDashboard from "./components/currencyDashboard";
import CryptoSelector from "./components/data-component/CryptoSelector";
import { Cryptocurrency } from "./data/interface/coin";
import { useState } from "react";

const App: React.FC = () => {
  const [selectedCrypto, setSelectedCrypto] = useState<Cryptocurrency>()
  const handleCryptoSelect = (cryptocurrency: Cryptocurrency) => {
    console.log("Selected cryptocurrency:", cryptocurrency);
    setSelectedCrypto(cryptocurrency)
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="w-full max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8">
        <h1 className="text-3xl font-bold text-center py-6">Crypto Dashboard</h1>
        <div className="grid grid-cols-6  gap-4">
          <div className="row-span-3">
            <CryptoSelector onSelect={handleCryptoSelect} />
          </div>

          <div className="col-span-5 row-span-6">
            <CurrencyDashboard currencyName={selectedCrypto?.name} />
          </div>
        </div>

      </div>
    </div>
  );
};

export default App;



