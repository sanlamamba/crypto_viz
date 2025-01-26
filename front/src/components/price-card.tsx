import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";

export const PriceCard: React.FC<{
  currencyName?: string;
  currencyPrice?: number;
  currencyMarketCap?: string;
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
            ? `$${currencyPrice}`
            : currencyMarketCap
            ? `$${currencyMarketCap}`
            : "--"}
        </h1>
      </CardContent>
      <CardFooter className="flex justify-between">
        {currencyPrice && (
          <div className="flex items-center gap-2 font-medium leading-none">
            + --%(24h)
          </div>
        )}
      </CardFooter>
    </Card>
  );
};
