""" command: .compress """

import asyncio
import os
import time
import zipfile

from telethon import events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter
import time
from datetime import datetime
from pySmartDL import SmartDL
from zipfile import ZipFile


@borg.on(admin_cmd(pattern=("unzip")))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to a file to unzip it.")
        return
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await borg.download_media(
                reply_message,
                Config.TMP_DOWNLOAD_DIRECTORY,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, mone, c_time, "trying to unzip")
                )
            )
            directory_name = downloaded_file_name
            await event.edit(downloaded_file_name)
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    zf = ZipFile(downloaded_file_name, 'r')
    zf.extractall(Config.TMP_DOWNLOAD_DIRECTORY)
    zf.close()
    await unzipdir()
    await event.edit("DONE!!!")
    await asyncio.sleep(7)
    await event.delete()


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))

# from zipfile import ZipFile
# zf = ZipFile(directory_name, 'r')
# zf.extractall('path_to_extract_folder')
# zf.close()
thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"

def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst

async def unzipdir(path,unziph,event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        start = datetime.now()
        # await event.edit("Processing ...")
        lst_of_files = sorted(get_lst_of_files(input_str, []))
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
                # https://stackoverflow.com/a/678242/4723940
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
                if single_file.endswith((".mp4", ".webm")):
                    metadata = extractMetadata(createParser(single_file))
                    duration = 0
                    if metadata.has("duration"):
                        duration = metadata.get('duration').seconds
                    document_attributes = [
                        DocumentAttributeVideo(
                            duration=duration,
                            w=width,
                            h=height,
                            round_message=False,
                            supports_streaming=True
                        )
                    ]
                    supports_streaming = True
                    force_document = False
                if single_file.endswith((".mp3", ".flac", ".wav")):
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
                        # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                        #     progress(d, t, event, c_time, "trying to upload")
                        # )
                    )
                except Exception as e:
                    await borg.send_message(
                        event.chat_id,
                        "{} caused `{}`".format(caption_rts, str(e)),
                        reply_to=event.message.id
                    )
                    # some media were having some issues
                    continue
                os.remove(single_file)
                u = u + 1
                # await event.edit("Uploaded {} / {} files.".format(u, len(lst_of_files)))
                # @ControllerBot was having issues,
                # if both edited_updates and update events come simultaneously.
                await asyncio.sleep(5)
        end = datetime.now()
        ms = (end - start).seconds
        await event.edit("Uploaded {} files in {} seconds.".format(u, ms))
    else:
        await event.edit("404: Directory Not Found")    
