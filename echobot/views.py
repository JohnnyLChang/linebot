# line_echobot/echobot/views.py

# WebhookHandler version


from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage, TextMessage, VideoMessage, AudioMessage, StickerMessage, ImageMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=event.message.text)
        )
    except LineBotApiError as e:
        print(e)

@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Video")
        )
    except LineBotApiError as e:
        print(e)

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Audio")
        )
    except LineBotApiError as e:
        print(e)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Sticker")
        )
    except LineBotApiError as e:
        print(e)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    try:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Image")
        )
    except LineBotApiError as e:
        print(e)

@handler.default()
def default(event):
    #print(event)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Currently Not Support None Text Message')
    )


@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
