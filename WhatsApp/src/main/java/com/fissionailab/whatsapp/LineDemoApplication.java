package com.fissionailab.whatsapp;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

//@EnableScheduling
@SpringBootApplication
public class LineDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(LineDemoApplication.class, args);
    }

}
