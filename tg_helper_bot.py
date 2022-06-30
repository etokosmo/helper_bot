import logging
import os
from functools import partial

from environs import Env
from notifiers.logging import NotificationHandler
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, \
    CallbackContext

from dialogflow_intents import detect_intent_texts

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(__file__) or '.'


def error_handler(update: object,
                  context: CallbackContext) -> None:
    """Log the error and send a telegram message to notify the developer."""
    logger.exception(context.error)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )


def process_message(update: Update,
                    context: CallbackContext,
                    project_id: str) -> None:
    """Answer the user message."""
    session_id = str(update.effective_user.id)
    response_message, is_fallback_intent = detect_intent_texts(
        project_id,
        session_id,
        update.message.text,
    )
    update.message.reply_text(response_message)


def main() -> None:
    """Start the bot."""
    logging.basicConfig(
        format='%(asctime)s : %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=logging.INFO
    )

    env = Env()
    env.read_env()
    telegram_api_token = env("TELEGRAM_API_TOKEN")
    telegram_chat_id = env("TELEGRAM_CHAT_ID")

    params = {
        'token': telegram_api_token,
        'chat_id': telegram_chat_id
    }
    tg_handler = NotificationHandler("telegram", defaults=params)
    logger.addHandler(tg_handler)

    GOOGLE_APPLICATION_CREDENTIALS = os.path.join(
        BASE_DIR,
        env("GOOGLE_APPLICATION_CREDENTIALS")
    )
    google_project_id = env("GOOGLE_PROJECT_ID")

    updater = Updater(telegram_api_token)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    process_message_with_args = partial(process_message,
                                        project_id=google_project_id)
    dispatcher.add_handler(
        MessageHandler(Filters.text & ~Filters.command,
                       process_message_with_args))
    dispatcher.add_error_handler(error_handler)
    logger.info('TG-бот запущен.')

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
