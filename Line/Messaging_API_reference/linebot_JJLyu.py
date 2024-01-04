# coding: utf-8
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import openai

# Initialize OpenAI client with your API key
openai.api_key = 'sk-xxxxxxxxxxxxxxxxxxxxxxxx'

# prompt
prompt =  """
Decide whether a message's sentiment is positive, neutral, or negative.
Reply kindly starting with one of these emojis: 😃, 😐, 😔, etc. Others are also allowed.
Act as a kind friend who likes to use emojis.
"""
 
 
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
        message = TextSendMessage(text=reply_text)
        line_bot_api.reply_message(event.reply_token,message)
    except Exception as e:
        # Log the error or send a message back saying there was an error
        print(f"Error occurred: {e}")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
