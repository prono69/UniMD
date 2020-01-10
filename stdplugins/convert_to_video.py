#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) M.Furkan

import asyncio
import os
import subprocess
import time
from datetime import datetime

import telethon
from telethon import *
from telethon.tl.types import *

from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
# https://stackoverflow.com/a/37631799/4723940
from PIL import Image
from sample_config import Config
from uniborg.util import *
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter


@borg.on(admin_cmd(pattern="converttovideo ?(.*)"))
async def convert_to_video(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id is not None:
        download_location = Config.TMP_DOWNLOAD_DIRECTORY 
        reply_message = await event.get_reply_message()
        mone = await event.edit("Processing ...")
        a = mone.edit("converting started please wait for a while!")
        c_time = time.time()
        the_real_download_location = await borg.download_media(
            reply_message,
            Config.TMP_DOWNLOAD_DIRECTORY,
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, mone, c_time, "trying to download")
            )
        )
        if the_real_download_location is not None:
            await borg.send_message
            (
                reply_message,
                "converting error download location is none",
            )
            # don't care about the extension
            await mone.edit("preparing to upload")
            logger.info(the_real_download_location)
            # get the correct width, height, and duration for videos greater than 10MB
            # ref: message from @BotSupport
            width = 0
            height = 0
            duration = 0
            metadata = extractMetadata(createParser(the_real_download_location))
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY  + str(event.reply_to_msg_id) + ".jpg"
            if not os.path.exists(thumb_image_path):
                thumb_image_path = None
            else:
                metadata = extractMetadata(createParser(thumb_image_path))
                if metadata.has("width"):
                    width = metadata.get("width")
                if metadata.has("height"):
                    height = metadata.get("height")
                # get the correct width, height, and duration for videos greater than 10MB
                # resize image
                # ref: https://t.me/PyrogramChat/44663
                # https://stackoverflow.com/a/21669827/4723940
                Image.open(thumb_image_path).convert("RGB").save(thumb_image_path)
                img = Image.open(thumb_image_path)
                # https://stackoverflow.com/a/37631799/4723940
                # img.thumbnail((90, 90))
                img.resize((90, height))
                img.save(thumb_image_path, "JPEG")
                # https://pillow.readthedocs.io/en/3.1.x/reference/Image.html#create-thumbnails
            # try to upload file
            c_time = time.time()
            await borg.send_file(
                chat_id=event.chat.id,
                video=the_real_download_location,
                caption=description,
                duration=duration,
                width=width,
                height=height,
                supports_streaming=True,
                # reply_markup=reply_markup,
                thumb=thumb_image_path,
                reply_to_message_id=event.reply_to_msg_id,
            )
            try:
                os.remove(the_real_download_location)
                os.remove(thumb_image_path)
            except:
                pass
            await mone.edit("uploaded successfully")
    else:
        await mone.edit("send video")
