import html
import random
import tg_bot.modules.truth_and_dare_string as truth_and_dare_string
import tg_bot.modules.fun_strings as fun_strings
from tg_bot import dispatcher
from telegram import ParseMode, Update, Bot
from tg_bot.modules.helper_funcs.chat_status import is_user_admin
from tg_bot.modules.helper_funcs.extraction import extract_user
from tg_bot.modules.disable import DisableAbleCommandHandler
from telegram.ext import run_async


@run_async
def truth(bot: Bot, update: Update):
    update.effective_message.reply_text(random.choice(truth_and_dare_string.TRUTH))

@run_async
def dare(bot: Bot, update: Update):
    update.effective_message.reply_text(random.choice(truth_and_dare_string.DARE))

@run_async
def runs(bot: Bot, update: Update):
    update.effective_message.reply_text(random.choice(fun_strings.RUN_STRINGS))


@run_async
def slap(bot: Bot, update):
    message = update.effective_message
    chat = update.effective_chat

    reply_text = message.reply_to_message.reply_text if message.reply_to_message else message.reply_text

    curr_user = html.escape(message.from_user.first_name)
    user_id = extract_user(message, args)

    if user_id == bot.id:
        temp = random.choice(fun_strings.SLAP_SAITAMA_TEMPLATES)

        if isinstance(temp, list):
            if temp[2] == "tmute":
                if is_user_admin(chat, message.from_user.id):
                    reply_text(temp[1])
                    return

                mutetime = int(time.time() + 60)
                bot.restrict_chat_member(chat.id, message.from_user.id, until_date=mutetime, can_send_messages=False)
            reply_text(temp[0])
        else:
            reply_text(temp)
        return

    if user_id:

        slapped_user = bot.get_chat(user_id)
        user1 = curr_user
        user2 = html.escape(slapped_user.first_name)

    else:
        user1 = bot.first_name
        user2 = curr_user

    temp = random.choice(fun_strings.SLAP_TEMPLATES)
    item = random.choice(fun_strings.ITEMS)
    hit = random.choice(fun_strings.HIT)
    throw = random.choice(fun_strings.THROW)

    reply = temp.format(user1=user1, user2=user2, item=item, hits=hit, throws=throw)

    reply_text(reply, parse_mode=ParseMode.HTML))


TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare)
SLAP_HANDLER = DisableAbleCommandHandler("slap", slap, pass_args=True

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
dispatcher.add_handler(SLAP_HANDLER)

