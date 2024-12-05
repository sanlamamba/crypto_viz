package org.par23.controllers;

import java.util.Optional;

import org.par23.models.CurrencyData;
import org.par23.repositories.CurrencyDataHistoryRepository;
import org.par23.repositories.CurrencyDataRepository;
import org.par23.repositories.CurrencyRepository;

import jakarta.inject.Inject;
import io.quarkus.websockets.next.OnTextMessage;
import io.quarkus.websockets.next.OnClose;
import io.quarkus.websockets.next.OnOpen;
import io.quarkus.websockets.next.WebSocket;
import io.quarkus.websockets.next.WebSocketConnection;

@WebSocket(path = "/websocket")
public class WebsocketController {

    @Inject
    WebSocketConnection connection;

    @Inject
    private CurrencyRepository currencyRepository;

    @Inject
    private CurrencyDataRepository currencyDataRepository;

    @Inject
    private CurrencyDataHistoryRepository currencyDataHistoryRepository;

    @OnOpen
    public void onOpen() {
        System.out.println("WebSocket connection opened");

    }

    @OnClose
    public void onClose() {
        System.out.println("WebSocket connection closed");
    }

    @OnTextMessage
    public Double getCurrentData(String currencyName) {
        System.out.println("Received message: " + currencyName);
        try {
            Optional<CurrencyData> currencyData = currencyDataRepository.findByCurrencyName(currencyName);
            if (currencyData.isPresent()) {
                // System.err.println("price : " + currencyData.get().getPrice());
                return currencyData.get().getPrice();
            } else {
                System.err.println("Currency data not found for: " + currencyName);
                return null;
            }
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
