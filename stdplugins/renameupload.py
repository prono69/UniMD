"""Download Files to your local server and upload it to you
Syntax:
.rename file.name as reply to a Telegram media
.rnupload file.name as reply to a Telegram media to rename and upload
.rnstreamupload file.name as reply to a Telegram media to rename and upload as streamable file"""
from telethon import events
import aiohttp
import asyncio
import json
import os
import requests
import subprocess
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from telethon.tl.types import DocumentAttributeVideo
from telethon.errors import MessageNotModifiedError

import time
from uniborg.util import progress, humanbytes, TimeFormatter

thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"

def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        else:
            output_lst.append(current_file_name)
    return output_lst


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

@borg.on(events.NewMessage(pattern=r"\.rename ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    await event.edit("Renaming in process 🙄🙇‍♂️🙇‍♂️🙇‍♀️ It might take some time if file size is big")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        if input_str:
            file_name = input_str
            reply_message = await event.get_reply_message()
            c_time = time.time()
            to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
            downloaded_file_name = os.path.join(to_download_directory, file_name)
            downloaded_file_name = await borg.download_media(
                reply_message,
                downloaded_file_name)
            end = datetime.now()
            ms = (end - start).seconds
            if os.path.exists(downloaded_file_name):
                await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
            else:
                await event.edit("Error Occurred\n {}".format(input_str))
        else:
            await event.edit("Forgot to give File Name 🙄🙇‍♂️🙇‍♂️🙇‍♀️\n")
    else:
        await event.edit("Syntax // .rename file.name as reply to a Telegram media")


@borg.on(events.NewMessage(pattern=r"\.rnupload ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
        # if thumb != None
        # await event.edit("Thumbnail exists")
    await event.edit("Rename & Upload in process 🙄🙇‍♂️🙇‍♂️🙇‍♀️ It might take some time if file size is big")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        if input_str:
            file_name = input_str
            reply_message = await event.get_reply_message()
            c_time = time.time()
            to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
            downloaded_file_name = os.path.join(to_download_directory, file_name)
            downloaded_file_name = await borg.download_media(
                reply_message,
                downloaded_file_name)
            end = datetime.now()
            ms = (end - start).seconds
            if os.path.exists(downloaded_file_name):
                await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
                thumb = None
                if os.path.exists(thumb_image_path):
                    thumb = thumb_image_path
                if os.path.exists(downloaded_file_name):
                    start = datetime.now()
                    c_time = time.time()
                    await borg.send_file(
                        event.chat_id,
                        downloaded_file_name,
                        force_document=True,
                        supports_streaming=False,
                        allow_cache=False,
                        reply_to=event.message.id,
                        thumb=thumb,
                        progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                            progress(d, t, event, c_time, "trying to upload")
                        )
                    )
                    end = datetime.now()
                    os.remove(downloaded_file_name)
                    ms = (end - start).seconds
                    await event.edit("Uploaded in {} seconds.".format(ms))
                else:
                    await event.edit("404: File Not Found")
            else:
                await event.edit("Error Occurred\n {}".format(input_str))
        else:
            await event.edit("Forgot to give File Name 🙄🙇‍♂️🙇‍♂️🙇‍♀️\n")
    else:
        await event.edit("Syntax // .rnupload file.name as reply to a Telegram media")


@borg.on(events.NewMessage(pattern=r"\.rnstreamupload ?(.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    await event.edit("Rename & Upload as Streamable in process 🙄🙇‍♂️🙇‍♂️🙇‍♀️ It might take some time if file size is big")
    input_str = event.pattern_match.group(1)
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        if input_str:
            file_name = input_str
            reply_message = await event.get_reply_message()
            c_time = time.time()
            to_download_directory = Config.TMP_DOWNLOAD_DIRECTORY
            downloaded_file_name = os.path.join(to_download_directory, file_name)
            downloaded_file_name = await borg.download_media(
                reply_message,
                downloaded_file_name)
            end = datetime.now()
            ms = (end - start).seconds
            if os.path.exists(downloaded_file_name):
                await event.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
                await event.edit("Processing ...")
                thumb = None
                file_name = downloaded_file_name
                if os.path.exists(file_name):
                    if not file_name.endswith((".mkv", ".mp4", ".mp3", ".flac")):
                        await event.edit("Sorry. But I don't think {} is a streamable file. Please try again.\n**Supported Formats**: MKV, MP4, MP3, FLAC".format(file_name))
                        return False
                    if os.path.exists(thumb_image_path):
                        thumb = thumb_image_path
                        # if thumb != None
                        #     await event.edit("Thumbnail exists")
                    else:
                        thumb = get_video_thumb(file_name, thumb_image_path)
                    start = datetime.now()
                    metadata = extractMetadata(createParser(file_name))
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
                    # Telegram only works with MP4 files
                    # this is good, since with MKV files sent as streamable Telegram responds,
                    # Bad Request: VIDEO_CONTENT_TYPE_INVALID
                    c_time = time.time()
                    try:
                        await borg.send_file(
                            event.chat_id,
                            file_name,
                            thumb=thumb,
                            caption=downloaded_file_name,
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
                                progress(d, t, event, c_time, "trying to upload")
                            )
                        )
                    except Exception as e:
                        await event.edit(str(e))
                    else:
                        end = datetime.now()
                        os.remove(downloaded_file_name)
                        ms = (end - start).seconds
                        await event.edit("Uploaded in {} seconds.".format(ms))
                else:
                    await event.edit("404: File Not Found")
            else:
                await event.edit("Error Occurred\n {}".format(input_str))
        else:
            await event.edit("Forgot to give File Name 🙄🙇‍♂️🙇‍♂️🙇‍♀️\n")
    else:
        await event.edit("Syntax // .rnstreamupload file.name as reply to a Telegram media")


async def download_coroutine(session, url, file_name, event, start):
    CHUNK_SIZE = 2341
    downloaded = 0
    display_message = ""
    async with session.get(url) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await event.edit("""Initiating Download
URL: {}
File Name: {}
File Size: {}""".format(url, file_name, humanbytes(total_length)))
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 5.00) == 0 or downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = round(
                        (total_length - downloaded) / speed) * 1000
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        current_message = """**Download Status**
URL: {}
File Name: {}
File Size: {}
Downloaded: {}
ETA: {}""".format(url, file_name, humanbytes(total_length), humanbytes(downloaded), TimeFormatter(estimated_total_time))
                        if current_message != display_message:
                            await event.edit(current_message)
                            display_message = current_message
                    except Exception as e:
                        logger.info(str(e))
                        pass
        return await response.release()
