# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
import os
import openai

# Initialize OpenAI client with your API key
openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxx'

# prompt
prompt =  """
Act as a polite japanese customer service agent, reply starting with only one of the following special indicators in the form of "[stickerId] context..." based on your reply.
stickerId   meaning
16581242	OK
16581243	感谢
16581244	帮大忙了
16581245	好的
16581246	您意下如何
16581247	您还好吗
16581248	拜托了
16581249	我马上去确认
16581250	非常抱歉
16581251	我很欣慰
16581252	辛苦了
16581253	比心
16581254	不愧是你
16581255	我很高兴
16581256	原来如此
16581257	请
16581258	（思考）
16581259	给您添麻烦了
16581260	早安
16581261	晚安
16581262	（紧张）
16581263	（不知所措）
16581264	多谢款待
16581265	加油

The reply must start with one of the above special indicators, followed by the context of your reply. For example, if you want to reply "OK, I will check it immediately.", you should reply with "[16581242] I will check it immediately.".
"""

stickers_dict = {
    "16581242": "OK",
    "16581243": "感谢",
    "16581244": "帮大忙了",
    "16581245": "好的",
    "16581246": "您意下如何",
    "16581247": "您还好吗",
    "16581248": "拜托了",
    "16581249": "我马上去确认",
    "16581250": "非常抱歉",
    "16581251": "我很欣慰",
    "16581252": "辛苦了",
    "16581253": "比心",
    "16581254": "不愧是你",
    "16581255": "我很高兴",
    "16581256": "原来如此",
    "16581257": "请",
    "16581258": "（思考）",
    "16581259": "给您添麻烦了",
    "16581260": "早安",
    "16581261": "晚安",
    "16581262": "（紧张）",
    "16581263": "（不知所措）",
    "16581264": "多谢款待",
    "16581265": "加油"
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

        # Check if the message is in the expected format: "[stickerId] rest of the message"
        if reply_text.startswith("[") and "]" in reply_text:
            # Extract the sticker ID and the rest of the message
            sticker_id = reply_text[1:reply_text.find(']')]  # Extract the sticker ID between the brackets
            # Extract the rest of the message
            rest_of_message = reply_text[reply_text.find(']')+1:].strip()  # Extract the rest of the message
            # Set the package ID (constant for all stickers in this case)
            package_id = '8515'
            # Check if the extracted sticker ID is in the stickers_dict
            if sticker_id in stickers_dict:
                # Creating the sticker message with the extracted sticker ID
                sticker_message = StickerSendMessage(
                    package_id=package_id,
                    sticker_id=sticker_id  # The extracted sticker ID
                )

                # Creating the text message with the rest of the message
                text_message = TextSendMessage(text=rest_of_message)

                # Sending both the text and sticker messages together
                line_bot_api.reply_message(
                    event.reply_token,
                    messages=[sticker_message, text_message]
                )
            # else:
            #     # Handle case where sticker ID is not recognized
            #     line_bot_api.reply_message(
            #         event.reply_token,
            #         TextSendMessage(text="Sticker ID not recognized.")
            #     )
        else:
            # Handle other messages that don't follow the "[stickerId] rest of the message" format
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
