import httpx
from trueconf.filters import Command

from app.config import config
from trueconf import Bot, Dispatcher, Router, Message
from trueconf.enums import ParseMode
from app.utils import handle_server_error
from app.localization import _

import logging

logger = logging.getLogger("chat_bot")

r = Router(name="monitoring_bot")
dp = Dispatcher()

dp.include_router(r)

monitoring_bot = Bot.from_credentials(
    username=config.monitoring_bot.username,
    password=config.monitoring_bot.password,
    server=config.server_address,
    dispatcher=dp,
    verify_ssl=False,
)

def color_for_cpu_usage(cpu_usage:int) -> str:

    if cpu_usage > 80:
        return "🟥"
    elif cpu_usage > 50:
        return "🟨"
    else:
        return "🟩"


async def get_current_stats(server, access_token):
    async with httpx.AsyncClient(verify=False) as client:
        params = {
            "access_token": access_token,
        }

        response = await client.get(
            f"https://{server}/api/v4/product/current-stats",
            params=params,
        )

        if response.status_code != 200:
            new_token = await handle_server_error(response, server)
            return await get_current_stats(server, new_token)

        return response.json()["stats"]


@r.message(Command("/online"))
async def online_users(message: Message):

    stats_ = await get_current_stats(
        config.server_address,
        config.monitoring_bot.access_token,
    )

    online_users_count = stats_["users"]

    await message.answer(
        text="\n\n".join([
            _("message.monitoring_bot.online", online_users_count=online_users_count),
            _("message.monitoring_bot.info_update")]),
        parse_mode=ParseMode.MARKDOWN,
    )


@r.message(Command("/participants"))
async def participants(message: Message):

    stats_ = await get_current_stats(
        config.server_address,
        config.monitoring_bot.access_token,
    )

    participants_count = stats_["participants"]

    await message.answer(
        text="\n\n".join([
            _("message.monitoring_bot.participants", participants_count=participants_count),
            _("message.monitoring_bot.info_update")]),
        parse_mode=ParseMode.HTML,
    )


@r.message(Command("/cpu"))
async def cpu(message: Message):

    stats_ = await get_current_stats(
        config.server_address,
        config.monitoring_bot.access_token,
    )

    cpu_usage:int = stats_["cpu_load"]

    await message.answer(
        text="\n\n".join([
            _("message.monitoring_bot.cpu", color=color_for_cpu_usage(cpu_usage), cpu_usage=cpu_usage),
            _("message.monitoring_bot.info_update")]),
        parse_mode=ParseMode.HTML,
    )


@r.message(Command("/conf"))
async def conferences(message: Message):

    stats_ = await get_current_stats(
        config.server_address,
        config.monitoring_bot.access_token,
    )

    conferences_count = stats_["conferences"]

    await message.answer(
        text="\n\n".join([
            _("message.monitoring_bot.conf", conferences_count=conferences_count),
            _("message.monitoring_bot.info_update")]),
        parse_mode=ParseMode.HTML,
    )


@r.message(Command("/stats"))
async def stats(message: Message):

    stats_ = await get_current_stats(
        config.server_address,
        config.monitoring_bot.access_token,
    )

    conferences_count = stats_["conferences"]
    cpu_usage = stats_["cpu_load"]
    online_users_count = stats_["users"]
    participants_count = stats_["participants"]

    await message.answer(
        text=_("message.monitoring_bot.stats",
                  conferences_count=conferences_count,
                  participants_count=participants_count,
                  online_users_count=online_users_count,
                  color=color_for_cpu_usage(cpu_usage),
                  cpu_usage=cpu_usage),
        parse_mode=ParseMode.HTML,
    )


@r.message(Command("/help"))
async def handle_help(message: Message):
    await message.answer(
        text=_("message.monitoring_bot.help"),
        parse_mode=ParseMode.HTML,
    )


@r.message(Command("/about"))
async def handle_about(message: Message):
    await message.answer(_("message.monitoring_bot.about"))
