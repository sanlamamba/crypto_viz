
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"


export const PriceCard = () => {
  return (
    <Card className="w-[350px]">
      <CardHeader>
        <CardTitle>Crypto Name</CardTitle>
        <CardDescription>Current Crypto Price.</CardDescription>
      </CardHeader>
      <CardContent className="text-center">
        <h1>$-- </h1>
      </CardContent>
      <CardFooter className="flex justify-between">
        + --%(24h)
      </CardFooter>
    </Card>
  )
}
