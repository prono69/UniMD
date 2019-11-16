
import asyncio
import os
import time

from datetime import datetime

from sample_config import Config

from uniborg.util import admin_cmd, humanbytes, progress, time_formatter

@borg.on(admin_cmd(pattern=("compress ?(.*)")))
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
            # zipfile.ZipFile(directory_name + '.zip', 'w', zipfile.ZIP_DEFLATED).write(directory_name)
            os.system(f'rar a {Config.TMP_DOWNLOAD_DIRECTORY} {directory_name}')
            await borg.send_file(
                event.chat_id,
                directory_name + ".rar",
                caption="RAR Completed By @By_Azade",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        os.system(f'rar a {Config.TMP_DOWNLOAD_DIRECTORY} {directory_name}')
        await event.edit("Local file compressed to `{}`".format(directory_name + ".rar"))


# os.system('rar a <archive_file_path> <file_path_to_be_added_to_archive>')