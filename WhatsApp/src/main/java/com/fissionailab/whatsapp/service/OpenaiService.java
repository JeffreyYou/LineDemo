package com.fissionailab.whatsapp.service;

import com.fissionailab.whatsapp.utils.SelectCharacterUtils;
import com.google.gson.Gson;
import com.fissionailab.whatsapp.entity.GreenMessage;
import com.fissionailab.whatsapp.utils.GreenApiUtils;
import com.fissionailab.whatsapp.utils.WebSocketUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
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
        try{
            String phone = data.getSenderData().getSender();
            String message;
            if (data.getMessageData().getTextMessageData() == null) {
                message = data.getMessageData().getFileMessageData().getDownloadUrl();
                System.out.println("[User]: send a image: " + data.getMessageData().getFileMessageData().getDownloadUrl());

            } else {
                message = data.getMessageData().getTextMessageData().getTextMessage();
                System.out.println("[User]: " + message);
                System.out.print("[AI]: ");
            }
            String chatId = data.getSenderData().getChatId();

            selectCharacterUtils.handleRequest(message, phone, chatId);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

}
