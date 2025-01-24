
// import AllCurrencies from "./data-component/allCurrencies";
import AllCurrentCurrencies from "./data-component/allCurrentCurrencies";
import CurrencyDetails from "./data-component/currentCurrency";
import CurrencyHistory from "./data-component/CurrencyHistory";

const CurrencyDashboard: React.FC<{ currencyName: string }> = () => {
  

  return (
    <div>
      <h1>Cryptocurrency Dashboard</h1>
      {/* <AllCurrencies /> */}
      <AllCurrentCurrencies />
      <CurrencyDetails currencyName="Bitcoin" />
      <CurrencyHistory currencyName="Bitcoin" />
    </div>
  );
};

export default CurrencyDashboard;
