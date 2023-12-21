package com.fissionailab.line.utils;

import com.fissionailab.line.entity.ReplyMessage;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Slf4j
@Component
public class LineApiUtils {

   @Autowired
   private RestTemplate restTemplate;

   @Autowired
   private HttpHeaders headers;

   public void sendMessageToUser(String message, String replyToken) {

      List<ReplyMessage.LineMessage> data = Arrays.asList(
              new ReplyMessage.LineMessage("text", message)
      );
      ReplyMessage replyMessage = new ReplyMessage(replyToken, data);
      HttpEntity<ReplyMessage> entity = new HttpEntity<>(replyMessage, headers);

      String url = "https://api.line.me/v2/bot/message/reply";
      String response = restTemplate.postForObject(url, entity, String.class);
      System.out.println(response);


   }

   private String generateUrl(String type, Long id) {
      String domain = "https://api.greenapi.com/waInstance";
      String instanceId = "7103884803/";
      String method = "";
      String token = "96c1bf21ad5944c18ef892f30b5743a7f52e33f9e9174c1889";
      if (type.equals("receive")) {
         method = "receiveNotification/";
      }
      if (type.equals("delete")) {
         method = "deleteNotification/";
         token = token + "/" + id;
      }
      if (type.equals("send")) {
         method = "SendMessage/";
      }
      StringBuilder requestUrl = new StringBuilder();
      requestUrl
            .append(domain)
            .append(instanceId)
            .append(method)
            .append(token);

      return requestUrl.toString();
   }
}
