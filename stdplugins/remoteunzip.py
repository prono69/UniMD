import asyncio
import os
import re
import time
import zipfile
from datetime import datetime
from zipfile import ZipFile

from pySmartDL import SmartDL
from remotezip import RemoteZip
from telethon import events
from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo

from uniborg.util import admin_cmd, humanbytes, progress, time_formatter

from sample_config import Config

filedir = f"{Config.TMP_DOWNLOAD_DIRECTORY}extracted/"

@borg.on(events.NewMessage(pattern=("runzip")))
async def _(event):
    """ remote unzip with url """
    await event.edit("`Processing...`")
    textx = await event.get_reply_message()
    message = event.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await event.edit("`Usage: .runzip <url> with .zip extention url`")
        return
    reply = ''
    links = re.findall(r'\bhttps?://.*\.\S+', message)
    if not links:
        reply = "`No links found!`"
        await event.edit(reply)
    for link in links:
        if link.endswith("zip") in link:
            with RemoteZip(links) as zip:
                zip.extractall(filedir)
                x = zip.extractall(filedir)
                await borg.send_file(
                                event.chat_id,
                                x,
                                caption="unzipped @By_Azade",
                                # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                                #     progress(d, t, event, c_time, "trying to upload")
                                # )
                            )
        else:
            await event.get_reply_message("there is no .zip link")

    await event.edit(reply)
