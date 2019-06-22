"""
Google Dictionary Scraper Plugin for Userbot // cuz U-dictonary spitting out random stuff . i was nearly gonna ban from some groups cuz of that. 
usage = .dict word
By : - @Zero_cool7870

"""
import asyncio
import json
import os
import sys

import requests
from bs4 import BeautifulSoup as bs
from telethon import events


@borg.on(events.NewMessage(pattern=r"\.dict", outgoing=True))
async def meme(event):
	if event.fwd_from:
		return
	word = event.text
	word = word[6:]
	await event.edit("**Processing...**")
	res = requests.get("https://googledictionaryapi.eu-gb.mybluemix.net/?define="+word)
	#json_string = json.dumps(res.text)
	try:
		data = json.loads(res.text)
		json_data = ""
		for i in data:
			json_data = i
		regex = ["{","}","[","]",",","'"]
		var = ""	 
		json_data =str(json_data)
		for i in regex:
			json_data = json_data.replace(i,var) 
		json_data = json_data.replace(":",":\n")
		await event.edit("**Google Dictionary Data :-- \n"+json_data+"**")
	except:
		await event.edit("**Not Found!**")
