package com.fissionailab.whatsapp.utils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketHttpHeaders;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.client.WebSocketClient;
import org.springframework.web.socket.handler.TextWebSocketHandler;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;
import java.math.BigInteger;

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
                String messageToUser = sb.toString();
                if (messageToUser.endsWith("[PDF_01]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[PDF_01]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "PDF/开群第1天 日本(最终版本).pdf");
                } else if (messageToUser.endsWith("[PDF_02]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[PDF_02]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "PDF/开群第2天 日本(最终版).pdf");
                } else if (messageToUser.endsWith("[PDF_03]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[PDF_03]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "PDF/10月17日です朝情報.pdf");
                } else if (messageToUser.endsWith("[Picture_01]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[Picture_01]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "picture/breakfast.jpg");
                } else if (messageToUser.endsWith("[Picture_02]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[Picture_02]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "picture/lunch.jpg");
                } else if (messageToUser.endsWith("[Picture_03]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[Picture_03]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "picture/yoga.jpg");
                } else if (messageToUser.endsWith("[Picture_04]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[Picture_04]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "picture/午饭.jpg");
                } else if (messageToUser.endsWith("[Picture_05]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[Picture_05]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "picture/在做什么.jpg");
                } else if (messageToUser.endsWith("[Picture_06]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[Picture_06]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "picture/san.jpg");
                } else if (messageToUser.endsWith("[Picture_07]")) {
                    String textMessage = messageToUser.substring(0, messageToUser.length() - "[Picture_07]".length());
                    greenApiUtils.sendMessageToUser(textMessage, userId);
                    greenApiUtils.sendFileToUser(userId, "picture/晚上出去吗.jpg");
                }
                else {
                    greenApiUtils.sendMessageToUser(messageToUser, userId);
                }


                sb.setLength(0);
                System.out.println();
            }
        }
    }

    private String generateUri(String phone) throws NoSuchAlgorithmException {
        StringBuilder builder = new StringBuilder("ws://");
        String url = "localhost:8001";
        String api_key = "123";
        String llm_model = "gpt-3.5-turbo-16k";

        // generate sessionId hash based on phone number
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hash = md.digest(phone.getBytes(StandardCharsets.UTF_8));
        BigInteger number = new BigInteger(1, hash);
        String sessionId = number.toString(16); // Convert to hexadecimal string

        builder.append(url)
                .append("/ws/")
                .append(sessionId)
                .append("?api_key=")
                .append(api_key)
                .append("&llm_model=")
                .append(llm_model);
        return builder.toString();
    }
}
