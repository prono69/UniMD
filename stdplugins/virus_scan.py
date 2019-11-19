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

@borg.on(admin_cmd(pattern="scan ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    url = event.pattern_match.group(2)
    input_str = event.pattern_match.group(2)
    if  input_str:
        reply_message = await event.get_reply_message()
        try:
            params = {
                'apikey': f'{api}',
                'url':f'{url}'
            }
            response = requests.post(url,data=params)
        except Exception as e:
            await mone.edit(str(e))
            return False
        else:
            pass
    
        if response:
            try:
                response = json.dumps(json.loads(response), sort_keys=True, indent=6)
            except Exception as e:
                # some sites don't return valid JSONs
                pass
            # assuming, the return values won't be longer than
            # 4096 characters
            await event.edit(response)





