import html
import random
import tg_bot.modules.truth_and_dare_string as truth_and_dare_string
from tg_bot import dispatcher
from telegram import ParseMode, Update, Bot
from tg_bot.modules.disable import DisableAbleCommandHandler
from telegram.ext import run_async


@run_async
def animeqoute(bot: Bot, update: Update):
    update.effective_message.reply_text(random.choice(truth_and_dare_string.qoute))


ANIMEQOUTE_HANDLER = DisableAbleCommandHandler("animeqoute", animeqoute)

dispatcher.add_handler(ANIMEQOUTE_HANDLER)
