import asyncio
import os
import time
import zipfile

from pySmartDL import SmartDL
from telethon import events
import shutil
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter

from sample_config import Config


@borg.on(admin_cmd(pattern=("tar ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
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
            await event.edit("Finish downloading to my local")
            try:
                input_directory = downloaded_file_name
                input_directory = Config.TMP_DOWNLOAD_DIRECTORY
                if os.path.exists(input_directory):
                    base_dir_name = os.path.basename(input_directory)
                    compressed_file_name = f"{base_dir_name}.tar.gz"
                    file_genertor_command = [
                        "tar",
                        "-zcvf",
                        compressed_file_name,
                        f"{input_directory}"
                    ]
                    process = await asyncio.create_subprocess_exec(
                        *file_genertor_command,
                        # stdout must a pipe to be accessible as process.stdout
                        stdout=asyncio.subprocess.PIPE,
                        stderr=asyncio.subprocess.PIPE,
                    )
                    # Wait for the subprocess to finish
                    stdout, stderr = await process.communicate()
                    e_response = stderr.decode().strip()
                    t_response = stdout.decode().strip()
                    if os.path.exists(compressed_file_name):
                        try:
                            shutil.rmtree(input_directory)
                        except:
                            pass
                        return_name = compressed_file_name
        await borg.send_file(
            event.chat_id,
            directory_name + ".tar",
            caption="TAR Created By @By_Azade",
            force_document=True,
            allow_cache=False,
            reply_to=event.message.id,
        )
        try:
            os.remove(directory_name + ".tar")
            os.remove(directory_name)
        except:
                pass
        await event.edit("Task Completed")
        await asyncio.sleep(3)
        await event.delete()
