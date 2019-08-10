from asyncio import sleep
from telethon.errors import rpcbaseerrors
from sample_config import PRIVATE_GROUP_BOT_API_ID
from telethon import events
import asyncio
import os
import subprocess
import sys
from uniborg.util import admin_cmd, humanbytes, progress, time_formatter

@borg(outgoing=True, pattern="^.sd")
async def selfdestruct(destroy):
    """ For .sd command, make seflf-destructable messages. """
    if not destroy.text[0].isalpha() and destroy.text[0] not in (
            "/", "#", "@", "!"):
        message = destroy.text
        counter = int(message[4:6])
        text = str(destroy.text[6:])
        await destroy.delete()
        smsg = await destroy.client.send_message(destroy.chat_id, text)
        await sleep(counter)
        await smsg.delete()
        if PRIVATE_GROUP_BOT_API_ID:
            await destroy.client.send_message(PRIVATE_GROUP_BOT_API_ID,
                                              "sd query done successfully")
