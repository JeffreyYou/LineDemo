package com.jeffrey.linedemo.deprecated;

import com.jeffrey.linedemo.entity.GreenMessage;
import com.jeffrey.linedemo.utils.GreenApiUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

import java.sql.SQLOutput;

@Service
public class ReceiveService {
    @Autowired
    private GreenApiUtils greenApiUtils;

    //   @PostConstruct
    @Scheduled(fixedRate = 1000)
    public void continuousPolling() throws Exception {

        greenApiUtils.clearQueue();
        GreenMessage data = null;
        while (true) {
            try {
                data = greenApiUtils.receiveNotification();
                if (data != null) {
                    if (data.getTypeWebhook().equals("incomingMessageReceived")) {
                        System.out.println(data.toString());
                    }
//                    greenApiUtils.deleteNofitication(data.getReceiptId());

                }

            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
    }
}
