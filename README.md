# Line Demo

## 1. Installation

LangChain Server (Real Char):

```shell
pip install -r requirements.txt --user
```

```shell
python cli.py run-uvicorn --port 8000 --host 0.0.0.0 
```

Webhook Server:

Open `WebHook Server` through IntelliJ 



## 2. Schedule

### Dec 13. 2023

#### 1. 整理聊天记录

每个人整理两个2个助理的聊天记录

格式:

```python
AI: 内容
User: 聊天内容
# 去除图片和聊天表情的符号，纯文本
```

每一天的聊天内容空行分隔开, 保存到 `data` 文件夹

如果可行的话可以写一个脚本处理更好

#### 2. Prompt测试

访问 http://13.56.166.103/ (注意不是https) 可以在线测试prompt,不过还有很多bug可能用起来比较麻烦

用法:

```python
# 左下角API Setting选择模型并输入你的OpenAI Key，调节temperature
# 目前GPT-3.5-turbo有bug，选择别的模型就行

# 输入Character Name和Character的设定并在左下角Create Character

# 如果遇到bug，F12开发者工具->Application->Local Storage->Clear Local Storage->重新访问上面链接
# 目前删除Character时可能会遇到bug，后面我会修一下
```

Example:

![image-20231212194215964](./images/website1.png)

![image-20231212194300555](./images/website2.png)

建议把这本书第2-3章快速过一遍，更好的写prompt

https://weread.qq.com/book-detail?type=1&senderVid=6727677&v=4cc32520813ab8230g015373

#### 3. 开发日志

请根据 [日志模版](./Development/template.md) 在`Development`文件夹下创建日志文件夹

Example

```
├── Development
│   ├── Template.md
│   ├── Jeffrey You.md
│   ├── xxx.md
│   ├── xxx.md
```

#### 4.  熟悉项目

尝试配置一下环境运行一下，有问题随时找我

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

