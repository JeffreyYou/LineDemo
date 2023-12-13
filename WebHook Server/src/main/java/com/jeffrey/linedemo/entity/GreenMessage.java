package com.jeffrey.linedemo.entity;

import lombok.Data;

@Data
public class GreenMessage {

      private String typeWebhook;
      private InstanceData instanceData;
      private Long timestamp;
      private String idMessage;
      private SenderData senderData;
      private MessageData messageData;

      @Data
      public static class InstanceData {
         private Long idInstance;
         private String wid;
         private String typeInstance;

      }
      @Data
      public static class SenderData {
         private String chatId;
         private String chatName;
         private String sender;
         private String senderName;

      }
      @Data
      public static class MessageData {
         private String typeMessage;
         private TextMessageData textMessageData;

         @Data
         public static class TextMessageData {
            private String textMessage;

         }
      }
}
