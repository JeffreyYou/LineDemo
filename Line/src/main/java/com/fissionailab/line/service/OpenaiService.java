package com.fissionailab.line.service;

import com.fissionailab.line.entity.LineMessage;
import com.fissionailab.line.utils.LineApiUtils;
import com.fissionailab.line.utils.SelectCharacterUtils;
import com.fissionailab.line.utils.WebSocketUtils;
import com.google.gson.Gson;
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
    LineApiUtils lineApiUtils;
    @Autowired
    Gson gson;
    @Autowired
    SelectCharacterUtils selectCharacterUtils;

    public void sendMessage(LineMessage data) {
        String message = data.getEvents().get(0).getMessage().getText();
        String userId = data.getEvents().get(0).getSource().getUserId();
        String replyToken = data.getEvents().get(0).getReplyToken();


        System.out.println("[User]: " + message);
        System.out.print("[AI]: ");

        try {
            selectCharacterUtils.handleRequest(message, userId, replyToken);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
    }

}
