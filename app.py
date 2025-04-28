from flask import Flask, request, abort

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境変数からチャンネル情報を取得
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    # リクエストヘッダーから署名検証
    signature = request.headers['X-Line-Signature']

    # リクエストボディを取得
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

# 受信したメッセージにオウム返し
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    reply_text = event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"あなたは「{reply_text}」と言いました！")
    )

if __name__ == "__main__":
    app.run()
