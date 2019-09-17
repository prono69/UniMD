""" Google Google Translate
Available Commands:
.tr LanguageCode as reply to a message
.tr LangaugeCode | text to sepak"""
from telethon import events
from uniborg import UniBorg as borg
from uniborg.util import admin_cmd

from mtranslate import translate
from sample_config import Config


@borg.on(admin_cmd(pattern="tr ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if "trim" in event.raw_text:
        # https://t.me/c/1220993104/192075
        return
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str
    elif "|" in input_str:
        lan, text = input_str.split("|")
    else:
        await event.edit("Invalid Syntax. Module stopping.")
        return
    text = text.strip()
    lan = lan.strip()
    try:
        translated_text = translate(text, lan)
        output_str = """**SOURCE**
        
`{}`

**TRANSLATED** to {}

`{}`""".format(
            text,
            lan,
            translated_text
        )
        await event.edit(output_str)
    except Exception as exc:
        await event.edit(str(exc))
