import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input"; // Import your Input component
import { ApiService } from "@/data/apiService";
import { Cryptocurrency } from "@/data/interface/coin";

interface CryptoSelectorProps {
  onSelect: (crypto: { id: string; name: string; symbol: string }) => void;
}

const CryptoSelector: React.FC<CryptoSelectorProps> = ({ onSelect }) => {
  const [selectedCrypto, setSelectedCrypto] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState<string>("");

  // Fetch cryptocurrencies using ApiService
  const { data: cryptos, loading, error } = ApiService.useCurrencies();

  const handleSelect = (crypto: { id: string; name: string; symbol: string }) => {
    setSelectedCrypto(crypto.id);
    onSelect(crypto);
  };

  const filteredCryptos = cryptos?.filter((crypto: Cryptocurrency) =>
    crypto.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Card className="w-full max-w-lg">
      <CardHeader className={'bg-none'}>
        <CardTitle className={'mb-4'} >Select a Cryptocurrency</CardTitle>
        <Input
          placeholder="Search Cryptocurrency..."
          value={searchQuery}
          onChange={(e: { target: { value: React.SetStateAction<string>; }; }) => setSearchQuery(e.target.value)}
          className="mt-2"
        />
      </CardHeader>
      <CardContent>
        {loading && <p>Loading...</p>}
        {error && <p className="text-red-500">Error: {error}</p>}
        {!loading && !error && (
          <div className="flex flex-col items-start gap-2 max-h-64 overflow-y-auto">
            {filteredCryptos?.map((crypto: Cryptocurrency) => (
              <Badge
                key={crypto.id}
                onClick={() => handleSelect(crypto)}
                className={`cursor-pointer ${
                  selectedCrypto === crypto.id ? "bg-blue-500 text-white" : ""
                }`}
              >
                {crypto.name}
              </Badge>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default CryptoSelector;
