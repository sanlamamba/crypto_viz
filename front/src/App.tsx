import React, { useState, useEffect, useCallback } from "react";
import { cryptocurrencies } from "./data/data.json";
import DataSelector from "./components/data-selector";
import { BarChartComponent } from "./components/charts/bar-chart";
import { PriceCard } from "./components/price-card";
import { RadialChartText } from "./components/radial-chart-text";
import { LineChartComponent } from "./components/charts/line-chart";

import CurrencyDashboard from "./components/currencyDashboard";

const App: React.FC = () => {

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
      <CurrencyDashboard currencyName={"Bitcoin"} />
      <DataSelector
        onAdd={handleAddView}
        availableDataSources={availableDataSources}
      />

      <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
        <div className="grid auto-rows-min gap-4 md:grid-cols-3">
          {views.map((view) => (
            <div key={view.id} className="grid-cols-4">
              <button
                className="mt-2 p-2 bg-blue-500 text-white rounded"
                onClick={() => requestWebSocketData(view.dataSource)}
              >
                Fetch Real-time Data
              </button>
            </div>
          ))}
          <PriceCard />
          <PriceCard />
          <RadialChartText />
          <BarChartComponent />
          <LineChartComponent />
        </div>
        
      </div>
      
    </div>
  );
};

export default App;
