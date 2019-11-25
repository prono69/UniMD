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
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser




@borg.on(admin_cmd(pattern=("playlistd ?(.*)")))
async def _(event):
    if event.fwd_from:
        return
    url = event.pattern_match.group(1)
    if not os.path.isdir("./DOWNLOAD/Playlist/"):
        os.makedirs("./DOWNLOAD/Playlist/")
    output = "./DOWNLOAD/Playlist/"
    thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    mone = await event.edit("Processing ...")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            command_to_exec = [
                    "./bin/youtubeplaylist.py",
                    f"{url}",
                    f"{output}"
                    ]
            sp = subprocess.Popen(command_to_exec, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
            filename = sorted(get_lst_of_files(output, []))
            for single_file in filename:
                if os.path.exists(single_file):
                    # https://stackoverflow.com/a/678242/4723940
                    caption_rts = os.path.basename(single_file)
                    force_document = True
                    supports_streaming = False
                    document_attributes = []
                    if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
                        metadata = extractMetadata(createParser(single_file))
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
                        document_attributes = [
                            DocumentAttributeVideo(
                                duration=duration,
                                w=width,
                                h=height,
                                round_message=False,
                                supports_streaming=True
                            )
                        ]
                    try:
                        await borg.send_file(
                            event.chat_id,
                            single_file,
                            caption=f" `{caption_rts}`",
                            force_document=force_document,
                            supports_streaming=supports_streaming,
                            allow_cache=False,
                            reply_to=event.message.id,
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
            os.remove(output)







def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst