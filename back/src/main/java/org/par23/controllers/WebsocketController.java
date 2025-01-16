package org.par23.controllers;

import java.util.List;
import java.util.stream.Collectors;

import org.par23.models.Currency;
import org.par23.models.CurrencyData;
import org.par23.repositories.CurrencyRepository;

import jakarta.inject.Inject;
import io.quarkus.websockets.next.OnTextMessage;
import io.quarkus.websockets.next.OnClose;
import io.quarkus.websockets.next.OnError;
import io.quarkus.websockets.next.OnOpen;
import io.quarkus.websockets.next.WebSocket;
import io.quarkus.websockets.next.WebSocketConnection;

import com.fasterxml.jackson.databind.ObjectMapper;

@WebSocket(path = "/websocket")
public class WebsocketController {

    @Inject
    WebSocketConnection connection;

    @Inject
    private CurrencyRepository currencyRepository;

    private ObjectMapper objectMapper = new ObjectMapper();

    @OnOpen
    public void onOpen() {
        System.out.println("WebSocket connection opened");
    }

    @OnClose
    public void onClose() {
        System.out.println("WebSocket connection closed");
    }

    @OnError
public void onError(Throwable throwable) {
    System.err.println("WebSocket Error: " + throwable.getMessage());
    throwable.printStackTrace();
}


    @OnTextMessage
    public void onMessage(String message) {
        System.out.println("Received message: " + message);
        try {
            // Check the message type
            if ("getAllCryptos".equalsIgnoreCase(message)) {
                // Retrieve all cryptocurrencies
                List<Currency> currencies = currencyRepository.findAll();
                
                // Convert the list to JSON
                String jsonResponse = objectMapper.writeValueAsString(currencies);
                
                // Send the response back to the client
                connection.sendText(jsonResponse);
            } else {
                connection.sendText("Unknown command: " + message);
            }
        } catch (Exception e) {
            e.printStackTrace();
            try {
                connection.sendText("Error processing message: " + e.getMessage());
            } catch (Exception sendError) {
                sendError.printStackTrace();
            }
        }
    }
}
