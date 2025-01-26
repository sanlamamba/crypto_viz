import React, { useState } from "react";
import { TrendingUp } from "lucide-react";
import { CartesianGrid, Line, LineChart, XAxis } from "recharts";

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

  if (!currencyHistoryData || currencyHistoryData.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Cryptocurrency Price History</CardTitle>
          <CardDescription>No data available for this cryptocurrency.</CardDescription>
        </CardHeader>
      </Card>
    );
  }

  // Filtrer les données en fonction du timeRange
  const filterDataByTimeRange = () => {
    switch (timeRange) {
      case "minutes":
        // Filtrer uniquement les points des dernières 24 heures
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
            price: entry.price,
          })); }
      
      case "days":
        // Grouper les données par jour (une donnée par jour)
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
          price: entry.price,
        })); }

      case "months":
        // Grouper les données par mois (une donnée par mois)
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
          price: entry.price,
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

        <ChartContainer config={chartConfig}>
          <LineChart
            accessibilityLayer
            data={chartData}
            margin={{
              left: 12,
              right: 12,
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
              dataKey="price"
              type="monotone"
              stroke="#1E88E5"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ChartContainer>
      </CardContent>
      <CardFooter>
        <div className="flex w-full items-start gap-2 text-sm">
          <div className="grid gap-2">
            <div className="flex items-center gap-2 font-medium leading-none">
              Trending up by 5.2% this month <TrendingUp className="h-4 w-4" />
            </div>
            <div className="flex items-center gap-2 leading-none text-muted-foreground">
              Showing price history based on the selected time range.
            </div>
          </div>
        </div>
      </CardFooter>
    </Card>
  );
};
