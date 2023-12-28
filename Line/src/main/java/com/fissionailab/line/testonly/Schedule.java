package com.fissionailab.line.testonly;

import com.fissionailab.line.entity.LineMessage;
import com.fissionailab.line.service.OpenaiService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;

import java.util.concurrent.ConcurrentLinkedDeque;

@Component
public class Schedule {

    @Autowired
    private OpenaiService openaiService;

    @Autowired
    private ConcurrentLinkedDeque<LineMessage> tempQueue;
    @Scheduled(fixedRate = 1000)
    public void performTaskWithFixedRate() {
        if (!tempQueue.isEmpty()) {
            openaiService.sendMessage(tempQueue.pollLast());
        }
    }
}
