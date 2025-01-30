import CurrencyDashboard from "./components/currencyDashboard";
import CryptoSelector from "./components/data-component/CryptoSelector";
import { Cryptocurrency } from "./data/interface/coin";
import { useState, useEffect } from "react";
import { Moon, Sun } from "lucide-react";

const App: React.FC = () => {
  const [selectedCrypto, setSelectedCrypto] = useState<Cryptocurrency>();
  const [darkMode, setDarkMode] = useState<boolean>(false);

  useEffect(() => {
    const storedTheme = localStorage.getItem("theme");
    if (storedTheme === "dark") {
      setDarkMode(true);
      document.documentElement.classList.add("dark");
    }
  }, []);

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    if (!darkMode) {
      document.documentElement.classList.add("dark");
      localStorage.setItem("theme", "dark");
    } else {
      document.documentElement.classList.remove("dark");
      localStorage.setItem("theme", "light");
    }
  };

  const handleCryptoSelect = (cryptocurrency: Cryptocurrency) => {
    console.log("Selected cryptocurrency:", cryptocurrency);
    setSelectedCrypto(cryptocurrency);
  };

  return (
      <div className="h-screen transition-all duration-500 bg-gray-100 dark:bg-gray-900 relative">
        <div className="absolute top-[0%] right-0 w-full md:w-1/2 h-full bg-gradient-to-br from-green-700 via-green-600 to-green-400 opacity-40 blur-[80px] transform translate-x-[10%]" />
        <div className="w-full max-w-[1920px] mx-auto px-4 sm:px-6 lg:px-8 relative z-10 pt-10 ">
          <div className="flex justify-between items-center py-6  pl-10 pr-10">
            <h1 className="text-3xl font-bold text-center text-gray-900 dark:text-gray-100">Crypto Dashboard</h1>
            <button
                onClick={toggleDarkMode}
                className=" rounded-full bg-gray-200 dark:bg-gray-800 hover:scale-110 transition"
            >
              {darkMode ? <Sun className="text-yellow-400" /> : <Moon className="text-gray-700" />}
            </button>
          </div>

          <div className="flex w-screen justify-center gap-10  p-10 ">

            <div className="w-72 row-span-3 p-4  dark:bg-gray-800 shadow-lg rounded-2xl backdrop-blur-md bg-opacity-80 dark:bg-opacity-50">
              <CryptoSelector onSelect={handleCryptoSelect} />
            </div>

            <div className="w-full col-span-5 row-span-6 p-6 bg-white dark:bg-gray-800 shadow-lg rounded-2xl backdrop-blur-md bg-opacity-40 dark:bg-opacity-50">
              <CurrencyDashboard currencyName={selectedCrypto?.name} />
            </div>
          </div>
        </div>
      </div>
  );
};

export default App;
