import asyncio
import logging
import random
from time import sleep

import vk_api as vk
from environs import Env
from vk_api.longpoll import VkLongPoll, VkEventType

from libs.helper_bot_utils import detect_intent_texts

logging.basicConfig(
    format='%(asctime)s : %(message)s',
    datefmt='%d/%m/%Y %H:%M:%S',
    level=logging.DEBUG
)
logger = logging.getLogger(__name__)


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
    env = Env()
    env.read_env()
    vk_api_token = env("VK_API_TOKEN")
    project_id = env("PROJECT_ID")

    vk_session = vk.VkApi(token=vk_api_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            await process_message(event, vk_api, project_id)


if __name__ == "__main__":
    while True:
        try:
            asyncio.run(main())
        except Exception as error:
            logger.error("Бот упал с ошибкой:")
            logger.error(error)
            sleep(3600)
