import React from "react";
import { ApiService } from "@/data/apiService";
import { DataTable } from "@/components/data-table/data-table"; // Assuming you have a reusable DataTable component
import { mergeCryptocurrencyData } from "@/data/utils/mergeData";

const AllCurrentCurrencies: React.FC = () => {
  const { data: allCurrenciesData, loading: allLoading, error: allError } =
    ApiService.useCurrencies(); // Fetch the list of all cryptocurrencies

  const {
    data: currentCurrenciesData,
    loading: currentLoading,
    error: currentError,
  } = ApiService.useAllCurrentCurrencies(); // Fetch current prices for cryptocurrencies

  if (allLoading || currentLoading) return <p>Loading...</p>;
  if (allError || currentError)
    return <p>Error: {allError || currentError}</p>;

  // Merge the data
  const mergedData = mergeCryptocurrencyData(
    allCurrenciesData || [],
    currentCurrenciesData || []
  );

  const columns = [
    {
      accessorKey: "name",
      header: "Name",
    },
    {
      accessorKey: "price",
      header: "Price (USD)",
    },
    {
      accessorKey: "marketCap",
      header: "Market Cap (USD)",
    },
    {
      accessorKey: "source",
      header: "Source",
    },
    {
      accessorKey: "trust_factor",
      header: "Trust Factor",
    },
  ];

  return (
    <div>
      <h2 className="text-2xl font-bold mb-4">All Current Cryptocurrencies</h2>
      <DataTable columns={columns} data={mergedData} />
    </div>
  );
};

export default AllCurrentCurrencies;
