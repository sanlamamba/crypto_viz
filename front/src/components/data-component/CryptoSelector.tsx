import React, { useState, useRef } from "react";
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

  const scrollContainerRef = useRef<HTMLDivElement>(null);

  const handleSelect = (crypto: { id: string; name: string; symbol: string }) => {
    setSelectedCrypto(crypto.id);
    onSelect(crypto);
  };

  const handleScroll = (direction: "left" | "right") => {
    if (scrollContainerRef.current) {
      const scrollAmount = 200; // Adjust the scroll amount as needed
      scrollContainerRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  const filteredCryptos = cryptos?.filter((crypto: Cryptocurrency) =>
    crypto.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <Card className="p-4 w-full max-w-lg">
      <CardHeader>
        <CardTitle>Select a Cryptocurrency</CardTitle>
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
          <div className="flex items-center gap-2">
            {/* Left Arrow */}
            <button
              onClick={() => handleScroll("left")}
              className="bg-gray-200 rounded-full p-2 shadow-md hover:bg-gray-300"
            >
              ←
            </button>

            {/* Badge Container */}
            <div
              ref={scrollContainerRef}
              className="flex gap-2 overflow-x-auto no-scrollbar"
            >
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

            {/* Right Arrow */}
            <button
              onClick={() => handleScroll("right")}
              className="bg-gray-200 rounded-full p-2 shadow-md hover:bg-gray-300"
            >
              →
            </button>
          </div>
        )}
      </CardContent>
    </Card>
  );
};

export default CryptoSelector;
