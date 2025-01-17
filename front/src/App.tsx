import React, { useState, useEffect, useCallback } from "react";
import { cryptocurrencies, currency_data } from "./data/data.json";
import { mergeCryptocurrencyData } from "./data/utils/mergeData";
import DataSelector from "./components/data-selector";
import ChartComponent from "./components/chart-component";
import { BarChartComponent } from "./components/charts/bar-chart";
import { PriceCard } from "./components/price-card";
import { RadialChartText } from "./components/radial-chart-text";
import { LineChartComponent } from "./components/charts/line-chart";
import { DataTable } from "./components/data-table/data-table";
import { columns } from "./components/data-table/columns";
import CurrencyDashboard from "./components/currencyDashboard";

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

  const [websocketData, setWebsocketData] = useState<{
    [key: string]: number | null;
  }>({});

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

  // WebSocket Connection
  useEffect(() => {
    const websocket = new WebSocket("ws://localhost:8080/websocket");

    websocket.onopen = () => {
      console.log("WebSocket connection opened");
    };

    websocket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data); // Assuming the server sends JSON data
        console.log("WebSocket message received:", data);

        // Update the state with real-time data
        if (data.currencyName && data.price) {
          setWebsocketData((prevData) => ({
            ...prevData,
            [data.currencyName]: data.price,
          }));
        }
      } catch (error) {
        console.error("Error parsing WebSocket message:", error);
      }
    };

    websocket.onclose = () => {
      console.log("WebSocket connection closed");
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };

    return () => {
      websocket.close(); // Clean up on component unmount
    };
  }, []);

  const requestWebSocketData = useCallback(
    (currencyName: string) => {
      const websocket = new WebSocket("ws://localhost:8080/websocket");

      websocket.onopen = () => {
        websocket.send(currencyName); // Send the currency name to request data
        console.log("Requested WebSocket data for:", currencyName);
      };

      websocket.onmessage = (event) => {
        const price = parseFloat(event.data);
        if (!isNaN(price)) {
          setWebsocketData((prevData) => ({
            ...prevData,
            [currencyName]: price,
          }));
        }
        websocket.close(); // Close after receiving the response
      };

      websocket.onerror = (error) => {
        console.error("WebSocket error during request:", error);
      };
    },
    []
  );

  return (
    <div className="App">
      <h1 className="text-3xl font-bold text-center py-6">Crypto Dashboard</h1>

      <DataSelector
        onAdd={handleAddView}
        availableDataSources={availableDataSources}
      />

      <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
          {views.map((view) => (
            <div key={view.id} className="grid-cols-4">
              <ChartComponent
                key={view.id}
                chartType={view.chartType}
                data={getDataForSource(view.dataSource)}
                options={{
                  title: view.dataSource,
                  subtitle: `Real-time price: ${
                    websocketData[view.dataSource] !== undefined
                      ? `$${websocketData[view.dataSource]}`
                      : "Fetching..."
                  }`,
                }}
              />
              <button
                className="mt-2 p-2 bg-blue-500 text-white rounded"
                onClick={() => requestWebSocketData(view.dataSource)}
              >
                Fetch Real-time Data
              </button>
            </div>
          ))}
          <DataTable columns={columns} data={mergedData} />
          <PriceCard />
          <PriceCard />
          <RadialChartText />
          <BarChartComponent />
          <LineChartComponent />
        </div>
        <CurrencyDashboard currencyName={"Bitcoin"} />
      </div>
    </div>
  );
};

export default App;
