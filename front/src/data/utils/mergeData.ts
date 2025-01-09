import { Cryptocurrency, CurrencyData, MergedCryptoData } from "../interface/coin";

 export function mergeCryptocurrencyData(
    cryptocurrencies: Cryptocurrency[],
    currencyData: CurrencyData[]
  ): MergedCryptoData[] {
    return cryptocurrencies.map((crypto) => {
      const currencyInfo = currencyData.find(
        (data) => data.currency_id === crypto.id
      );
  
      return {
        id: crypto.id,
        name: crypto.name,
        symbol: crypto.symbol,
        price: currencyInfo?.price || 0,
        market_cap: currencyInfo?.market_cap || 0,
        updated_at: currencyInfo?.updated_at || '',
        source: currencyInfo?.source || '',
        trust_factor: currencyInfo?.trust_factor || 0
      };
    });
}