import React from "react";
import { Chart } from "react-google-charts";

interface ChartComponentProps {
  chartType: "LineChart" | "BarChart" | "PieChart" | "CandlestickChart";
  data: any[];
  options?: object;
}

const ChartComponent: React.FC<ChartComponentProps> = ({
  chartType,
  data,
  options,
}) => {
  return (
    
    <Chart
      chartType={chartType}
      width="100%"
      height="400px"
      data={data}
      options={options}
    />
  );
};

export default ChartComponent;
