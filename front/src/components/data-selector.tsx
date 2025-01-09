import React, { useState } from "react";

interface DataSelectorProps {
  onAdd: (
    chartType: "LineChart" | "BarChart" | "PieChart" | "CandlestickChart",
    dataSource: string
  ) => void;
  availableDataSources: string[];
}

const DataSelector: React.FC<DataSelectorProps> = ({
  onAdd,
  availableDataSources,
}) => {
  const [selectedChartType, setSelectedChartType] = useState<
    "LineChart" | "BarChart" | "PieChart" | "CandlestickChart"
  >("LineChart");
  const [selectedDataSource, setSelectedDataSource] = useState("");

  const handleAdd = () => {
    if (selectedDataSource) {
      onAdd(selectedChartType, selectedDataSource);
    }
  };

  return (
    <div className="data-selector">
      <select
        value={selectedDataSource}
        onChange={(e) => setSelectedDataSource(e.target.value)}
        className="border p-2 rounded mr-4"
      >
        <option value="" disabled>
          Select Data Source
        </option>
        {availableDataSources.map((source) => (
          <option key={source} value={source}>
            {source}
          </option>
        ))}
      </select>

      <select
        value={selectedChartType}
        onChange={(e) => setSelectedChartType(e.target.value as any)}
        className="border p-2 rounded mr-4"
      >
        <option value="LineChart">Line Chart</option>
        <option value="BarChart">Bar Chart</option>
        <option value="PieChart">Pie Chart</option>
        <option value="CandlestickChart">Candlestick Chart</option>
      </select>

      <button
        onClick={handleAdd}
        className="bg-blue-500 text-white p-2 rounded"
      >
        Add to Dashboard
      </button>
    </div>
  );
};

export default DataSelector;
