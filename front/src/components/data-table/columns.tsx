import {  MergedCryptoData } from "@/data/interface/coin"
import { ColumnDef } from "@tanstack/react-table"
import { ArrowUpDown } from "lucide-react"
import { Button } from "../ui/button"
  

export const columns: ColumnDef<MergedCryptoData>[] = [

  {
    
    accessorKey: "name",
    header: ({ column }) => {
      return (
        <Button
        variant="outline"
          onClick={() => column.toggleSorting(column.getIsSorted() === "asc")}
        >
          Name
          <ArrowUpDown className="ml-2 h-4 w-4" />
        </Button>
      )
    },
  },
  {
    accessorKey: "symbol",
    header: "Symbol",
  },
  {
    accessorKey: "price",
    header: "Price",
  },
  {
    accessorKey: "market_cap",
    header: "Market Cap",
  },
  {
    accessorKey: "updated_at",
    header: "Updated",
  },
  {
    accessorKey: "source",
    header: "Source",
  },
  {
    accessorKey: "trust_factor",
    header: "Trust Factor",
  },
]
