import {  MergedCryptoData } from "@/data/interface/coin"
import { ColumnDef } from "@tanstack/react-table"



export const columns: ColumnDef<MergedCryptoData>[] = [

  {
    accessorKey: "name",
    header: "Name",
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
