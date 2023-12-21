package com.fissionailab.line.utils;

import com.fissionailab.line.entity.OpenAIMessage;
import com.google.gson.Gson;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.util.concurrent.ConcurrentHashMap;

@Component
public class SelectCharacterUtils {
    @Autowired
    ConcurrentHashMap<String, String> characterList;
    @Autowired
    ConcurrentHashMap<String, WebSocketSession> userSessions;
    @Autowired
    WebSocketUtils webSocketUtils;
    @Autowired
    Gson gson;
    public void handleRequest(String message, String userId, String replyToken) throws Exception {
        WebSocketSession session = webSocketUtils.createSessionIfNotExist(userId, replyToken);

        if (message.startsWith("[day")) {
            selectCharacter(message, userId, session);
            return;
        }
        characterList.putIfAbsent(userId, "default_character");
        sendMessage(message, userId, session);
    }

    private void selectCharacter(String message, String userId, WebSocketSession session) throws Exception {
        String number = message.substring(4,6);
        String character = "DemoDay" + number;

        characterList.put(userId, character);
        String jsonMessage = gson.toJson(new OpenAIMessage("", character,"delete_history"));
        TextMessage aiMessage = new TextMessage(jsonMessage);
        session.sendMessage(aiMessage);
    }

    private void sendMessage(String message, String userId, WebSocketSession session) throws Exception {
        String jsonMessage = gson.toJson(new OpenAIMessage(message, characterList.get(userId), "Chat" ));
        TextMessage aiMessage = new TextMessage(jsonMessage);
        session.sendMessage(aiMessage);
    }
}

