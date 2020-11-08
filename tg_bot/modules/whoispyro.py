"""Get info about the replied user
Syntax: .whois"""
from datetime import datetime

from pyrogram import filters
from pyrogram.types import User, Message
from pyrogram.raw import functions
from tg_bot.helper_funcs.extract_user
from pyrogram.errors import PeerIdInvalid
from tg_bot import pbot
import os
import time

@Client.on_message(
    filters.command(whois)
)
async def who_is(client, message):
    """ extract user information """
    status_message = await message.reply_text(
        "🤔😳😳🙄"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        user_id = from_user_id
        if not str(user_id).startswith("@"):
            user_id = int(user_id)
        from_user = await client.get_users(user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        await status_message.edit("no valid user_id / message specified")
    else:
        message_out_str = ""
        message_out_str += f"ID: <code>{from_user.id}</code>\n"
        message_out_str += "First Name: "
        message_out_str += f"<a href='tg://user?id={from_user.id}'>"
        message_out_str += from_user.first_name or ""
        message_out_str += "</a>\n"
        last_name = from_user.last_name or ""
        message_out_str += f"Last Name: {last_name}\n"
        dc_id = from_user.dc_id or "[🙏 no profile photo 👀]"
        message_out_str += f"DC ID: <code>{dc_id}</code>\n"
        if message.chat.type in (("supergroup", "channel")):
            try:
                chat_member_p = await message.chat.get_member(from_user.id)
                joined_date = datetime.fromtimestamp(
                    chat_member_p.joined_date or time.time()
                ).strftime("%Y.%m.%d %H:%M:%S")
                message_out_str += (
                    "<b>Joined On</b>: <code>"
                    f"{joined_date}"
                    "</code>\n"
                )
            except UserNotParticipant:
                pass
        chat_photo = from_user.photo
        if chat_photo:
            local_user_photo = await client.download_media(
                message=chat_photo.big_file_id
            )
            await message.reply_photo(
                photo=local_user_photo,
                quote=True,
                caption=message_out_str,
                parse_mode="html",
                # ttl_seconds=,
                disable_notification=True
            )
            os.remove(local_user_photo)
        else:
            await message.reply_text(
                text=message_out_str,
                quote=True,
                parse_mode="html",
                disable_notification=True
            )
        await status_message.delete()
