package com.fissionailab.whatsapp.utils;

import org.springframework.stereotype.Component;

@Component
public class URLGenerator {

    private static final String DOMAIN = "https://api.greenapi.com/waInstance";
    private static final String INSTANCE_ID = "7103884803/";
    private static final String DEFAULT_TOKEN = "96c1bf21ad5944c18ef892f30b5743a7f52e33f9e9174c1889";

    public String generateUrl(String type, Long id) {
        String method = determineMethod(type);
        String token = (type.equals("delete")) ? DEFAULT_TOKEN + "/" + id : DEFAULT_TOKEN;

        return DOMAIN + INSTANCE_ID + method + token;
    }

    private String determineMethod(String type) {
        return switch (type) {
            case "receive" -> "receiveNotification/";
            case "delete" -> "deleteNotification/";
            case "send" -> "SendMessage/";
            case "file" -> "sendFileByUpload/";
            default -> throw new IllegalArgumentException("Invalid type: " + type);
        };
    }
}
