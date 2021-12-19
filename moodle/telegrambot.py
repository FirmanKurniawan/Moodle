from telegram.ext import Updater
from moodle import log, TOKEN, CHAT_ID


def send(msg):
    try:
        updater = Updater(TOKEN)
        updater.bot.sendMessage(chat_id=CHAT_ID, text=msg)
    except:
        log.error(
            "Unable to send messasge please check bot chat token,your chat id and /start bot in telegram"
        )
