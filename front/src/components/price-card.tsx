import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export const PriceCard: React.FC<{
  currencyName?: string;
  currencyPrice?: number;
  currencyMarketCap?: number;
}> = ({ currencyName, currencyPrice, currencyMarketCap }) => {
  return (
    <Card>
      <CardHeader>
        <CardTitle>{currencyName || "Crypto Name"}</CardTitle>
        <CardDescription>
  {currencyPrice && !currencyMarketCap
    ? "Current Crypto Price."
    : !currencyPrice && currencyMarketCap
    ? "Current Market Cap."
    : !currencyPrice && !currencyMarketCap
    ? "No data available."
    : "Current Crypto Price and Market Cap."}
</CardDescription>

      </CardHeader>
      <CardContent className="text-center">
        <h1>
          {currencyPrice
            ? `$${currencyPrice.toFixed(2)}`
            : currencyMarketCap
            ? `$${currencyMarketCap.toFixed(2)}`
            : "--"}
        </h1>
      </CardContent>

    </Card>
  );
};
