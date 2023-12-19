package com.jeffrey.linedemo.utils;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import com.jeffrey.linedemo.entity.GreenMessage;
import com.jeffrey.linedemo.repository.MessageRepository;

import java.util.HashMap;
import java.util.Map;

@Component
public class MessageHandleUtils {
    @Autowired
    GreenApiUtils greenApiUtils;

    /*@Autowired
    MessageRepository messageRepository;*/

    /*private GreenMessage firstReceivedMessage;

    public void setfirstReceivedMessage(GreenMessage data) {
        this.firstReceivedMessage = data;
        messageRepository.save(firstReceivedMessage); // Save the message to SQLite
    }*/

    private static final Map<String, String[]> dayMessages = new HashMap<>();
    static {
        dayMessages.put("[Day1]", new String[]{"謝謝你的聯繫,你好我是三浦老師的助理,村崎幸子,請多多關照。", "能請教一下怎麼稱呼您嗎？"});
        dayMessages.put("[Day2]", new String[]{"晚上好,这是今晚的材料。请务必检查一下。", "从现在开始，我们每天都会给您发送当天的课程内容，请您有空的时候看一下。"});
        dayMessages.put("[Day3]", new String[]{"早上好,新的一周开始了。", "让我们尽力而为吧！"});
        dayMessages.put("[Day4]", new String[]{"晚上好，这就是今天的课程内容。", "今天三浦老師推荐的01920涨了不少，你看到了吗"});
        dayMessages.put("[Day5]", new String[]{"晚上好。对于今天的课程，你有什么感想？", "我想下周我就能关注三浦先生的库存管理了。"});

        // Add other days here...
    }
    /*int i =1;

    @Scheduled(fixedDelay = 3000) // 每隔3秒执行一次
    public void scheduledSendNotifications() {
        if (firstReceivedMessage != null) {
            // 从 lastReceivedMessage 中获取数据
            String phone = firstReceivedMessage.getSenderData().getSender();
            String message = firstReceivedMessage.getMessageData().getTextMessageData().getTextMessage();
            String chatId = firstReceivedMessage.getSenderData().getChatId();


            // 使用获取到的信息调用 sendNotifications 方法
            SendNotification(phone, message, chatId);
            i++;

        }
    }*/
    /*public void SendNotification(String phone, String message, String chatId) {

            String dayKey = "[Day" + i + "]";
            if (dayMessages.containsKey(dayKey)) {
        String[] messages = dayMessages.get(dayKey);
        for (String msg : messages) {
            greenApiUtils.sendMessageToUser(msg, chatId);
            System.out.println(msg);
        }

    }
    }*/



    public static boolean isNotification(String message ){
        return dayMessages.containsKey(message);
    }

    public void SendNotification(String phone, String message, String chatId){

        if (isNotification(message)) {
            String[] messages = dayMessages.get(message);

            for (String msg : messages) {
                greenApiUtils.sendMessageToUser(msg, chatId);
                System.out.println(msg);
            }
        }
    }





}
