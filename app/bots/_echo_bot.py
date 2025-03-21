from requests.cookies import extract_cookies_to_jar
from trueconf import Bot, Dispatcher, Router, F, Message

from trueconf.enums import MessageType
import logging

from app.config import config
from app.localization import _

logger = logging.getLogger("chat_bot")

r = Router(name="echo_bot")

@r.message()
async def echo_text(message: Message):
    await message.answer(text=message.text, parse_mode=message.content.parse_mode)


@r.message(F.type == MessageType.ATTACHMENT)
async def echo_attachment(message: Message):
    await message.reply(_("errors.no_files"))

dp = Dispatcher()

dp.include_router(r)

echo_bot = Bot.from_credentials(
    username=config.echo_bot.username,
    password=config.echo_bot.password,
    server=config.server_address,
    dispatcher=dp,
    verify_ssl=False,
)

