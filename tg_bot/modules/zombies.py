
from asyncio import sleep


from telethon.errors import (BadRequestError, ChatAdminRequiredError,
                             ImageProcessFailedError, PhotoCropSizeSmallError,
                             UserAdminInvalidError)
from telethon.errors.rpcerrorlist import UserIdInvalidError
from telethon.tl.functions.channels import (EditAdminRequest,
                                            EditBannedRequest,
                                            EditPhotoRequest)
from telethon.tl.types import (ChannelParticipantsAdmins, ChatAdminRights,
                               ChatBannedRights, MessageEntityMentionName,
                               MessageMediaPhoto)
from telethon import events
from tg_bot import oko

@oko.on(events.NewMessage(pattern="^[!/]deluser$"))
async def rm_deletedacc(event):
    """ For .adminlist command, list all of the admins of the chat. """
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        con = event.pattern_match.group(1)
        del_u = 0
        del_status = "`No deleted accounts found, Group is cleaned as Hell`"

        if not event.is_group:
            await event.reply("`This command is only for groups!`")
            return

        if con != "clean":
            await event.reply("`Searching for zombie accounts...`")
            async for user in event.client.iter_participants(
                    event.chat_id
            ):
                if user.deleted:
                    del_u += 1

            if del_u > 0:
                del_status = f"found **{del_u}** deleted account(s) in this group \
                \nclean them by using .delusers clean"
            await event.reply(del_status)
            return

        # Here laying the sanity check
        chat = await event.get_chat()
        admin = chat.admin_rights
        creator = chat.creator

        # Well
        if not admin and not creator:
            await event.reply("`You aren't an admin here!`")
            return

        await event.reply("`Cleaning deleted accounts...`")
        del_u = 0
        del_a = 0

        async for user in event.client.iter_participants(
                event.chat_id
        ):
            if user.deleted:
                try:
                    await event.client(
                        EditBannedRequest(
                            event.chat_id,
                            user.id,
                            BANNED_RIGHTS
                        )
                    )
                except ChatAdminRequiredError:
                    await event.reply("`you don't have ban rights in this group`")
                    return
                except UserAdminInvalidError:
                    del_u -= 1
                    del_a += 1
                await show.client(
                    EditBannedRequest(
                        show.chat_id,
                        user.id,
                        UNBAN_RIGHTS
                    )
                )
                del_u += 1

        if del_u > 0:
            del_status = f"cleaned **{del_u}** deleted account(s)"

        if del_a > 0:
            del_status = f"cleaned **{del_u}** deleted account(s) \
            \n**{del_a}** deleted admin accounts are not removed"

        await event.reply(del_status)
