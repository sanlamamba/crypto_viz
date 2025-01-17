import { ApiService } from "@/data/apiService";
import { CryptoDataHistory, CurrencyData } from "@/data/interface/coin";
import { useEffect, useState } from "react";

type UseCurrencyDataResult = {
    currentData: CurrencyData | undefined;
    historyData: CryptoDataHistory[] | undefined;
    loading: boolean;
    error: string | null;
};

export const useCurrencyData = (currencyName: string): UseCurrencyDataResult => {
    const [currentData, setCurrentData] = useState<CurrencyData | undefined>();
    const [historyData, setHistoryData] = useState<CryptoDataHistory[] | undefined>();
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchCurrencyData = async () => {
            setLoading(true);
            setError(null);

            try {
                const [current, history] = await Promise.all([
                    ApiService.getCurrentCurrency(currencyName),
                    ApiService.getCurrencyHistory(currencyName),
                ]);

                setCurrentData(current);
                setHistoryData(history);
            } catch (err) {
                if (err instanceof Error) {
                    setError(err.message);
                } else {
                    setError("An unexpected error occurred.");
                }
            } finally {
                setLoading(false);
            }
        };

        if (currencyName) {
            fetchCurrencyData();
        }
    }, [currencyName]);

    return { currentData, historyData, loading, error };
};
