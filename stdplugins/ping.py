from telethon import events
from datetime import datetime
from uniborg.util import admin_cmd


@borg.on(admin_cmd("ping"))
async def _(event):
    if event.fwd_from:
        return
    start = datetime.now()
    await event.edit("Pong!")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await borg.send_sticker(event.chat_id, 'CAADBAAD1QIAAlAYNw2Pr-ymr7r8TgI')
    await event.edit("Pong!\n`{}`".format(ms))
