package com.jeffrey.linedemo.utils;

import com.google.gson.Gson;
import com.jeffrey.linedemo.entity.OpenAIMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.util.concurrent.ConcurrentHashMap;

@Component
public class SelectCharacterUtils {
    @Autowired
    ConcurrentHashMap<String, String> userCharacter;
    @Autowired
    ConcurrentHashMap<String, WebSocketSession> userSessions;
    @Autowired
    WebSocketUtils webSocketUtils;
    @Autowired
    Gson gson;
    public void handleRequest(String message, String phone, String chatId) throws Exception {
        WebSocketSession session = webSocketUtils.createSessionIfNotExist(phone, chatId);

        if (message.startsWith("[day")) {
            selectCharacter(message, phone, session);
        }
        userCharacter.putIfAbsent(phone, "default_character");
        sendMessage(message, phone, session);
    }

    private void selectCharacter(String message, String phone, WebSocketSession session) throws Exception {
        String number = message.substring(4,6);
        String character = "DemoDay" + number;

        userCharacter.put(phone, character);
        String jsonMessage = gson.toJson(new OpenAIMessage("", character,"delete_history"));
        TextMessage aiMessage = new TextMessage(jsonMessage);
        session.sendMessage(aiMessage);
    }

    private void sendMessage(String message, String phone, WebSocketSession session) throws Exception {
        String jsonMessage = gson.toJson(new OpenAIMessage(message, userCharacter.get(phone), "Chat" ));
        TextMessage aiMessage = new TextMessage(jsonMessage);
        session.sendMessage(aiMessage);
    }
}

