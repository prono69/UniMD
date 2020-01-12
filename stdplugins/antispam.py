#COMBOT ANTI SPAM SYSTEM IS USED
#created for @uniborg (unfinished)

import logging
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)
import os
import sys

from requests import get
from telethon import events
from telethon.events import ChatAction
from telethon.tl.types import ChannelParticipantsAdmins, Message

from sample_config import Config
from uniborg.util import admin_cmd



@borg.on(events.ChatAction())
async def _(cas):
    chat = await cas.get_chat()
    if (chat.admin_rights or chat.creator):
        if cas.user_joined or cas.user_added: 
            user = await cas.get_user()
            id = user.id
            mid = "{}".format(chat.title)
            mention = "[{}](tg://user?id={})".format(user.first_name, user.id) 
            r = get(f'https://combot.org/api/cas/check?user_id={id}') 
            r_dict = r.json() 
            if r_dict['ok']:
                try:                
                    more = r_dict['result']
                    from telethon.tl.types import ChatBannedRights
                    from telethon.tl.functions.channels import EditBannedRequest
                    rights = ChatBannedRights(
                        until_date=None,
                        view_messages=True,
                        send_messages=True
                    )
                    await borg(EditBannedRequest(cas.chat_id, id, rights))
                    await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, "**antispam log** \n**Who**: {} \n**Where**: {} \n**How**: [here](https://combot.org/api/cas/check?user_id={}) \n**Action**: Banned \n**More**: ```{}```".format(mention, mid, id, more),link_preview=True)
                except (Exception) as exc:
                    await borg.send_message(Config.PRIVATE_GROUP_BOT_API_ID, str(exc))
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    print(exc_type, fname, exc_tb.tb_lineno)
                    print(exc)
    else:
        return ""
