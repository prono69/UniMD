# import asyncio
# import os
# import shutil
# import subprocess
# import time
# from pySmartDL import SmartDL
# from sample_config import Config
# from telethon import events
# from uniborg.util import admin_cmd, humanbytes, progress, time_formatter
# import subprocess
# import patoolib
# from hachoir.metadata import extractMetadata
# from hachoir.parser import createParser
# from telethon.tl.types import DocumentAttributeAudio, DocumentAttributeVideo
# from youtube_dl import YoutubeDL
# from youtube_dl.utils import (DownloadError, ContentTooShortError,
#                               ExtractorError, GeoRestrictedError,
#                               MaxDownloadsReached, PostProcessingError,
#                               UnavailableVideoError, XAttrMetadataError)


# thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


# @borg.on(admin_cmd(pattern=("playlistd ?(.*)")))
# async def _(event):
#     if event.fwd_from:
#         return
#     url = event.pattern_match.group(1)
#     if not os.path.isdir("./DOWNLOAD/Playlist/"):
#         os.makedirs("./DOWNLOAD/Playlist/")
#     output = "./DOWNLOAD/Playlist/"
#     thumb_image_path = Config.TMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"
#     mone = await event.edit("Processing ...")
#     if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
#         os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
#     if event.reply_to_msg_id:
#         reply_message = await event.get_reply_message()
#         c_time = time.time()
#         command_to_exec = [
#                 "youtube-dl",
#                 "-t",
#                 "--extract-audio",
#                 "--audio-format",
#                 "mp3",
#                 f"{url}",
#                 "-o",
#                 f"{output}"
#                 ]
#         sp = subprocess.Popen(command_to_exec, stderr=subprocess.STDOUT, stdout=subprocess.PIPE)
#         try:
#             await event.edit("`Fetching data, please wait..`")
#             with YoutubeDL(command_to_exec) as ytdl:
#                 ytdl_data = ytdl.extract_info(url)
#         except DownloadError as DE:
#             await event.edit(f"`{str(DE)}`")
#             return
#         except ContentTooShortError:
#             await event.edit("`The download content was too short.`")
#             return
#         except GeoRestrictedError:
#             await event.edit(
#             "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
#             )
#             return
#         except MaxDownloadsReached:
#             await event.edit("`Max-downloads limit has been reached.`")
#             return
#         except PostProcessingError:
#             await event.edit("`There was an error during post processing.`")
#             return
#         except UnavailableVideoError:
#             await event.edit("`Media is not available in the requested format.`")
#             return
#         except XAttrMetadataError as XAME:
#             await event.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
#             return
#         except ExtractorError:
#             await event.edit("`There was an error during info extraction.`")
#             return
#         except Exception as e:
#             await event.edit(f"{str(type(e)): {str(e)}}")
#             return
#         logger.info(command_to_exec)
#         filename = sorted(get_lst_of_files(output, []))
#         for single_file in filename:
#             if os.path.exists(single_file):

#                 # https://stackoverflow.com/a/678242/4723940
#                 caption_rts = os.path.basename(single_file)
#                 force_document = True
#                 supports_streaming = False
#                 document_attributes = []
#                 if single_file.endswith((".mp4", ".mp3", ".flac", ".webm")):
#                     metadata = extractMetadata(createParser(single_file))
#                     duration = 0
#                     width = 0
#                     height = 0
#                     if metadata.has("duration"):
#                         duration = metadata.get('duration').seconds
#                     if os.path.exists(thumb_image_path):
#                         metadata = extractMetadata(createParser(thumb_image_path))
#                         if metadata.has("width"):
#                             width = metadata.get("width")
#                         if metadata.has("height"):
#                             height = metadata.get("height")
#                     document_attributes = [
#                         DocumentAttributeVideo(
#                             duration=duration,
#                             w=width,
#                             h=height,
#                             round_message=False,
#                             supports_streaming=True
#                         )
#                     ]
#                 try:
#                     await borg.send_file(
#                         event.chat_id,
#                         single_file,
#                         caption=f" `{caption_rts}`",
#                         force_document=force_document,
#                         supports_streaming=supports_streaming,
#                         allow_cache=False,
#                         reply_to=event.message.id,
#                         attributes=document_attributes,
#                         # progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
#                         #     progress(d, t, event, c_time, "trying to upload")
#                         # )
#                     )
#                 except Exception as e:
#                     await borg.send_message(
#                         event.chat_id,
#                         "{} caused `{}`".format(caption_rts, str(e)),
#                         reply_to=event.message.id
#                     )
#                     # some media were having some issues
#                     continue
#                 os.remove(single_file)
#         os.remove(output)


