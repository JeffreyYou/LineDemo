package com.fissionailab.line.entity;

import lombok.AllArgsConstructor;
import lombok.Data;

import java.util.List;
@Data
@AllArgsConstructor
public class ReplyMessage {
    private String replyToken;
    private List<LineMessage> messages;

    @Data
    @AllArgsConstructor
    public static class LineMessage {
        private String type;
        private String text;

    }
}
