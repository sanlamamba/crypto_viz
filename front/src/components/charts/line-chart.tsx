import React, { useState } from "react";
import { TrendingUp } from "lucide-react";
import {
  CartesianGrid,
  Line,
  LineChart,
  XAxis,
  AreaChart,
  Area,
} from "recharts";

import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  ChartConfig,
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from "@/components/ui/chart";
import { CryptoDataHistory } from "@/data/interface/coin";

interface LineChartComponentProps {
  currencyHistoryData: CryptoDataHistory[] | null;
  currencyName: string;
}

export const LineChartComponent: React.FC<LineChartComponentProps> = ({
  currencyHistoryData,
  currencyName,
}) => {
  const [timeRange, setTimeRange] = useState<"minutes" | "days" | "months">(
    "minutes"
  );
  const [dataType, setDataType] = useState<"price" | "marketCap">("price"); // Filtre entre price et marketCap

  if (!currencyHistoryData || currencyHistoryData.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Cryptocurrency History</CardTitle>
          <CardDescription>No data available for this cryptocurrency.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  // Filtrer les données en fonction du timeRange
  const filterDataByTimeRange = () => {
    switch (timeRange) {
      case "minutes":
        { const now = new Date();
        const twentyFourHoursAgo = new Date(now.getTime() - 24 * 60 * 60 * 1000);

        return currencyHistoryData
          .filter(
            (entry) =>
              new Date(entry.timestamp) >= twentyFourHoursAgo &&
              new Date(entry.timestamp) <= now
          )
          .map((entry) => ({
            time: new Date(entry.timestamp).toLocaleTimeString("en-US", {
              hour: "2-digit",
              minute: "2-digit",
            }),
            value: dataType === "price" ? entry.price : entry.marketCap,
          })); }

      case "days":
        { const daysMap = new Map<string, CryptoDataHistory>();
        currencyHistoryData.forEach((entry) => {
          const day = new Date(entry.timestamp).toISOString().split("T")[0];
          if (!daysMap.has(day)) {
            daysMap.set(day, entry); // Ajouter la première entrée du jour
          }
        });
        return Array.from(daysMap.values()).map((entry) => ({
          time: new Date(entry.timestamp).toLocaleDateString("en-US", {
            month: "short",
            day: "2-digit",
          }),
          value: dataType === "price" ? entry.price : entry.marketCap,
        })); }

      case "months":
        { const monthsMap = new Map<string, CryptoDataHistory>();
        currencyHistoryData.forEach((entry) => {
          const month = new Date(entry.timestamp).toISOString().slice(0, 7); // Format YYYY-MM
          if (!monthsMap.has(month)) {
            monthsMap.set(month, entry); // Ajouter la première entrée du mois
          }
        });
        return Array.from(monthsMap.values()).map((entry) => ({
          time: new Date(entry.timestamp).toLocaleDateString("en-US", {
            month: "short",
          }),
          value: dataType === "price" ? entry.price : entry.marketCap,
        })); }

      default:
        return [];
    }
  };

  const chartData = filterDataByTimeRange();

  const chartConfig = {
    [currencyName]: {
      label: currencyName,
      color: "hsl(var(--chart-1))",
    },
  } satisfies ChartConfig;

  return (
    <Card className="">
      <CardHeader>
        <CardTitle>{currencyName}</CardTitle>
        <CardDescription>Time series</CardDescription>
      </CardHeader>
      <CardContent>
        {/* Time Range Filter */}
        <div className="flex gap-4 mb-4">
          {["minutes", "days", "months"].map((range) => (
            <button
              key={range}
              onClick={() => setTimeRange(range as "minutes" | "days" | "months")}
              className={`px-4 py-2 rounded ${
                timeRange === range ? "bg-blue-500 text-white" : "bg-gray-200"
              }`}
            >
              {range.charAt(0).toUpperCase() + range.slice(1)}
            </button>
          ))}
        </div>

        {/* Data Type Filter */}
        <div className="flex gap-4 mb-4">
          {["price", "marketCap"].map((type) => (
            <button
              key={type}
              onClick={() => setDataType(type as "price" | "marketCap")}
              className={`px-4 py-2 rounded ${
                dataType === type ? "bg-blue-500 text-white" : "bg-gray-200"
              }`}
            >
              {type.charAt(0).toUpperCase() + type.slice(1)}
            </button>
          ))}
        </div>

        {/* Chart Configuration */}
        <ChartContainer config={chartConfig}>
          {dataType === "price" ? (
            <AreaChart
              width={600}
              height={300}
              data={chartData}
              margin={{
                top: 5,
                right: 20,
                left: 10,
                bottom: 5,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="time"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(value) => value}
              />
              <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
              <Area
                type="monotone"
                dataKey="value"
                stroke="#1E88E5"
                fill="#1E88E5"
                strokeWidth={2}
              />
            </AreaChart>
          ) : (
            <LineChart
              width={600}
              height={300}
              data={chartData}
              margin={{
                top: 5,
                right: 20,
                left: 10,
                bottom: 5,
              }}
            >
              <CartesianGrid vertical={false} />
              <XAxis
                dataKey="time"
                tickLine={false}
                axisLine={false}
                tickMargin={8}
                tickFormatter={(value) => value}
              />
              <ChartTooltip cursor={false} content={<ChartTooltipContent />} />
              <Line
                dataKey="value"
                type="monotone"
                stroke="#4CAF50"
                strokeWidth={2}
                dot={false}
              />
            </LineChart>
          )}
        </ChartContainer>
      </CardContent>
      <CardFooter>
        <div className="flex w-full items-start gap-2 text-sm">
          <div className="grid gap-2">
            <div className="flex items-center gap-2 font-medium leading-none">
              Trending up by 5.2% this month <TrendingUp className="h-4 w-4" />
            </div>
            <div className="flex items-center gap-2 leading-none text-muted-foreground">
              Showing {dataType} history based on the selected time range.
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
};