# def get_lst_of_files(input_directory, output_lst):
#     filesinfolder = os.listdir(input_directory)
#     for file_name in filesinfolder:
#         current_file_name = os.path.join(input_directory, file_name)
#         if os.path.isdir(current_file_name):
#             return get_lst_of_files(current_file_name, output_lst)
#         output_lst.append(current_file_name)
#     return output_lst




"""
Audio and video downloader using Youtube-dl
.yta To Download in mp3 format
.ytv To Download in mp4 format
"""

import os
import time
import math
import asyncio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (DownloadError, ContentTooShortError,
                              ExtractorError, GeoRestrictedError,
                              MaxDownloadsReached, PostProcessingError,
                              UnavailableVideoError, XAttrMetadataError)
from asyncio import sleep
from telethon.tl.types import DocumentAttributeAudio
from uniborg.util import admin_cmd

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

@borg.on(admin_cmd(pattern="playlist(a|v) (.*)"))
async def download_video(v_url):
    """ For .ytdl command, download media from YouTube and many other sites. """
    url = v_url.pattern_match.group(2)
    type = v_url.pattern_match.group(1).lower()

    await v_url.edit("`Preparing to download...`")

    if type == "a":
        opts = {
            '-citk',
            '--max-quality',
            'mp3',
            '--extract-audio',
            '--audio-format',
            'mp3',
            f'{url}'
        }
        video = False
        song = True

    elif type == "v":
        opts = {
            'format':
            'best',
            'addmetadata':
            True,
            'key':
            'FFmpegMetadata',
            'prefer_ffmpeg':
            True,
            'geo_bypass':
            True,
            'nocheckcertificate':
            True,
            'postprocessors': [{
                'key': 'FFmpegVideoConvertor',
                'preferedformat': 'mp4'
            }],
            'outtmpl':
            '%(id)s.mp4',
            'logtostderr':
            False,
            'quiet':
            True
        }
        song = False
        video = True

    try:
        await v_url.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as ytdl:
            ytdl_data = ytdl.extract_info(url)
    except DownloadError as DE:
        await v_url.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await v_url.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await v_url.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await v_url.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await v_url.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await v_url.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await v_url.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await v_url.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await v_url.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await v_url.edit(f"`Preparing to upload song:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(duration=int(ytdl_data['duration']),
                                       title=str(ytdl_data['title']),
                                       performer=str(ytdl_data['uploader']))
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{ytdl_data['title']}.mp3")))
        os.remove(f"{ytdl_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await v_url.edit(f"`Preparing to upload video:`\
        \n**{ytdl_data['title']}**\
        \nby *{ytdl_data['uploader']}*")
        await v_url.client.send_file(
            v_url.chat_id,
            f"{ytdl_data['id']}.mp4",
            supports_streaming=True,
            caption=ytdl_data['title'],
            progress_callback=lambda d, t: asyncio.get_event_loop(
            ).create_task(
                progress(d, t, v_url, c_time, "Uploading..",
                         f"{ytdl_data['title']}.mp4")))
        os.remove(f"{ytdl_data['id']}.mp4")
        await v_url.delete()