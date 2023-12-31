package com.fissionailab.whatsapp.config;

import com.fissionailab.whatsapp.utils.SelectCharacterUtils;
import com.google.gson.Gson;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
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
    public ConcurrentHashMap<String, String> userCharacter() {
        return new ConcurrentHashMap<>();
    }

    @Bean
    public RestTemplate restTemplate() {
        return new RestTemplate();
    }

    @Bean
    public Gson gsonClient() {
        return new Gson();
    }

    public SelectCharacterUtils selectCharacterUtils() {
        return new SelectCharacterUtils();
    }
}
