package com.fissionailab.line.utils;

import jakarta.servlet.http.HttpServletRequest;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.io.BufferedReader;

@Component
public class Log {

    public void printLog(HttpServletRequest request) throws IOException {
        // Print basic request info
        System.out.println("Request URL: " + request.getRequestURL().toString());
//        System.out.println("Request Method: " + request.getMethod());
//        System.out.println("Remote Address: " + request.getRemoteAddr());
        StringBuilder requestBody = new StringBuilder();
        String line;

        try (BufferedReader reader = request.getReader()) {
            while ((line = reader.readLine()) != null) {
                requestBody.append(line).append('\n');
            }
        }

        // Print the body data
        System.out.println("Request Body: " + requestBody.toString());


        // Print all headers
//        Enumeration<String> headers = request.getHeaderNames();
//        while (headers.hasMoreElements()) {
//            String header = headers.nextElement();
//            System.out.println("Header: " + header + " - Value: " + request.getHeader(header));
//        }

        // Print all parameters
//        Enumeration<String> parameters = request.getParameterNames();
//        while (parameters.hasMoreElements()) {
//            String parameter = parameters.nextElement();
//            System.out.println("Parameter: " + parameter + " - Value: " + request.getParameter(parameter));
//        }
    }
}
