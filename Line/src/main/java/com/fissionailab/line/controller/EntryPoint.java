package com.fissionailab.line.controller;

import com.fissionailab.line.entity.LineMessage;
import com.fissionailab.line.entity.OpenAIMessage;
import com.fissionailab.line.entity.ReplyMessage;
import com.fissionailab.line.service.OpenaiService;
import com.fissionailab.line.utils.LineApiUtils;
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
import java.util.concurrent.ConcurrentLinkedDeque;

@RequestMapping("webhook")
@RestController
public class EntryPoint {

    @Autowired
    Log log;


    @Autowired
    private OpenaiService openaiService;

    @Autowired
    private ConcurrentLinkedDeque<LineMessage> tempQueue;

    @RequestMapping("/test")
    public ResponseEntity<String> test(@RequestBody LineMessage request) throws IOException {

//        log.printLog(request);
//        System.out.println(request);

        tempQueue.offerFirst(request);
//        openaiService.sendMessage(request);


        return ResponseEntity.ok("webhook test");
    }
}
