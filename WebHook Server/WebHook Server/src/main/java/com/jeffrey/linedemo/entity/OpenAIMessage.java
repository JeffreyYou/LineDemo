package com.jeffrey.linedemo.entity;

import lombok.Data;

@Data
public class OpenAIMessage {
    String messageContent;
    Boolean isQuestion;

    public OpenAIMessage(String message) {
        if (message.startsWith("[day")) {
            this.isQuestion = false;
            this.messageContent = "empty";
        } else {
            this.isQuestion = true;
            this.messageContent = message;
        }
    }
}
