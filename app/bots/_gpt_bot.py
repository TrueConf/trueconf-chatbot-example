import random
import threading
import asyncio

from trueconf import Bot, Dispatcher, Router, F, Message
from trueconf.enums import MessageType, ParseMode

from app.config import config
from app.config import llm
from app.localization import _

import logging

logger = logging.getLogger("chat_bot")

message_queue: asyncio.Queue = asyncio.Queue()
worker_task: asyncio.Task | None = None


r = Router(name="gpt_bot")
dp = Dispatcher()

dp.include_router(r)

gpt_bot = Bot.from_credentials(
    username=config.gpt_bot.username,
    password=config.gpt_bot.password,
    server=config.server_address,
    dispatcher=dp,
    verify_ssl=False,
)

async def process_queue() -> None:
    while True:
        msg = await message_queue.get()
        try:
            # если get_answer синхронная и тяжёлая — оберни:
            # await asyncio.to_thread(get_answer, msg)
            await get_answer(msg)
        except Exception:
            logger.exception("Queue worker failed while processing message")
        finally:
            message_queue.task_done()


async def get_answer(message: Message):

    if any(
        x in message.content.text
        for x in [
            "TrueConf",
            "Труконф",
            "труконф",
            "trueconf",
            "трюконф",
            "ТРУКОНФ",
            "TRUECONF",
        ]
    ):
        messages = [
            {
                "role": "system",
                "content": f"Труконф - это TrueConf. {_("message.llm.tune")}",
            },
            {"role": "user", "content": message.content.text},
        ]
    else:
        messages = [
            {
                "role": "system",
                "content": _("message.llm.tune"),
            },
            {"role": "user", "content": message.content.text},
        ]

    response = llm.create_chat_completion(
        messages=messages,
        max_tokens=config.gpt_bot.llama.max_tokens,
    )

    logger.info(_("logger.info.response_from_llm", response=response))
    if response and "choices" in response and len(response["choices"]) > 0:
        content = response["choices"][0]["message"]["content"]

        logger.info(_("logger.info.outgoing_message"))
        await message.answer(text=content, parse_mode=ParseMode.HTML)

    else:
        logger.error(_("logger.error.invalid_response_from_llm"))
        await message.answer(_("message.llm.invalid_response_from_llm"))


@r.message(F.text)
async def handle_gpt(message: Message):

    thinking_list = _("message.llm.thinking_list")
    logger.info(_("logger.incoming_message", message= message.content.text))
    await message.answer(random.choice(thinking_list))

    await message_queue.put(message)

    global worker_task
    if worker_task is None or worker_task.done():
        worker_task = asyncio.create_task(process_queue())


@r.message(F.type == MessageType.ATTACHMENT)
async def attachment_handler(message: Message):
    await message.answer(text=_("message.no_files"),parse_mode=ParseMode.HTML)


