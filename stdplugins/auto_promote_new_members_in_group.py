# -*- coding: utf-8 -*-
# (c) @UniBorg

from telethon import events
from telethon.tl.functions.channels import EditAdminRequest
from telethon.tl.types import ChatAdminRights
import os

CHAT_AP_JOIN_PP = os.environ.get("CHAT_AP_JOIN_PP", "")
CHAT_AP_JOIN_PP_ARRY = [int(c) for c in CHAT_AP_JOIN_PP.split(" ")]


@borg.on(events.ChatAction(chats=CHAT_AP_JOIN_PP_ARRY))
async def auto_promote_new_joiners(event):
	if event.user_joined:
		rights = ChatAdminRights(
			post_messages=True
		)
		# https://t.me/telethonofftopic/93334
		user_ids = event.action_message.action.users
		for user_id in user_ids:
			try:
				await borg(EditAdminRequest(event.chat_id, user_id, rights))
			except (Exception) as exc:
				await event.respond(str(exc))
				continue
		await event.delete()
