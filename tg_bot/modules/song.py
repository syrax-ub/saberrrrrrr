from tg_bot import oko
import glob
import os
import subprocess
from telethon import types
from telethon.tl import functions
from tg_bot import oko
from tg_bot.events import register






@register(pattern="^/song (.*)")
async def _(event):
    if event.fwd_from:
        return
    

    cmd = event.pattern_match.group(1)
    cmnd = f"{cmd}"
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id
    try:
        subprocess.run(["spotdl", "-s", cmnd, "-q", "best"])
        subprocess.run(
            'for f in *.opus; do      mv -- "$f" "${f%.opus}.mp3"; done', shell=True
        )
        l = glob.glob("*.mp3")
        loa = l[0]
        await event.reply("sending the song")
        await tbot.send_file(
            event.chat_id,
            loa,
            force_document=False,
            allow_cache=False,
            supports_streaming=True,
            caption=cmd,
            reply_to=reply_to_id,
        )
        os.system("rm -rf *.mp3")
    except Exception:
        await event.reply("I am getting too many requests !\nPlease try again later.")
from tg_bot import CMD_HELP
global __help__
global file_helpo
file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo=  file_help.replace("_", " ")

__help__ = """
 - /song <songname artist(optional)>: uploads the song in it's best quality available
"""

CMD_HELP.update({
    file_helpo: [
        file_helpo,
        __help__
    ]
})
