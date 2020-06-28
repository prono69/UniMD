import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import asyncio
import json
import os
import time
from datetime import datetime

import requests
from sample_config import Config
#
from telethon import events
from uniborg.util import admin_cmd, humanbytes, progress

api = Config.VIRUSTOTAL_API_KEY

@borg.on(admin_cmd(pattern="virustotal ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.edit("Processing ...")
    input_str = event.pattern_match.group(1)
    url = input_str
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            params = {
                'apikey': str(api),
                'url': str(url)
            }
            response = requests.post(url,data=params)
        except Exception as e:
            await mone.edit(str(e))
            return False
        if response:
            try:
                response = json.dumps(json.loads(response), sort_keys=True, indent=6)
            except Exception as e:
                # some sites don't return valid JSONs
                pass
            # assuming, the return values won't be longer than
            # 4096 characters
            await event.edit(response)





