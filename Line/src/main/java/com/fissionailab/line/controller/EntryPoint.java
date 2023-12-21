package com.fissionailab.line.controller;

import com.fissionailab.line.entity.MessageBody;
import com.fissionailab.line.entity.ReplyMessage;
import com.fissionailab.line.utils.Log;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.client.RestTemplate;

import java.io.IOException;
import java.util.Arrays;
import java.util.List;

@RequestMapping("webhook")
@RestController
public class EntryPoint {

    @Autowired
    Log log;

    @RequestMapping("/test")
    public ResponseEntity<String> test(@RequestBody MessageBody request) throws IOException {

//        log.printLog(request);
        System.out.println(request);

        String data = request.getEvents().get(0).getMessage().getText();
        String user = request.getEvents().get(0).getSource().getUserId();
        String replyToken = request.getEvents().get(0).getReplyToken();

        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", "Bearer eyJhbGciOiJIUzI1NiJ9.63dTKEW22wAxhrAAPhAD8w5ecI6qWx7OjTdLOA1hIJKBgfANKStXSaA2gJlRdx8cqsQe9qkcMZC4zEpIbgNozwI2rHlDbkSL0_G8QkYQTZJq5JFDmDPm2nQ7NSC--sqG.BMk_1hmtduanIwtQXn-npOCmSdk2UvLy8K4fZSsKxjA");

        List<ReplyMessage.LineMessage> messages = Arrays.asList(
                new ReplyMessage.LineMessage("text", "Hello, Jeffrey"),
                new ReplyMessage.LineMessage("text", "May I help you?")
        );

        ReplyMessage replyMessage = new ReplyMessage(replyToken, messages);
        HttpEntity<ReplyMessage> entity = new HttpEntity<>(replyMessage, headers);

        String url = "https://api.line.me/v2/bot/message/reply";
        String response = restTemplate.postForObject(url, entity, String.class);
        System.out.println(response);

        return ResponseEntity.ok("webhook test");
    }
}
