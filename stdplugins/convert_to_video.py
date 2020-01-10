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
            start = datetime.now()
            lst_of_files = sorted(get_lst_of_files(Config.TMP_DOWNLOAD_DIRECTORY, []))
            logger.info(lst_of_files)
            u = 0
            await event.edit(
                "Found {} files. ".format(len(lst_of_files)) + \
                "Uploading will start soon. " + \
                "Please wait!"
            )
            thumb = None
            if os.path.exists(thumb_image_path):
                thumb = thumb_image_path
            for single_file in lst_of_files:
                if os.path.exists(single_file):
                    caption_rts = os.path.basename(single_file)
                    force_document = True
                    supports_streaming = False
                    document_attributes = []
                    width = 0
                    height = 0
                    if os.path.exists(thumb_image_path):
                        metadata = extractMetadata(createParser(thumb_image_path))
                        if metadata.has("width"):
                            width = metadata.get("width")
                        if metadata.has("height"):
                            height = metadata.get("height")
                    if single_file.upper().endswith(Config.TL_VID_STREAM_TYPES):
                        metadata = extractMetadata(createParser(single_file))
                        duration = 0
                        if metadata.has("duration"):
                            duration = metadata.get('duration').seconds
                        document_attributes = [
                            documentAttributeVideo(
                                duration=duration,
                                w=width,  
                                h=height,
                                round_message=False,
                                supports_streaming=True
                            )
                        ]
                        supports_streaming = True
                        force_document = False
                    if single_file.upper().endswith(Config.TL_MUS_STREAM_TYPES):
                        metadata = extractMetadata(createParser(single_file))
                        duration = 0
                        title = ""
                        artist = ""
                        if metadata.has("duration"):
                            duration = metadata.get('duration').seconds
                        if metadata.has("title"):
                            title = metadata.get("title")
                        if metadata.has("artist"):
                            artist = metadata.get("artist")
                        document_attributes = [
                            DocumentAttributeAudio(
                                duration=duration,
                                voice=False,
                                title=title,
                                performer=artist,
                                waveform=None
                            )
                        ]
                        supports_streaming = True
                        force_document = False
                    try:
                        await borg.send_file(
                            event.chat_id,
                            single_file,
                            caption=caption_rts,
                            force_document=force_document,
                            supports_streaming=supports_streaming,
                            allow_cache=False,
                            reply_to=event.message.id,
                            thumb=thumb,
                            attributes=document_attributes,
                        )
                    except Exception as e:
                        await borg.send_message(
                            event.chat_id,
                            "{} caused `{}`".format(caption_rts, str(e)),
                            reply_to=event.message.id
                        )
                        continue
                    os.remove(single_file)
                    u = u + 1
                    await asyncio.sleep(5)
            end = datetime.now()
            ms = (end - start).seconds
            await event.edit("Uploaded {} files in {} seconds.".format(u, ms))
            await asyncio.sleep(5)
            os.remove(downloaded_file_name)
    else:
        await event.edit("404: Directory Not Found")

def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst