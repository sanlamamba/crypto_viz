import { useEffect, useState } from "react";

type UseFetchDataResult<T> = {
  data: T | null;
  loading: boolean;
  error: string | null;
};

export const useFetchData = <T>(url: string): UseFetchDataResult<T> => {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const controller = new AbortController(); // Create an instance of AbortController
    const signal = controller.signal; // Get the signal from the controller

    const fetchData = async () => {
      setLoading(true);
      setError(null);

      try {
        const response = await fetch(url, { signal }); // Pass the signal to the fetch API
        if (!response.ok) {
          throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const json = (await response.json()) as T;
        setData(json);
      } catch (err) {
        if (err instanceof DOMException && err.name === "AbortError") {
          // Handle the abort error
          console.log("Fetch aborted");
        } else if (err instanceof Error) {
          setError(err.message);
        } else {
          setError("An unexpected error occurred.");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchData();

    // Cleanup function to abort the request when the component unmounts or URL changes
    return () => {
      controller.abort();
    };
  }, [url]); // Dependency array: refetches if the URL changes

  return { data, loading, error };
};
