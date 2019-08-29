from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()