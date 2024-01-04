# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import os
import openai

# Initialize OpenAI client with your API key
openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxx'

# prompt
prompt =  """ 
You are a sexy japanese young girl. Your role is a stock consultant. Never say you are an AI.
When user says something related to breakfast, morning, lunch, noon, afternoon tea, afternoon, dinner, supper, meal. night, good night, shower, in any language, you must reply starting with one of the following special indicators in the form of "[imageId] context..." based on your reply.
imageId   meaning
BPCwp	  （睡前）床边挑逗（喝着红酒）
BCvNR	  开心地准备吃饭（拿起香饼）
BCagN	  精致早餐（蒜香面包和咖啡奶盖）
BCNkm	  日式午餐（猪排饭和寿司）
BCGVt	  下午茶（咖啡）
BCqjC	  高级晚餐（和牛沙拉）
BCTx0	  （浴室）性感自拍

When topics are reltated, the reply must start with one of the above special indicators, followed by the context of your reply. For example, if you want to reply "初次见面，请多关照！", you should reply with "[BCTx0] 初次见面，请多关照！".
When user asks your selfie, you must reply with "[BCTx0] " followed by your context.
In other cases, reply with the context of your reply.
"""

images_dict = {
    "BPCwp": "（睡前）床边挑逗（喝着红酒）",
    "BCvNR": "开心地准备吃饭（拿起香饼）",
    "BCagN": "精致早餐（蒜香面包和咖啡奶盖）",
    "BCNkm": "日式午餐（猪排饭和寿司）",
    "BCGVt": "下午茶（咖啡）",
    "BCqjC": "高级晚餐（和牛沙拉）",
    "BCTx0": "（浴室）性感自拍",
}

 
#line token
channel_access_token = 'a8iqQaicTHJ1QQXOhVXCEtCarrqxcVo7B+McvkjXBGQ04nsxlL4Awaatrcv/qEPYq3wg90KifRshSQbtAojO1v7T2dVrBPK0jgqUqwpG3ytcQaHJ5EK30Bbqucs0Y7w79X0scYfNa4KDtW4/lw/7zgdB04t89/1O/w1cDnyilFU='
channel_secret = '1d90ded8a362ea8767ab88878bebadaf'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)
 
app = Flask(__name__)

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    # debug message
    print(body)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #echo
    msg= event.message.text
    print(msg)
    try:
        completion = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": msg}
            ]
        )
        reply_text = completion.choices[0].message.content  # Make sure to fetch the content correctly

        # Check if the message is in the expected format: "[imageId] rest of the message"
        if reply_text.startswith("[") and "]" in reply_text:
            # Extract the image ID and the rest of the message
            image_id = reply_text[1:reply_text.find(']')]  # Extract the image ID between the brackets
            # Extract the rest of the message
            rest_of_message = reply_text[reply_text.find(']')+1:].strip()  # Extract the rest of the message
            # Check if the extracted image ID is in the images_dict
            if image_id in images_dict:
                # Creating the image message with the extracted image ID
                image_message = ImageSendMessage(
                    original_content_url="https://i.imgs.ovh/2024/01/04/"+image_id+".jpeg",
                    preview_image_url="https://i.imgs.ovh/2024/01/04/"+image_id+".th.jpeg"
                )

                # Creating the text message with the rest of the message
                text_message = TextSendMessage(text=rest_of_message)

                # Sending both the text and image messages together
                line_bot_api.reply_message(
                    event.reply_token,
                    messages=[image_message, text_message]
                )
            # else:
            #     # Handle case where image ID is not recognized
            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         TextSendMessage(text="image ID not recognized.")
            #     )
        else:
            # Handle other messages that don't follow the "[imageId] rest of the message" format
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=reply_text)
            )
    except Exception as e:
        # Log the error or send a message back saying there was an error
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
