import logging
import os
from functools import partial
from time import sleep

from environs import Env
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, \
    MessageHandler, filters

from libs.helper_bot_utils import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s : %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(__file__) or '.'


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Здравствуйте, {user.mention_html()}! Чем можем помочь?",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update,
                       context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def process_message(update: Update,
                          context: ContextTypes.DEFAULT_TYPE,
                          project_id: str) -> None:
    """Answer the user message."""
    session_id = str(update.effective_user.id)
    response_message = await detect_intent_texts(
        project_id,
        session_id,
        update.message.text,
        social_network="tg"
    )
    await update.message.reply_text(response_message)


def main() -> None:
    """Start the bot."""
    env = Env()
    env.read_env()
    telegram_api_token = env("TELEGRAM_API_TOKEN")
    GOOGLE_APPLICATION_CREDENTIALS = os.path.join(
        BASE_DIR,
        "secret",
        env("GOOGLE_APPLICATION_CREDENTIALS")
    )
    project_id = env("PROJECT_ID")

    application = Application.builder().token(telegram_api_token).build()
    process_message_with_args = partial(process_message, project_id=project_id)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND,
                       process_message_with_args))

    application.run_polling()


if __name__ == "__main__":
    main()
    while True:
        try:
            main()
        except Exception as error:
            logger.error("Бот упал с ошибкой:")
            logger.error(error)
            sleep(3600)
