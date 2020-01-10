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

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"

@borg.on(admin_cmd(pattern="converttovideo ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    thumb = None
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Downloaded now preparing to streaming upload")
        # if os.path.exists(input_str):
            thumb = None
            if os.path.exists(Config.TMP_DOWNLOAD_DIRECTORY):
                if not downloaded_file_name.endswith((".mkv", ".mp4", ".mp3", ".flac")):
                    await mone.edit(
                        "**Supported Formats**: MKV, MP4, MP3, FLAC"
                    )
                    return False
                if os.path.exists(thumb_image_path):
                    thumb = thumb_image_path   
                else:
                    thumb = get_video_thumb(downloaded_file_name, thumb_image_path)
                start = datetime.now()
                metadata = extractMetadata(createParser(downloaded_file_name))
                duration = 0
                width = 0
                height = 0
                if metadata.has("duration"):
                    duration = metadata.get('duration').seconds
                if os.path.exists(thumb_image_path):
                    metadata = extractMetadata(createParser(thumb_image_path))
                    if metadata.has("width"):
                        width = metadata.get("width")
                    if metadata.has("height"):
                        height = metadata.get("height")
                c_time = time.time()
                try:
                    await borg.send_file(
                        event.chat_id,
                        downloaded_file_name,
                        thumb=thumb,
                        caption=input_str,
                        force_document=False,
                        allow_cache=False,
                        reply_to=event.message.id,
                        attributes=[
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True
                            )
                        ],
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, mone, c_time, "trying to upload")
                        )
                    )
                except Exception as e:
                    await mone.edit(str(e))
                else:
                    end = datetime.now()
                    # os.remove(input_str)
                    ms = (end - start).seconds
                    await mone.edit("Uploaded in {} seconds.".format(ms))
            else:
                await mone.edit("404: File Not Found")

            # await borg.send_file(
            #     event.chat_id,
            #     downloaded_file_name,
            #     supports_streaming=True,
            #     allow_cache=False,
            #     reply_to=event.message.id
            # )





    # thumb = None
    # file_name = input_str
    # if os.path.exists(file_name):
    #     if not file_name.endswith((".mkv", ".mp4", ".mp3", ".flac")):
    #         await mone.edit(
    #             "Sorry. But I don't think {} is a streamable file.".format(file_name) + \
    #             " Please try again.\n" + \
    #             "**Supported Formats**: MKV, MP4, MP3, FLAC"
    #         )
    #         return False
    #     if os.path.exists(thumb_image_path):
    #         thumb = thumb_image_path
    #     else:
    #         thumb = get_video_thumb(file_name, thumb_image_path)
    #     start = datetime.now()
    #     metadata = extractMetadata(createParser(file_name))
    #     duration = 0
    #     width = 0
    #     height = 0
    #     if metadata.has("duration"):
    #         duration = metadata.get('duration').seconds
    #     if os.path.exists(thumb_image_path):
    #         metadata = extractMetadata(createParser(thumb_image_path))
    #         if metadata.has("width"):
    #             width = metadata.get("width")
    #         if metadata.has("height"):
    #             height = metadata.get("height")
    #     # Telegram only works with MP4 files
    #     # this is good, since with MKV files sent as streamable Telegram responds,
    #     # Bad Request: VIDEO_CONTENT_TYPE_INVALID
    #     c_time = time.time()
    #     try:
    #         await borg.send_file(
    #             event.chat_id,
    #             file_name,
    #             thumb=thumb,
    #             caption=input_str,
    #             force_document=False,
    #             allow_cache=False,
    #             reply_to=event.message.id,
    #             attributes=[
    #                 DocumentAttributeVideo(
    #                     duration=duration,
    #                     w=width,
    #                     h=height,
    #                     round_message=False,
    #                     supports_streaming=True
    #                 )
    #             ],
    #             progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
    #                 progress(d, t, mone, c_time, "trying to upload")
    #             )
    #         )
    #     except Exception as e:
    #         await mone.edit(str(e))
    #     else:
    #         end = datetime.now()
    #         os.remove(input_str)
    #         ms = (end - start).seconds
    #         await mone.edit("Uploaded in {} seconds.".format(ms))
    # else:
    #     await mone.edit("404: File Not Found")









def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen([
        'ffmpeg', '-i', file,
        '-ss', str(int((0, metadata.get('duration').seconds)[metadata.has('duration')] / 2)),
        '-filter:v', 'scale={}:-1'.format(width),
        '-vframes', '1',
        output,
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if not p.returncode and os.path.lexists(file):
        return output







def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst