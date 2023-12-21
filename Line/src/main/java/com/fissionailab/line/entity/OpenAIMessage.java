package com.fissionailab.line.entity;

import lombok.Data;

@Data
public class OpenAIMessage {
    String message_content;
    Boolean isQuestion;
    String character;
    String operation;
    public OpenAIMessage(String message, String character, String operation) {
        this.message_content = message;
        this.character = character;
        this.operation = operation;
    }
}
