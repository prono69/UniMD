import asyncio
import os
import shutil
import tarfile
import time

from pySmartDL import SmartDL
from sample_config import Config
from telethon import events
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter


@borg.on(admin_cmd(pattern=("tar ?(.*)")))
async def _(event,is_zip):
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
            # out_tar = tardir(directory_name,directory_name )
            to_upload_file = directory_name 
            if is_zip:
                # first check if current free space allows this
                # ref: https://github.com/out386/aria-telegram-mirror-bot/blob/master/src/download_tools/aria-tools.ts#L194
                # archive the contents
                check_if_file = await create_archive(to_upload_file)
                if check_if_file is not None:
                    to_upload_file = check_if_file
            await borg.send_file(
                event.chat_id,
                to_upload_file,
                caption="TAR By @By_Azade",
                force_document=True,
                allow_cache=False,
                reply_to=event.message.id,
            )
            try:
                os.remove(to_upload_file)
                os.remove(to_upload_file)
            except:
                    pass
            await event.edit("Task Completed")
            await asyncio.sleep(3)
            await event.delete()
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.edit(str(e))
    elif input_str:
        directory_name = input_str
        
        await event.edit("Local file compressed to `{}`".format(to_upload_file))

        
# def make_tarfile(output_filename, source_dir):
#     with tarfile.open(output_filename, "w:gz") as tar:
#         tar.add(source_dir, arcname=os.path.basename(source_dir))

# def tardir(path, tar_name):
#     with tarfile.open(tar_name, "w:gz") as tar_handle:
#         for root, dirs, files in os.walk(path):
#             for file in files:
#                 tar_handle.add(os.path.join(root, file))


async def create_archive(input_directory):
    return_name = None
    if os.path.exists(input_directory):
        base_dir_name = os.path.basename(input_directory)
        compressed_file_name = f"{base_dir_name}.tar.gz"
        # #BlameTelegram
        suffix_extention_length = 1 + 3 + 1 + 2
        if len(base_dir_name) > (64 - suffix_extention_length):
            compressed_file_name = base_dir_name[0:(64 - suffix_extention_length)]
            compressed_file_name += ".tar.gz"
        # fix for https://t.me/c/1434259219/13344
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
    return return_name
