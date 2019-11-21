"""
Audio and video downloader using Youtube-dl
.yta To Download in mp3 format
.ytv To Download in mp4 format
"""

import os
import time
import math
import asyncio
import shutil
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from asyncio import sleep
from telethon.tl.types import DocumentAttributeAudio
from uniborg.util import admin_cmd
from sample_config import Config


@borg.on(admin_cmd(pattern="ytp(v|a) (.*)"))
async def download_video(v_url):
    """ For .ytp command, download media from YouTube and many other sites. """
    return_name = None
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    playlist_folder = Config.TMP_DOWNLOAD_DIRECTORY + "playlist_folder/"
    thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
    if not os.path.isdir(playlist_folder):
        os.makedirs(playlist_folder)

    if os.path.exists(playlist_folder):
        base_dir_name = os.path.basename(playlist_folder)
    await v_url.edit("`Preparing to download...`")
    filename = sorted(get_lst_of_files(playlist_folder, []))
    if type == "a":
        ytdl_playlist_cmd = [
                "youtube-dl",
                "-i",
                "-f",
                "mp4",
                "--yes-playlist",
                playlist_folder,
                f"{url}"
            ]
    elif type == "v":
        ytdl_playlist_cmd = [
                "youtube-dl",
                "-i",
                "-f",
                "mp3",
                "--yes-playlist",
                playlist_folder,
                f"{url}"
            ]
    process = await asyncio.create_subprocess_exec(
        *ytdl_playlist_cmd,
            # stdout must a pipe to be accessible as process.stdout
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
    stdout, stderr = await process.communicate()
    e_response = stderr.decode().strip()
    t_response = stdout.decode().strip()
    if os.path.exists(playlist_folder):
        try:
            shutil.rmtree(playlist_folder)
        except:
            pass
        return_name = playlist_folder
    return return_name


    
    for single_file in filename:
        if os.path.exists(single_file):
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
                await v_url.send_file(
                    v_url.event.chat_id,
                    single_file,
                    caption=f"`{caption_rts}`",
                    force_document=force_document,
                    supports_streaming=supports_streaming,
                    allow_cache=False,
                    reply_to=v_url.message.id,
                    attributes=document_attributes,                   
                )
            except Exception as e:
                await v_url.send_message(
                    v_url.chat_id,
                    "{} caused `{}`".format(caption_rts, str(e)),
                    reply_to=v_url.message.id
                )
                continue
            os.remove(single_file)



def get_lst_of_files(input_directory, output_lst):
    filesinfolder = os.listdir(input_directory)
    for file_name in filesinfolder:
        current_file_name = os.path.join(input_directory, file_name)
        if os.path.isdir(current_file_name):
            return get_lst_of_files(current_file_name, output_lst)
        output_lst.append(current_file_name)
    return output_lst


async def progress(current, total, event, start, type_of_ps, file_name=None):
    """Generic progress_callback for uploads and downloads."""
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion
        progress_str = "{0}{1} {2}%\n".format(
            ''.join(["█" for i in range(math.floor(percentage / 10))]),
            ''.join(["░" for i in range(10 - math.floor(percentage / 10))]),
            round(percentage, 2))
        tmp = progress_str + \
            "{0} of {1}\nETA: {2}".format(
                humanbytes(current),
                humanbytes(total),
                time_formatter(estimated_total_time)
            )
        if file_name:
            await event.edit("{}\nFile Name: `{}`\n{}".format(
                type_of_ps, file_name, tmp))
        else:
            await event.edit("{}\n{}".format(type_of_ps, tmp))


def humanbytes(size):
    """Input size in bytes,
    outputs in a human readable format"""
    # https://stackoverflow.com/a/49361727/4723940
    if not size:
        return ""
    # 2 ** 10 = 1024
    power = 2**10
    raised_to_pow = 0
    dict_power_n = {0: "", 1: "Ki", 2: "Mi", 3: "Gi", 4: "Ti"}
    while size > power:
        size /= power
        raised_to_pow += 1
    return str(round(size, 2)) + " " + dict_power_n[raised_to_pow] + "B"


def time_formatter(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " day(s), ") if days else "") + \
        ((str(hours) + " hour(s), ") if hours else "") + \
        ((str(minutes) + " minute(s), ") if minutes else "") + \
        ((str(seconds) + " second(s), ") if seconds else "") + \
        ((str(milliseconds) + " millisecond(s), ") if milliseconds else "")
    return tmp[:-2]

# playlist_folder = Config.TMP_DOWNLOAD_DIRECTORY + "playlist_folder/"
# thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"

# async def download_playlist(input_directory,url):
#     return_name = None
#     if os.path.exists(playlist_folder):
#         base_dir_name = os.path.basename(playlist_folder)
#         compressed_file_name = f"{base_dir_name}.tar.gz"
#         # #BlameTelegram
#         suffix_extention_length = 1 + 3 + 1 + 2
#         if len(base_dir_name) > (64 - suffix_extention_length):
#             compressed_file_name = base_dir_name[0:(64 - suffix_extention_length)]
#             compressed_file_name += ".tar.gz"
#         # fix for https://t.me/c/1434259219/13344
#         ytdl_playlist_cmd = [
#                 "youtube-dl",
#                 "-i",
#                 "-f",
#                 "mp4",
#                 "--yes-playlist",
#                 playlist_folder,
#                 f"{url}"
#             ]
#         process = await asyncio.create_subprocess_exec(
#             *ytdl_playlist_cmd,
#             # stdout must a pipe to be accessible as process.stdout
#             stdout=asyncio.subprocess.PIPE,
#             stderr=asyncio.subprocess.PIPE,
#         )
#         # Wait for the subprocess to finish
#         stdout, stderr = await process.communicate()
#         e_response = stderr.decode().strip()
#         t_response = stdout.decode().strip()
#         if os.path.exists(compressed_file_name):
#             try:
#                 shutil.rmtree(input_directory)
#             except:
#                 pass
#             return_name = compressed_file_name
#     return return_name
        