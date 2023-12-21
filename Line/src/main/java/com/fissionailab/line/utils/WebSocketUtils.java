package com.fissionailab.line.utils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketHttpHeaders;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.client.WebSocketClient;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.math.BigInteger;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class WebSocketUtils {

    @Autowired
    WebSocketClient webSocketClient;
    @Autowired
    LineApiUtils lineApiUtils;
    @Autowired
    ConcurrentHashMap<String, WebSocketSession> userSessions;
    @Autowired
    ConcurrentHashMap<String, String> replyTokenList;
    public WebSocketSession createSessionIfNotExist(String userId, String replyToken) throws Exception {
        // create session if not exist
        if (!userSessions.containsKey(userId)) {
            connect(userId, replyToken);
        }
        // check if the session is still alive
        if (!userSessions.get(userId).isOpen()) {
            connect(userId, replyToken);
        }
        // session initialization
        replyTokenList.put(userId, replyToken);

        return userSessions.get(userId);
    }

    private void connect(String userId, String replyToken) throws Exception {
        String uri = generateUri(userId);

        WebSocketHttpHeaders headers = new WebSocketHttpHeaders();
        headers.add("user_id", userId);
        WebSocketSession session = webSocketClient.doHandshake(
                        new MessageHandler(), headers,
                        URI.create(uri))
                        .get();

        userSessions.put(userId, session);

    }

    private class MessageHandler extends TextWebSocketHandler {
        private StringBuilder sb = new StringBuilder();
        @Override
        public void handleTextMessage(WebSocketSession session, TextMessage message) {
            String messagePayload = message.getPayload();
            String userId = session.getHandshakeHeaders().get("user_id").get(0);

            if (!messagePayload.startsWith("[end_")) {
                System.out.print(messagePayload);
                sb.append(messagePayload);
            } else {
                String replyToken = replyTokenList.get(userId);
                lineApiUtils.sendMessageToUser(sb.toString(), replyToken);
                sb.setLength(0);
                System.out.println();
            }
        }
    }

    private String generateUri(String userId) throws NoSuchAlgorithmException {
        StringBuilder builder = new StringBuilder("ws://");
        String url = "localhost:8000";
        String api_key = "123";
        String llm_model = "gpt-3.5-turbo-16k";

        // generate sessionId hash based on phone number
        MessageDigest md = MessageDigest.getInstance("SHA-256");
        byte[] hash = md.digest(userId.getBytes(StandardCharsets.UTF_8));
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
