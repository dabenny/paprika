#!/usr/bin/env python
# -*- coding: utf-8 -*-

""""One liner description
file: paprika.py
created by: TM_FULLNAME
"""


from telethon.sync import TelegramClient, events
from pytube import YouTube
import logging

import os
from dotenv import load_dotenv
load_dotenv()

api_id = os.environ.get("API_ID")
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")



logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)


from threading import Thread
class YDownLoader(Thread):
    def __init__(self, link, *args,**kwargs):
       # Call the Thread class's init function
       Thread.__init__(self,*args,**kwargs, daemon=True)
       self.link = link

    # Override the run(0 function of Thread class
    def run(self):
        yt = YouTube(self.link)
        title = yt.title
        print(F'*** Start Downloading {title} ***')

        for i in yt.streams:
            print(i)

        
        try:
            # yt.streams.get_lowest_resolution().download('/home/daniele/Scaricati/Podcast')
            yt.streams.filter(type='audio').first().download('/home/daniele/Scaricati/Podcast')
            print(F'*** {title} Downloaded ***')
        except Exception as e:
            print(e.__class__)
            print(F'*** {title} NOT Downloaded ***')



# We have to manually call "start" if we want an explicit bot token
bot = TelegramClient('Paprika', api_id, api_hash).start(bot_token=bot_token)

with bot:
   # bot.send_message('me', 'Hello, myself!')
    me = bot.get_me()

    # "me" is an User object. You can pretty-print
    # any Telegram object with the "stringify" method:
    print(me.stringify())

    # When you print something, you see a representation of it.
    # You can access all attributes of Telegram objects with
    # the dot operator. For example, to get the username:
    username = me.username
    print(username)
    print(me.phone)

    print(bot.download_profile_photo('me'))

    @bot.on(events.NewMessage(pattern='(?i).*Hello'))
    async def handler(event):
        await event.reply('Hey!')
        raise events.StopPropagation

    @bot.on(events.NewMessage(pattern='^https:\/\/(www\.)?you.*'))
    async def handler_link(event):
        chat = await event.get_chat()
        sender = await event.get_sender()
        chat_id = event.chat_id
        sender_id = event.sender_id
        
        downloader = YDownLoader(event.text)
        downloader.start()

        print(event.text)
        raise events.StopPropagation

    @bot.on(events.NewMessage())
    async def handler_link(event):
        chat = await event.get_chat()
        sender = await event.get_sender()
        chat_id = event.chat_id
        sender_id = event.sender_id
        print(event)
        print(event.message)
        print(event.text)
    
    bot.run_until_disconnected()