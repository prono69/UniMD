
#    This file is part of NiceGrill.

#    NiceGrill is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    NiceGrill is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with NiceGrill.  If not, see <https://www.gnu.org/licenses/>.


#Ported to ftg by @Nihinivi
#Thanks to @emillybennetty for this amazing template
#And fkin dont edit the credits
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import textwrap
import urllib
import logging
import os
import asyncio
import datetime
from telethon import events
from telethon.tl import functions, types
from uniborg.util import admin_cmd
class Quote:


    async def process(msg, reply, client):
        if not os.path.isdir(".tmp"):
            os.mkdir(".tmp", 0o755)
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/pfp.jpg',
                '.tmp/pfp.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/top.jpg',
                '.tmp/top.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/mid.jpg',
                '.tmp/mid.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/bottom.jpg',
                '.tmp/bottom.jpg')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Medium.ttf',
                '.tmp/Roboto-Medium.ttf')
            urllib.request.urlretrieve(
                'https://github.com/erenmetesar/modules-repo/raw/master/Roboto-Regular.ttf',
                '.tmp/Roboto-Regular.ttf')
            urllib.request.urlretrieve("https://github.com/rebel6969/modules-repo/raw/master/Telegram.jpg",".tmp/lol.png")
            urllib.request.urlretrieve("https://github.com/rebel6969/mym/raw/master/Rebel-robot-Regular.ttf",".tmp/Fuck.ttf")
            
            
            
            
        top = Image.open(".tmp/top.jpg", "r").convert('RGBA')
        mid = Image.open(".tmp/mid.jpg", "r").convert('RGBA')
        bottom = Image.open(".tmp/bottom.jpg", "r").convert('RGBA')

        msg = reply.message
        msg = msg.replace("\n", "\\\\n").replace("*","").replace("`","").replace("_","")
        text = []
        for i in textwrap.wrap(msg, 43):
            text = text + i.replace("\\\\n", "\n").split("\n")
        midh = mid.height - 20

        for line in text:
            mid = mid.resize((mid.width, midh + 40))
            midh += 40
    
        dlpfp = await client.download_profile_photo(reply.sender_id)


        
        
        if dlpfp == None:
            paste = Image.open(".tmp/lol.png")
        else:
            paste = Image.open(dlpfp)
            os.system("rm -rf *.png")

        
        pfp = Image.open(".tmp/pfp.jpg")
        paste.thumbnail((110, 115))

        # MASK
        mask_im = Image.new("L", paste.size, 0)
        draw = ImageDraw.Draw(mask_im)
        draw.ellipse((0, 0, 110, 115), fill=255)

        # APPLY MASK
        pfpbg = pfp.copy()
        pfp = mask_im.copy()
        pfpbg.paste(paste, (10, 20), mask_im)

        canvas = Image.new(
            'RGB',
            (top.width
             + pfpbg.width,
             top.height
             + mid.height
             + bottom.height))
        canvas.paste(pfpbg, (0, 0))
        canvas.paste(top, (pfpbg.width, 0))
        canvas.paste(mid, (pfpbg.width, top.height))
        canvas.paste(bottom, (pfpbg.width, top.height + mid.height))

        canvas.resize((canvas.width - 100, canvas.height))

        draw = ImageDraw.Draw(canvas)
        font = ImageFont.truetype(".tmp/Fuck.ttf", 48)
        font2 = ImageFont.truetype(".tmp/Roboto-Regular.ttf", 42)

        lname = "" if not reply.sender.last_name else reply.sender.last_name
        tot = reply.sender.first_name + " " + lname

        draw.text((pfp.width + 70, 40), tot, font=font, fill='#E9967A')

        lnh = 70
        for line in text:
            draw.text((pfp.width + 70, lnh + 40),
                      line, font=font2, fill='white')
            lnh += 40
        return True, canvas



@borg.on(admin_cmd(pattern="quote"))
async def quotexxx(message):
    
        await message.delete()
        reply = await message.get_reply_message()
        res, canvas = await Quote.process(reply.message, reply, message.client)
        if not res:
            return
        canvas.save('.tmp/done.webp')
        await message.client.send_file(message.chat_id, ".tmp/done.webp")
