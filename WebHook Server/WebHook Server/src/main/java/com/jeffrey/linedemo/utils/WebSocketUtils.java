package com.jeffrey.linedemo.utils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketHttpHeaders;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.client.WebSocketClient;
import org.springframework.web.socket.handler.TextWebSocketHandler;


import java.net.URI;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class WebSocketUtils {

    @Autowired
    WebSocketClient webSocketClient;
    @Autowired
    GreenApiUtils greenApiUtils;
    @Autowired
    ConcurrentHashMap<String, WebSocketSession> userSessions;

    public WebSocketSession createSessionIfNotExist(String phone, String chatId) throws Exception {
        // create session if not exist
        if (!userSessions.containsKey(phone)) {
            connect(phone, chatId);
        }
        // check if the session is still alive
        if (!userSessions.get(phone).isOpen()) {
            connect(phone, chatId);
        }
        // session initialization

        return userSessions.get(phone);
    }

    private void connect(String phone, String chatId) throws Exception {
        String uri = generateUri(phone);

        WebSocketHttpHeaders headers = new WebSocketHttpHeaders();
        headers.add("user_phone", phone);
        headers.add("chat_id", chatId);
        WebSocketSession session = webSocketClient.doHandshake(
                        new MessageHandler(), headers,
                        URI.create(uri))
                        .get();

        userSessions.put(phone, session);

    }

    private class MessageHandler extends TextWebSocketHandler {
        private StringBuilder sb = new StringBuilder();
        @Override
        public void handleTextMessage(WebSocketSession session, TextMessage message) {
            String messagePayload = message.getPayload();
            String userId = session.getHandshakeHeaders().get("chat_id").get(0);

            if (!messagePayload.startsWith("[end_")) {
                System.out.print(messagePayload);
                sb.append(messagePayload);
            } else {
                greenApiUtils.sendMessageToUser(sb.toString(), userId);
                sb.setLength(0);
                System.out.println();
            }
        }
    }

    private String generateUri(String phone) {
        StringBuilder builder = new StringBuilder("ws://");
        String url = "localhost:8000";
        String api_key = "123";
        String llm_model = "gpt-3.5-turbo-16k";

        builder.append(url)
                .append("/ws/")
                .append(phone)
                .append("?api_key=")
                .append(api_key)
                .append("&llm_model=")
                .append(llm_model);
        return builder.toString();
    }
}
