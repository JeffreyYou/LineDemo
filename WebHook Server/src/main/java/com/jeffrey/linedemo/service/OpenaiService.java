package com.jeffrey.linedemo.service;

import com.google.gson.Gson;
import com.jeffrey.linedemo.entity.GreenMessage;
import com.jeffrey.linedemo.entity.OpenAIMessage;
import com.jeffrey.linedemo.utils.GreenApiUtils;
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
    public void sendMessage(GreenMessage data) {
        String phone = data.getSenderData().getSender();
        String message = data.getMessageData().getTextMessageData().getTextMessage();
        String chatId = data.getSenderData().getChatId();
        handleRequest(phone, message, chatId);
    }


    public void handleRequest(String phone, String message, String chatId) {
        try {
            System.out.println("[User]: " + message);
            System.out.print("[AI]: ");
            WebSocketSession session = webSocketUtils.createSessionIfNotExist(phone, chatId);

            if (message.startsWith("[Day")) {
                if (message.equals("[Day1]")) {
                    greenApiUtils.sendMessageToUser("謝謝你的聯繫,你好我是三浦老師的助理,村崎幸子,請多多關照。", chatId);
                    greenApiUtils.sendMessageToUser("能請教一下怎麼稱呼您嗎？", chatId);
                }
            } else {
                String jsonMessage = gson.toJson(new OpenAIMessage(message));
                TextMessage aiMessage = new TextMessage(jsonMessage);
                session.sendMessage(aiMessage);
            }



        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }
}
