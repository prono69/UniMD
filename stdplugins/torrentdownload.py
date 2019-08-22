from qbittorrent import Client
import asyncio
import io
import os
from uniborg.util import admin_cmd


qbittorrent_port = 6800
qb = Client(
    host="http://localhost",
    port=qbittorrent_port,
    secret=""
)

qb.login('admin', 'your-secret-password')
# not required when 'Bypass from localhost' setting is active.
# defaults to admin:admin.
# to use defaults, just do qb.login()
torrents = qb.torrents()

@borg.on(admin_cmd("addmagne"))
async def magnet_download(event):
    if event.fwd_from:
        return
    var = event.raw_text
    var = var.split("")
    magnet_uri = var[1]
    try:
        download = qb.download_from_link(magnet_uri)
    except Exception as e:
        await event.edit("pls send correct magnet link")
        return
    m = await event.reply("downloading now, if you want to see downloading status use .status")
    await asyncio.sleep(5)
    await m.delete()
