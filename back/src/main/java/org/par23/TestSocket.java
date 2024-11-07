package org.par23;

import java.util.HashMap;
import java.util.concurrent.ConcurrentHashMap;

import jakarta.enterprise.context.ApplicationScoped;
import jakarta.websocket.OnClose;
import jakarta.websocket.OnMessage;
import jakarta.websocket.OnOpen;
import jakarta.websocket.server.PathParam;
import jakarta.websocket.server.ServerEndpoint;
import jakarta.websocket.Session;

@ServerEndpoint("/chat/{username}")
@ApplicationScoped
public class TestSocket {
    HashMap<String, Session> sessions = new HashMap<>();
    ConcurrentHashMap<String, String> users = new ConcurrentHashMap<>();

    @OnOpen
    public void onOpen(Session session, @PathParam("username") String username) {
        sessions.put(session.getId(), session);
        users.put(session.getId(), username);
        broadcast("New user connected: " + username);
    }

    @OnClose
    public void onClose(Session session) {
        String username = users.get(session.getId());
        sessions.remove(session.getId());
        users.remove(session.getId());
        broadcast("User disconnected: " + username);
    }

    @OnMessage
    public void onMessage(String message, Session session) {
        String username = users.get(session.getId());
        if (username != null) {
            broadcast(username + ": " + message);
        } else {
            broadcast("Unknown user: " + message);
        }
    }

    private void broadcast(String message) {
        System.out.println("Broadcasting: " + message);
        if (message == null) {
            message = "nullmessage";
            broadcast2(message);
        } else {
            broadcast2(message);
        }
    }

    private void broadcast2(final String message) {
        sessions.values().forEach(s -> s.getAsyncRemote().sendObject(message, result -> {
            if (result.getException() != null) {
                System.out.println("Unable to send message: " + result.getException());
            }
        }));
    }
}