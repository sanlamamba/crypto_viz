import { Cryptocurrency, CurrencyData, MergedCryptoData } from "../interface/coin";

 export function mergeCryptocurrencyData(
    cryptocurrencies: Cryptocurrency[],
    currencyData: CurrencyData[]
  ): MergedCryptoData[] {
    return cryptocurrencies.map((crypto) => {
      const currencyInfo = currencyData.find(
        (data) => data.currencyId === crypto.id
      );
  
      return {
        id: crypto.id,
        name: crypto.name,
        symbol: crypto.symbol,
        price: currencyInfo?.price || 0,
        marketCap: currencyInfo?.marketCap || 0,
        updated_at: currencyInfo?.updated_at || '',
        source: currencyInfo?.source || '',
        trustFactor: currencyInfo?.trustFactor || 0
      };
    });
}