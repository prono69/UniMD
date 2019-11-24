import asyncio
import os
import shutil
import subprocess
import time
from pySmartDL import SmartDL
from sample_config import Config
from telethon import events
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter
import subprocess
import patoolib
from bin.cmrudl import *
from datetime import datetime
import io




@borg.on(admin_cmd(pattern=("cmrdl ?(.*)")))
async def _(event):
    url = event.pattern_match.group(1)
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        c_time = time.time()
        downloaded_file_name = Config.TMP_DOWNLOAD_DIRECTORY
        await event.edit("Finish downloading to my local")
        command_to_exec = [
                "./bin/cmrudl.py",
                url,
                "-d",
                "./DOWNLOADS/"
                ]
        process = await asyncio.create_subprocess_shell(
        command_to_exec, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        OUTPUT = f"**Files in DOWNLOADS folder:**\n"
        stdout, stderr = await process.communicate()
        if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
            file = open("exec.text","w")
            file.write(str(stdout))
            await borg.send_file(
                    event.chat_id,
                    file,
                    force_document=True,
                    allow_cache=False,
                    caption=OUTPUT,
                    reply_to=event.reply_to_id
           )
           await event.delete()
        if stderr.decode():
            await event.edit(f"**{stderr.decode()}**")
            return
        await event.edit(f"{OUTPUT}{stdout.decode()}")