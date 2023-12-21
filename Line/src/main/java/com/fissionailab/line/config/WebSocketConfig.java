package com.fissionailab.line.config;

import com.fissionailab.line.utils.SelectCharacterUtils;
import com.google.gson.Gson;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.client.WebSocketClient;
import org.springframework.web.socket.client.standard.StandardWebSocketClient;

import java.util.concurrent.ConcurrentHashMap;

@Configuration
public class WebSocketConfig {
    @Bean
    public WebSocketClient webSocketClient() {
        return new StandardWebSocketClient();
    }

    @Bean
    public ConcurrentHashMap<String, WebSocketSession> connectionPool() {
        return new ConcurrentHashMap<>();
    }

    @Bean
    public ConcurrentHashMap<String, String> characterList() {
        return new ConcurrentHashMap<>();
    }

    @Bean
    public ConcurrentHashMap<String, String> replyTokenList() {
        return new ConcurrentHashMap<>();
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public HttpHeaders httpHeaders() {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", "Bearer eyJhbGciOiJIUzI1NiJ9.63dTKEW22wAxhrAAPhAD8w5ecI6qWx7OjTdLOA1hIJKBgfANKStXSaA2gJlRdx8cqsQe9qkcMZC4zEpIbgNozwI2rHlDbkSL0_G8QkYQTZJq5JFDmDPm2nQ7NSC--sqG.BMk_1hmtduanIwtQXn-npOCmSdk2UvLy8K4fZSsKxjA");
        return headers;
    }

    @Bean
    public Gson gsonClient() {
        return new Gson();
    }

    public SelectCharacterUtils selectCharacterUtils() {
        return new SelectCharacterUtils();
    }
}
