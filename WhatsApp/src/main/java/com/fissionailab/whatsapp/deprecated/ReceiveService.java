package com.fissionailab.whatsapp.deprecated;

import com.fissionailab.whatsapp.entity.GreenMessage;
import com.fissionailab.whatsapp.entity.GreenMessageHTTP;
import com.fissionailab.whatsapp.service.OpenaiService;
import com.fissionailab.whatsapp.utils.GreenApiUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;

@Service
public class ReceiveService {
    @Autowired
    private GreenApiUtils greenApiUtils;
    @Autowired
    OpenaiService openaiService;

    //   @PostConstruct
    @Scheduled(fixedRate = 1000)
    public void continuousPolling() throws Exception {

        greenApiUtils.clearQueue();
        GreenMessageHTTP data = null;
        while (true) {
            try {
                data = greenApiUtils.receiveNotification();
                if (data != null) {
                    if (data.getBody().getTypeWebhook().equals("incomingMessageReceived")) {
                        GreenMessage message = data.getBody();
                        openaiService.sendMessage(message);
//                        System.out.println(data.toString());
                    }
                    greenApiUtils.deleteNofitication(data.getReceiptId());

                }

            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
    }
}
