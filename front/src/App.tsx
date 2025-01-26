
import { BarChartComponent } from "./components/charts/bar-chart";
import { PriceCard } from "./components/price-card";
import { RadialChartText } from "./components/radial-chart-text";
import { LineChartComponent } from "./components/charts/line-chart";

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

        {/* Grille Responsive */}
        <div className="grid gap-4 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6">
          <div className="rounded-xl bg-muted/50 col-span-3 ">
          <div className="grid grid-rows-1 gap-4">
          <PriceCard />
          <PriceCard />
          </div>
          </div>

          <div className=" aspect-video rounded-xl bg-muted/50 col-span-3  col-start-4">
          <CryptoSelector onSelect={handleCryptoSelect} />   
          <RadialChartText />
           </div>
          <div className="  w-full aspect-video rounded-xl bg-muted/50 col-span-3 row-span-2 row-start-2">
          <BarChartComponent />
          </div>
          <div className="  w-full aspect-video rounded-xl bg-muted/50 col-span-3 row-span-2 col-start-4 row-start-2">
          <LineChartComponent />
          </div>
          <div className="rounded-xl bg-muted/50 md:min-h-min col-span-6 row-span-6 row-start-4">
          <CurrencyDashboard currencyName={selectedCrypto?.name} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;



