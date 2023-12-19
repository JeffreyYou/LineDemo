package com.jeffrey.linedemo;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;
import org.springframework.scheduling.annotation.EnableScheduling;


@SpringBootApplication
@EnableScheduling
/*@EnableJpaRepositories(basePackages = "com.jeffrey.linedemo.repository")*/
public class LineDemoApplication {

    public static void main(String[] args) {
        SpringApplication.run(LineDemoApplication.class, args);
    }

}
