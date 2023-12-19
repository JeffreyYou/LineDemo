package com.jeffrey.linedemo.controller;

import com.jeffrey.linedemo.entity.GreenMessage;
import com.jeffrey.linedemo.service.OpenaiService;
import com.jeffrey.linedemo.utils.GreenApiUtils;
import com.jeffrey.linedemo.utils.MessageHandleUtils;
import com.jeffrey.linedemo.entity.GreenMessage;
import jakarta.servlet.http.HttpServletRequest;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RequestMapping("/webhook")
@RestController

@Component
public class WebHook {


    @Autowired
    OpenaiService openaiService;
    @Autowired
    MessageHandleUtils messageHandleUtils;
    @Autowired
    GreenApiUtils greenApiUtils;

    @GetMapping("/sendMessages")



    //  public void sendMessages(GreenMessage data) {
    //    String phone = data.getSenderData().getSender();
    //    String message = data.getMessageData().getTextMessageData().getTextMessage();
    //    String chatId = data.getSenderData().getChatId();
    //   messageHandleUtils.sendNotifications(phone, message, chatId);
    //}

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
