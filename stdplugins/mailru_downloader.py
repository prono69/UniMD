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
    # if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
    #     os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    # if event.reply_to_msg_id:
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
        # sp = subprocess.Popen(command_to_exec, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        process = await asyncio.create_subprocess_shell(
        command_to_exec, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        OUTPUT = f"**Files in DOWNLOADS folder:**\n"
        stdout, stderr = await process.communicate()
        if len(stdout) > Config.MAX_MESSAGE_SIZE_LIMIT:
            with io.BytesIO(str.encode(stdout)) as out_file:
                out_file.name = "exec.text"
                await borg.send_file(
                    event.chat_id,
                    out_file,
                    force_document=True,
                    allow_cache=False,
                    caption=OUTPUT,
                    reply_to=reply_to_id
                )
                await event.delete()
        if stderr.decode():
            await event.edit(f"**{stderr.decode()}**")
            return
        await event.edit(f"{OUTPUT}`{stdout.decode()}`")
    # except Exception as e:  # pylint:disable=C0103,W0703
    #     await mone.edit(str(e))
    # else:
    #     end = datetime.now()
    #     ms = (end - start).seconds
    # if os.path.exists(downloaded_file_name):
    #     await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    # else:
    #     await mone.edit("Incorrect URL\n {}".format(input_str))