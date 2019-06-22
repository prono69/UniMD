# For @UniBorg
# (c) Shrimadhav U K

from telethon import events
import asyncio
import dropbox
import math
import os


DROP_BOX_ACCESS_TOKEN = "XN7uiBFbOMAAAAAAAAAAnT7IdyEOcLZGhoBDwP8qrU98mVdWBMWxhvgttcbGX0ax"
# get your own access token from https://www.dropbox.com/developers/apps/ and fill here


@borg.on(events.NewMessage(pattern=r"\.dropbox (.*)", outgoing=True))
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    if os.path.exists(input_str):
        input_str = os.path.abspath(input_str)
        # https://stackoverflow.com/a/51523/4723940
        dbx = dropbox.Dropbox(DROP_BOX_ACCESS_TOKEN)
        file_name_without_ext = input_str.split(os.path.sep)[-1]
        mode = dropbox.files.WriteMode.add
        file_size = os.path.getsize(input_str)
        await event.edit("""Detected File Size: {}
File Name: {}""".format(humanbytes(file_size), file_name_without_ext))
        # https://stackoverflow.com/a/678242/4723940
        CHUNK_SIZE = 10283
        file_name_without_ext = "/" + file_name_without_ext
        with open(input_str, "rb") as f:
            # https://stackoverflow.com/a/37399658/4723940
            upload_session_start_result = dbx.files_upload_session_start(
                f.read(CHUNK_SIZE))
            cursor = dropbox.files.UploadSessionCursor(
                session_id=upload_session_start_result.session_id, offset=f.tell())
            commit = dropbox.files.CommitInfo(path=file_name_without_ext)
            while f.tell() < file_size:
                if ((file_size - f.tell()) <= CHUNK_SIZE):
                    a = dbx.files_upload_session_finish(
                        f.read(CHUNK_SIZE), cursor, commit)
                else:
                    dbx.files_upload_session_append(
                        f.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                    cursor.offset = f.tell()
        logger.info(a)
        await event.edit("Successfully Uploaded")
    else:
        await event.edit("404: File Not Found")


def humanbytes(size):
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2**10
    n = 0
    Dic_powerN = {0: ' ', 1: 'Ki', 2: 'Mi', 3: 'Gi', 4: 'Ti'}
    while size > power:
        size /= power
        n += 1
    return str(math.floor(size)) + " " + Dic_powerN[n] + 'B'
