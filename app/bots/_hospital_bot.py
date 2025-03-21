import toml

from app.config import config
from trueconf import Bot, Dispatcher, Router, F, Message
from trueconf.enums import MessageType, ParseMode
from trueconf.types.requests import CreatedGroupChat
from app.localization import _

import logging

logger = logging.getLogger("chat_bot")

r = Router(name="hospital_bot")
dp = Dispatcher()

dp.include_router(r)

hospital_bot = Bot.from_credentials(
    username=config.hospital_bot.username,
    password=config.hospital_bot.password,
    server=config.server_address,
    dispatcher=dp,
    verify_ssl=False,
)

@r.created_group_chat()
async def chat_created(message: CreatedGroupChat):

    chat_id = message.chat_id
    name = message.title

    config.hospital_bot.chat_id = chat_id
    config.hospital_bot.chat_name = name
    toml.dump(config.model_dump(), open("config.toml", "w"))

    await hospital_bot.send_message(chat_id=chat_id, text=_("message.hospital_bot.greeting"))


@r.message(MessageType.PLAIN_MESSAGE)
async def handle_hospital(message: Message):
    await hospital_bot.forward_message(
        chat_id=config.hospital_bot.chat_id, 
        message_id=message.message_id
        )



@r.message(MessageType.ATTACHMENT)
async def attachment_handler(message: Message):
    await message.answer(text=_("message.no_files"), parse_mode=ParseMode.HTML)
