from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerSendMessage
)

app = Flask(__name__)

line_bot_api = LineBotApi('UzHclTXU22gZOhFMU866HAnoUKKjNOO25JskkBQ310Rnuw/y0ZspP7cIYeUCSW/kIJe/bwMe6AeeDCkUPl7q1jp4YbBM18Xo5zbEmJ/3kCOUnJpCxgJMsd5Wa13AH8ndY7SasRiqf8iy3YI76zxqwgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b5114c2744496b87b88ed089cf64ced4')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    r = '很抱歉，你在說什麼'

    if '貼圖' in msg:
        sticker_message = StickerSendMessage(
            package_id='2',
            sticker_id='24'
        )
    
    line_bot_api.reply_message(
        event.reply_token,
        sticker_message)
    return

    if msg in ['hi', 'Hi']:
        r = '哈囉'
    elif msg == '你吃飯了嗎?':
        r = '你覺得呢?'
    elif msg == '你是誰?':
        r = '你的好朋友'
    elif '訂位' in msg:
        r = '請按以下連結...'

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=r))


if __name__ == "__main__":
    app.run()