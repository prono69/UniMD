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


@borg.on(admin_cmd(pattern=("cmrdl ?(.*)")))
async def _(event):
    url = event.pattern_match.group(1)
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    # if event.reply_to_msg_id:
    start = datetime.now()
    reply_message = await event.get_reply_message()
    try:
        c_time = time.time()
        downloaded_file_name = Config.TMP_DOWNLOAD_DIRECTORY,
        directory_name = downloaded_file_name
        await event.edit("Finish downloading to my local")
        command_to_exec = [
                "bin/cmrudl.py",
                url,
                "-d",
                directory_name
                ]
        sp = subprocess.Popen(command_to_exec, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
    except Exception as e:  # pylint:disable=C0103,W0703
        await mone.edit(str(e))
    else:
        end = datetime.now()
        ms = (end - start).seconds
    if os.path.exists(downloaded_file_name):
        await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    else:
        await mone.edit("Incorrect URL\n {}".format(input_str))