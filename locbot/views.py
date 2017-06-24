# linebot/locbot/views.py

# WebhookHandler version

import logging
import locbot.gmap
import threading 
import os
from django.core.cache import cache
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextSendMessage, TextMessage, VideoMessage, 
    AudioMessage, StickerMessage, ImageMessage, LocationMessage, LocationSendMessage)

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(settings.LINE_CHANNEL_SECRET)
gmap = locbot.gmap.Gmap()
logging.basicConfig(level=logging.DEBUG)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    mapkey = None
    try:
        logging.debug(str(os.getpid()) + "|handle_location_message|>>>")
        mapkey = cache.get(event.source.user_id)
        
        if mapkey:
            logging.info(event.source.user_id + "|find|" + mapkey)
            cache.set(event.source.user_id, "")
            ret = gmap.place_nearby((event.message.latitude, event.message.longitude), mapkey)
            msgs = []
            for obj in ret:
                msgs.append(LocationSendMessage(
                    title=obj['name'],
                    address=obj['addr'],
                    latitude=obj['lat'],
                    longitude=obj['lng']
                ))
            if not msgs:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='找不到'+mapkey)
                )
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    messages=msgs
                )
        else:
            logging.warning(event.source.user_id + "=> not found")
    except LineBotApiError as e:
        print(e)

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    try:
        logging.debug(str(os.getpid()) + "|handle_text_message|>>>")
        text = event.message.text
        if text[0] == u'找':
            key = text[1:]
            cache.set(event.source.user_id, key)
            msg = u'你要找\u300e' + key + '\u300f,請輸入您的位置' + '\u2198'
            logging.info(event.source.user_id + "=>" + msg)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=msg)
            )
    except LineBotApiError as e:
        logging.warning(e)

@handler.add(MessageEvent, message=VideoMessage)
def handle_video_message(event):
    try:
        print(event)
    except LineBotApiError as e:
        logging.warning(e)

@handler.add(MessageEvent, message=AudioMessage)
def handle_audio_message(event):
    try:
        print(event)
    except LineBotApiError as e:
        logging.warning(e)

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    try:
        print(event)
    except LineBotApiError as e:
        logging.warning(e)

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    try:
        print(event)
        #line_bot_api.reply_message(
        #    event.reply_token,
        #    TextSendMessage(text="Image")
        #)
    except LineBotApiError as e:
        logging.warning(e)

@handler.default()
def default(event):
    print(event)


@csrf_exempt
def callback(request):
    global usermap
    global count
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')
        print(signature)
        print(body)
        print(str(os.getpid())+"|callback")
        try:
            handler.handle(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()
        return HttpResponse()
    else:
        return HttpResponseBadRequest()
