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

Using `git pull` to update most recent changes

## 2. Schedule

[Dec 13.2023](./schedule/Dec13_2023.md)

[Dec 14.2023](./schedule/Dec14_2023.md)

[Dec 15.2023](./schedule/Dec15_2023.md)

## 3. Development Progress

[Jeffrey You](./Development/Jeffrey.md)

## 4. Project Structure

<details> <summary> <b>👇 Click Me </b></summary>

```
LineDemo
│   .gitignore
│   commit.py
│   README.md
│
├───data
│       LINE_-与Kajiyama-satoshi的对话.txt
│       LINE_-与mori907的对话.txt
│       与江角正行的对话.txt
│       与清水-亏的对话.txt
│
├───Development
│       Jeffrey.md
│       template.md
│
├───images
│       website1.png
│       website2.png
│
├───LangChain Server
│   │   .env
│   │   .evn.example
│   │   .gitignore
│   │   alembic.ini
│   │   cli.py
│   │   requirements.txt
│   │   script
│   │   sqlite.py
│   │   test.db
│   │
│   ├───alembic
│   │   │   env.py
│   │   │   script.py.mako
│   │   │
│   │   ├───versions
│   │   │   │   3b2e26d7395f_create_interactions_table.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           3b2e26d7395f_create_interactions_table.cpython-312.pyc
│   │   │
│   │   └───__pycache__
│   │           env.cpython-312.pyc
│   │
│   ├───realtime_ai_character
│   │   │   logger.py
│   │   │   main.py
│   │   │   utils.py
│   │   │   websocket_routes.py
│   │   │
│   │   ├───character_catalog
│   │   │   │   catalog.py
│   │   │   │
│   │   │   ├───Day1Demo
│   │   │   │       config.yaml
│   │   │   │
│   │   │   ├───Day2Demo
│   │   │   │       config.yaml
│   │   │   │
│   │   │   ├───LineDemo
│   │   │   │       config.yaml
│   │   │   │
│   │   │   └───__pycache__
│   │   │           catalog.cpython-312.pyc
│   │   │
│   │   ├───database
│   │   │   │   base.py
│   │   │   │   chroma.py
│   │   │   │   connection.py
│   │   │   │   __init__.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           base.cpython-311.pyc
│   │   │           base.cpython-312.pyc
│   │   │           chroma.cpython-311.pyc
│   │   │           connection.cpython-311.pyc
│   │   │           connection.cpython-312.pyc
│   │   │           __init__.cpython-311.pyc
│   │   │           __init__.cpython-312.pyc
│   │   │
│   │   ├───llm
│   │   │   │   openai_llm.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           openai_llm.cpython-312.pyc
│   │   │
│   │   ├───models
│   │   │   │   interaction.py
│   │   │   │
│   │   │   └───__pycache__
│   │   │           interaction.cpython-312.pyc
│   │   │
│   │   └───__pycache__
│   │           logger.cpython-312.pyc
│   │           main.cpython-312.pyc
│   │           utils.cpython-312.pyc
│   │           websocket_routes.cpython-312.pyc
│   │
│   ├───test
│   │   │   uuid.py
│   │   │
│   │   └───__pycache__
│   │           uuid.cpython-312.pyc
│   │
│   └───__pycache__
│           catalog.cpython-312.pyc
│           main.cpython-312.pyc
│           openai_llm.cpython-312.pyc
│           utils.cpython-312.pyc
│           websocket_routes.cpython-312.pyc
│
├───schedule
│       Dec13_2023.md
│       Dec14_2023.md
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
    │       vcs.xml
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
    │   │   │               │       GreenMessageHTTP.java
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
        │               │       GreenMessageHTTP.class
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

## 5. Tech Stack

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

