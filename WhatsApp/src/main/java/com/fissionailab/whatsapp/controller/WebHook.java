package com.fissionailab.whatsapp.controller;

import com.fissionailab.whatsapp.entity.GreenMessage;
import com.fissionailab.whatsapp.service.OpenaiService;
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

//    Your public IP address
//    http://99.9.142.36:8080/webhook/receive
    @RequestMapping("receive")
    public ResponseEntity<String> test(@RequestBody GreenMessage message) {
//        System.out.println(message.toString());

        if (message.getTypeWebhook().equals("incomingMessageReceived")) {
            openaiService.sendMessage(message);
        }
        return ResponseEntity.ok("Message Received");
    }
}
