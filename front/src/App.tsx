import React, { useState } from "react";
import { cryptocurrencies, currency_data } from "./data/data.json";
import { mergeCryptocurrencyData } from "./data/utils/mergeData";
import DataSelector from "./components/data-selector";
import ChartComponent from "./components/chart-component";
import { BarChartComponent } from "./components/charts/bar-chart";
import { PriceCard } from "./components/price-card";
import { RadialChartText } from "./components/radial-chart-text";
import { LineChartComponent } from "./components/charts/line-chart";
const App: React.FC = () => {
  const mergedData = mergeCryptocurrencyData(cryptocurrencies, currency_data);

  const availableDataSources = cryptocurrencies.map((crypto) => crypto.name);

  const [views, setViews] = useState<
    {
      id: number;
      chartType: "LineChart" | "BarChart" | "PieChart" | "CandlestickChart";
      dataSource: string;
    }[]
  >([]);

  const handleAddView = (
    chartType: "LineChart" | "BarChart" | "PieChart" | "CandlestickChart",
    dataSource: string
  ) => {
    const id = new Date().getTime();
    setViews([...views, { id, chartType, dataSource }]);
  };

  const getDataForSource = (source: string) => {
    const crypto = mergedData.find((c) => c.name === source);
    if (!crypto) return [];

    const data = mergedData.filter((d) => d.id === crypto.id);
    return [
      ["Date", "Open", "High", "Low", "Close"],
      ...data.map((d) => [d.updated_at, d.price, d.price + 1000, d.price - 1000, d.price]),
    ];
  };

  return (
    <div className="App">
      <h1 className="text-3xl font-bold text-center py-6">Crypto Dashboard</h1>

      <DataSelector
        onAdd={handleAddView}
        availableDataSources={availableDataSources}
      />

<div className="mt-6 grid grid-cols-1 md:grid-cols-2 gap-4">
{views.map((view) => (
          <div key={view.id} className="grid-cols-4 ">
          <ChartComponent
            key={view.id}
            chartType={view.chartType}
            data={getDataForSource(view.dataSource)}
            options={{ title: view.dataSource }}
          />
          </div>
        ))}
<PriceCard />
<PriceCard />
<BarChartComponent />
<LineChartComponent />
<RadialChartText />

      </div>
    </div>
  );
};

export default App;
