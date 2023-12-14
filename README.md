# Line Demo

## 1. Quick Start

**LangChain Server (Real Char):**

Install dependencies

```shell
pip install -r requirements.txt --user
```
Setup Environment Variable

```shell
cp .env.example .env
# Put your OpenAI Api Key in .env file
```

Start the server

```shell
python cli.py run-uvicorn --port 8000 --host 0.0.0.0 
```

**Webhook Server:**

Open `WebHook Server` through IntelliJ 

Run the `LineDemoApplication`

**Green API Documentation:**

https://green-api.com/en/docs/api/sending/SendMessage/

https://green-api.com/en/docs/api/receiving/technology-http-api/ReceiveNotification/

https://green-api.com/en/docs/api/receiving/technology-http-api/DeleteNotification/

## 2. Schedule

[Dec 13.2023](./schedule/Dec13_2023.md)

## 3. Project Structure

<details> <summary> <b>👇 Click Me </b></summary>


```
LineDemo
│   .gitignore
│   commit.py
│   README.md
│
├───data
├───Development
│       template.md
│
├───images
│       website1.png
│       website2.png
│
├───LangChain Server
│   │   catalog.py
│   │   cli.py
│   │   main.py
│   │   openai_llm.py
│   │   requirements.txt
│   │   script
│   │   utils.py
│   │   websocket_routes.py
│   │
│   └───character
│       ├───Day1Demo
│       │       config.yaml
│       │
│       ├───Day2Demo
│       │       config.yaml
│       │
│       └───LineDemo
│               config.yaml
│
└───WebHook Server
    │   .gitignore
    │   HELP.md
    │   mvnw
    │   mvnw.cmd
    │   pom.xml
    │
    ├───.idea
    │       .gitignore
    │       compiler.xml
    │       encodings.xml
    │       jarRepositories.xml
    │       misc.xml
    │       uiDesigner.xml
    │       workspace.xml
    │
    ├───.mvn
    │   └───wrapper
    │           maven-wrapper.jar
    │           maven-wrapper.properties
    │
    ├───src
    │   ├───main
    │   │   ├───java
    │   │   │   └───com
    │   │   │       └───jeffrey
    │   │   │           └───linedemo
    │   │   │               │   LineDemoApplication.java
    │   │   │               │
    │   │   │               ├───config
    │   │   │               │       WebSocketConfig.java
    │   │   │               │
    │   │   │               ├───controller
    │   │   │               │       WebHook.java
    │   │   │               │
    │   │   │               ├───deprecated
    │   │   │               │       ReceiveService.java
    │   │   │               │
    │   │   │               ├───entity
    │   │   │               │       GreenMessage.java
    │   │   │               │       OpenAIMessage.java
    │   │   │               │
    │   │   │               ├───service
    │   │   │               │       OpenaiService.java
    │   │   │               │
    │   │   │               └───utils
    │   │   │                       GreenApiUtils.java
    │   │   │                       WebSocketUtils.java
    │   │   │
    │   │   └───resources
    │   │       │   application.properties
    │   │       │
    │   │       ├───static
    │   │       └───templates
    │   └───test
    │       └───java
    │           └───com
    │               └───jeffrey
    │                   └───linedemo
    │                           LineDemoApplicationTests.java
    │
    └───target
        ├───classes
        │   │   application.properties
        │   │
        │   └───com
        │       └───jeffrey
        │           └───linedemo
        │               │   LineDemoApplication.class
        │               │
        │               ├───config
        │               │       WebSocketConfig.class
        │               │
        │               ├───controller
        │               │       WebHook.class
        │               │
        │               ├───deprecated
        │               │       ReceiveService.class
        │               │
        │               ├───entity
        │               │       GreenMessage$InstanceData.class
        │               │       GreenMessage$MessageData$TextMessageData.class
        │               │       GreenMessage$MessageData.class
        │               │       GreenMessage$SenderData.class
        │               │       GreenMessage.class
        │               │       OpenAIMessage.class
        │               │
        │               ├───service
        │               │       OpenaiService.class
        │               │
        │               └───utils
        │                       GreenApiUtils.class
        │                       WebSocketUtils$MessageHandler.class
        │                       WebSocketUtils.class
        │
        └───generated-sources
            └───annotations
```

</details> 

## 4. Tech Stack
<details> <summary> <b>👇 Click Me </b></summary>

- Green API
- LangChain
- Docker
- Spring Boot
- Spring MVC
- WebSocket
- Chroma
- MySQL / SQLite

</details> 

