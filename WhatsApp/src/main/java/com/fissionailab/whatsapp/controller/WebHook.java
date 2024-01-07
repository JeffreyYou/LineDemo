package com.fissionailab.whatsapp.controller;

import com.fissionailab.whatsapp.entity.GreenMessage;
import com.fissionailab.whatsapp.service.OpenaiService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.io.BufferedReader;
import java.io.IOException;

@RequestMapping("/webhook")
@RestController
public class WebHook {
    @Autowired
    OpenaiService openaiService;

//    Your public IP address
//    http://99.9.142.36:8080/webhook/receive
    @RequestMapping("receive")
    public ResponseEntity<String> test(@RequestBody GreenMessage message) {
//        System.out.println(message.toString());
//    public ResponseEntity<String> test(HttpServletRequest message) {
//        StringBuilder stringBuilder = new StringBuilder();
//        String line;
//        try (BufferedReader reader = message.getReader()) {
//            while ((line = reader.readLine()) != null) {
//                stringBuilder.append(line);
//            }
//        } catch (IOException e) {
//            throw new RuntimeException(e);
//        }
//        System.out.println(stringBuilder.toString());

        if (message.getTypeWebhook().equals("incomingMessageReceived")) {
            openaiService.sendMessage(message);
        }
        return ResponseEntity.ok("Message Received");
    }
}
