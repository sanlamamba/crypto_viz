package org.par23.controllers;

import org.par23.models.Currency;
import org.par23.models.CurrencyData;
import org.par23.models.CurrencyDataHistory;
import org.par23.repositories.CurrencyDataHistoryRepository;
import org.par23.repositories.CurrencyDataRepository;
import org.par23.repositories.CurrencyRepository;

import java.util.List;
import java.util.Optional;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.inject.Inject;

@Path("/http")
public class HttpController {

    @Inject
    private CurrencyRepository currencyRepository;
    @Inject
    private CurrencyDataRepository currencyDataRepository;
    @Inject
    private CurrencyDataHistoryRepository currencyDataHistoryRepository;

    // get endpoint that returns the current data of a currency
    @GET
    @Path("/{currencyName}/current")
    public CurrencyData getCurrentData(String currencyName) {
        Optional<CurrencyData> currencyData = currencyDataRepository.findByCurrencyName(currencyName);
        System.err.println(currencyData.get().getPrice());
        return currencyData.orElse(null);
    }

    // get endpoint that returns the history of a currency
    @GET
    @Path("/{currencyName}/history")
    public List<CurrencyDataHistory> getHistory(String currencyName) {
        Optional<Currency> currency = currencyRepository.findByName(currencyName);
        if (currency.isEmpty()) {
            return null;
        }
        return currencyDataHistoryRepository.findByCurrencyName(currencyName);
    }

    // get endpoint that returns all the currencies
    @GET
    @Path("/currencies")
    public List<Currency> getCurrencies() {
        return currencyRepository.findAll();
    }

    // get endpoint that returns current data of all currencies
    @GET
    @Path("/currencies/current")
    public List<CurrencyData> getCurrentData() {
        return currencyDataRepository.findAll();
    }
}
