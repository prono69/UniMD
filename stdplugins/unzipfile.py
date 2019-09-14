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


# @borg.on(admin_cmd(pattern=("unzip")))
# async def _(event):
#     if event.fwd_from:
#         return
#     if not event.is_reply:
#         await event.edit("Reply to a file to unzip it.")
#         return
#     mone = await event.edit("Processing ...")
#     if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
#         os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
#     if event.reply_to_msg_id:
#         reply_message = await event.get_reply_message()
#         try:
#             c_time = time.time()
#             downloaded_file_name = await borg.download_media(
#                 reply_message,
#                 Config.TMP_DOWNLOAD_DIRECTORY,
#                 progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
#                     progress(d, t, mone, c_time, "trying to unzip")
#                 )
#             )
#             directory_name = downloaded_file_name
#             await event.edit(downloaded_file_name)
#         except Exception as e:  # pylint:disable=C0103,W0703
#             await mone.edit(str(e))

#     await event.edit("DONE!!!")
#     await asyncio.sleep(7)
#     await event.delete()


@borg.on(admin_cmd(pattern=("unzip")))
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.edit("Reply to a file to compress it.")
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
                    progress(d, t, mone, c_time, "trying to download")
                )
            )
            directory_name = downloaded_file_name
            await event.edit(downloaded_file_name)
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    

    working_directory = Config.TMP_DOWNLOAD_DIRECTORY
    os.chdir(working_directory)


    for file in os.listdir(working_directory):   # get the list of files
        if zipfile.is_zipfile(file): # if it is a zipfile, extract it
            with zipfile.ZipFile(file) as item: # treat the file as a zip
                item.extractall()  # extract it in the working directory
                await borg.send_file(event.chat_id,working_directory + ".zip",caption="Zipped By @By_Azade",force_document=True,allow_cache=False,reply_to=event.message.id,)
    await event.edit("DONE!!!")
    await asyncio.sleep(7)
    await event.delete()


# working_directory = Config.TMP_DOWNLOAD_DIRECTORY
# os.chdir(working_directory)

# for file in os.listdir(working_directory):   # get the list of files
#     if zipfile.is_zipfile(file): # if it is a zipfile, extract it
#         with zipfile.ZipFile(file) as item: # treat the file as a zip
#            item.extractall()  # extract it in the working directory
#            await borg.send_file(event.chat_id,directory_name + ".zip",caption="Zipped By @By_Azade",force_document=True,allow_cache=False,reply_to=event.message.id,)

# from zipfile import ZipFile
# zf = ZipFile(directory_name, 'r')
# zf.extractall('path_to_extract_folder')
# zf.close()
