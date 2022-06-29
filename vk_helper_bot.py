import asyncio
import logging
import os
import random

import vk_api as vk
from environs import Env
from notifiers.logging import NotificationHandler
from vk_api.longpoll import VkLongPoll, VkEventType

from libs.helper_bot_utils import detect_intent_texts

logger = logging.getLogger(__name__)
BASE_DIR = os.path.dirname(__file__) or '.'


async def process_message(event: vk.longpoll.Event,
                          vk_api: vk.vk_api.VkApiMethod,
                          project_id: str) -> None:
    """Answer the user message."""
    response_message = await detect_intent_texts(
        project_id,
        event.user_id,
        event.text,
        social_network="vk"
    )
    if response_message:
        vk_api.messages.send(
            user_id=event.user_id,
            message=response_message,
            random_id=random.randint(1, 1000)
        )


async def main():
    """Start the bot."""
    logging.basicConfig(
        format='%(asctime)s : %(message)s',
        datefmt='%d/%m/%Y %H:%M:%S',
        level=logging.INFO
    )
    env = Env()
    env.read_env()
    vk_api_token = env("VK_API_TOKEN")
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

    vk_session = vk.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    logger.info('VK-бот запущен.')

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            await process_message(event, vk_api, google_project_id)


if __name__ == "__main__":
    asyncio.run(main())
