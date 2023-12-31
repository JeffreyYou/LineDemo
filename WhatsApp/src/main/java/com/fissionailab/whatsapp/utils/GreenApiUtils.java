package com.fissionailab.whatsapp.utils;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fissionailab.whatsapp.entity.GreenMessageHTTP;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.http.*;
import org.springframework.stereotype.Component;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.Map;

@Slf4j
@Component
public class GreenApiUtils {

   @Autowired
   private RestTemplate restTemplate;
   @Autowired
   URLGenerator urlGenerator;

   public void clearQueue() throws JsonProcessingException {
      System.out.println("-----------------------------------------------------Service Started------------------------------------------------------------");
      log.info("Cleaning existing messages...");
      GreenMessageHTTP data = receiveNotification();
      while (data != null) {
         deleteNofitication(data.getReceiptId());
         data = receiveNotification();
      }
      log.info("Message queue cleared");
   }

   public void sendMessageToUser(String message, String recipient) {
      String url =  urlGenerator.generateUrl("send", 0L);

      Map<String, String> payload = new HashMap<>();
      payload.put("chatId", recipient);
      payload.put("message", message);
      HttpHeaders headers = new HttpHeaders();
      headers.setContentType(MediaType.APPLICATION_JSON);
      HttpEntity<Map<String, String>> entity = new HttpEntity<>(payload, headers);

      // Making the POST request
      ResponseEntity<String> response = restTemplate.postForEntity(url, entity, String.class);
//      System.out.println("Response: " + response.getBody());
   }

   public void sendFileToUser(String recipient, String filename) {
//      Generating URL
      String url = urlGenerator.generateUrl("file", 0L);
//      Setup Header
      HttpHeaders headers = new HttpHeaders();
      headers.setContentType(MediaType.MULTIPART_FORM_DATA);
//      SetupPayload
      MultiValueMap<String, Object> payload = new LinkedMultiValueMap<>();
      payload.add("chatId", recipient);
      Resource fileResource = new ClassPathResource("/" + filename);
      payload.add("file", fileResource);
      payload.add("fileName", filename);

      HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(payload, headers);
      String response = restTemplate.postForObject(url, requestEntity, String.class);


   }
   public GreenMessageHTTP receiveNotification() throws JsonProcessingException {
      String url = generateUrl("receive", 0L);

      HttpHeaders headers = new HttpHeaders();
      HttpEntity<String> entity = new HttpEntity<>(null, headers);

      ResponseEntity<GreenMessageHTTP> responseJson = restTemplate.exchange(url, HttpMethod.GET, entity, GreenMessageHTTP.class);
      GreenMessageHTTP message = responseJson.getBody();

      if (message == null) {
         return null;
      }
//      System.out.println(message);
      return message;
   }


   public void deleteNofitication(Long id) {
      String url = generateUrl("delete", id);
      HttpHeaders headers = new HttpHeaders();
      HttpEntity<String> entity = new HttpEntity<>(null, headers);
      ResponseEntity<String> response = restTemplate.exchange(url, HttpMethod.DELETE, entity, String.class);
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
      if (type.equals("file")) {
         method = "sendFileByUpload/";
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
