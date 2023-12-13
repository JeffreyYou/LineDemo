package com.jeffrey.linedemo.controller;

import com.jeffrey.linedemo.entity.GreenMessage;
import com.jeffrey.linedemo.service.OpenaiService;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("/webhook")
@RestController
public class WebHook {
    @Autowired
    OpenaiService openaiService;

    @RequestMapping("test")
    public ResponseEntity<String> test(@RequestBody GreenMessage message) {
//        System.out.println(message.toString());

        if (message.getTypeWebhook().equals("incomingMessageReceived")) {
            openaiService.sendMessage(message);
        }
        return ResponseEntity.ok("Message Received");
    }
}
