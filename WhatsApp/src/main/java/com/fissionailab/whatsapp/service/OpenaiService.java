package com.jeffrey.linedemo.service;

import com.google.gson.Gson;
import com.jeffrey.linedemo.entity.GreenMessage;
import com.jeffrey.linedemo.entity.OpenAIMessage;
import com.jeffrey.linedemo.utils.GreenApiUtils;
import com.jeffrey.linedemo.utils.SelectCharacterUtils;
import com.jeffrey.linedemo.utils.WebSocketUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;

import java.util.concurrent.ConcurrentHashMap;

@Service
public class OpenaiService {

    @Autowired
    WebSocketUtils webSocketUtils;
    @Autowired
    ConcurrentHashMap<String, WebSocketSession> userSessions;
    @Autowired
    GreenApiUtils greenApiUtils;
    @Autowired
    Gson gson;
    @Autowired
    SelectCharacterUtils selectCharacterUtils;
    @Autowired
    ConcurrentHashMap<String, String> userCharacter;
    public void sendMessage(GreenMessage data) {
        String phone = data.getSenderData().getSender();
        String message = data.getMessageData().getTextMessageData().getTextMessage();
        String chatId = data.getSenderData().getChatId();

        System.out.println("[User]: " + message);
        System.out.print("[AI]: ");

        try {
            selectCharacterUtils.handleRequest(message, phone, chatId);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

}
