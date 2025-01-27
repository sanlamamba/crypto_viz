import { useEffect, useState } from "react";

type UseFetchDataResult<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
};

export const useFetchData = <T>(url: string, refreshIntervalMs: number): UseFetchDataResult<T> => {
  const [data, setData] = useState<T | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true); // First-time loading indicator

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;

    const fetchData = async (isSilent: boolean = false) => {
      if (!isSilent) setLoading(true); // Show loading state only on the first fetch
      setError(null);

      try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const json = (await response.json()) as T;
        setData(json);
        console.log("Fetched data:", json);
      } catch (err) {
        if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred.");
        }
      } finally {
        if (!isSilent) setLoading(false);
      }
    };

    fetchData(); // Initial fetch (visible loading)
    if (refreshIntervalMs) {
      interval = setInterval(() => fetchData(true), refreshIntervalMs); // Silent updates
    }

    return () => {
      if (interval) {
        clearInterval(interval);
      }
    };
  }, [url, refreshIntervalMs]); // Dependency array: refetches if the URL or interval changes

  return { data, loading, error };
};
