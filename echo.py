import logging
import os

from trueconf.types.message import Message

# одна строка — создаём папку для логов (если её нет)
os.makedirs("logs", exist_ok=True)


# всё пишем только в файл logs/bot.log
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="logs/bot.log",
    encoding="utf-8",
)


import asyncio
from trueconf.client.bot import Bot
from trueconf.dispatcher import Dispatcher
from trueconf.router import Router
from trueconf.filters import Command, AnyText
from trueconf.enums import ParseMode, SurveyType
from trueconf.types.requests import (
    CreatedChannel,
    CreatedGroupChat,
    CreatedPrivateChat,
    UploadingProgress,
    RemovedChat,
    RemovedMessage,
    RemovedChatParticipant,
    AddedChatParticipant,
    EditedMessage


)
from trueconf.enums import EnvelopeType
from trueconf.exceptions import ApiError

async def main():
    dp = Dispatcher()
    r = Router()

    @r.message(Command("start"))
    async def on_start(evt: dict):
        chat_id = (evt.get("payload") or {}).get("chatId")
        await bot.send_message(chat_id=chat_id, text="Hi! I'm alive", parse_mode=ParseMode.HTML)
        await bot.reply_message()

    @r.message()
    async def echo(message: Message):
        print("#message", message)


    @r.uploading_progress()
    async def upload_progress(update: UploadingProgress):
        print("#upload", update)

    @r.removed_message()
    async def removed_message(evt: RemovedMessage):
        print("#removed", evt)

    @r.edited_message()
    async def edited_message(evt: EditedMessage):
        print("#edited", evt)

    @r.added_chat_participant()
    async def added_chat_participant(evt: AddedChatParticipant):
        print("#added_chat_participant", evt)

    @r.removed_chat_participant()
    async def removed_chat_participant(evt: RemovedChatParticipant):
        print("#removed_chat_participant", evt)

    @r.removed_chat()
    async def removed_chat(evt:RemovedChat):
        print("#removed_chat", evt)

    @r.created_channel()
    @r.created_group_chat()
    @r.created_private_chat()
    async def created_any_type_chat(evt: CreatedChannel | CreatedGroupChat | CreatedPrivateChat):
        print("#created_any_chat", evt)



    dp.include_router(r)

    bot = await Bot.from_credentials(
        server="10.140.0.33",
        username="echo_bot",
        password="123tr",
        dispatcher=dp,
        verify_ssl=False,
        receive_unread_messages=True
    )

    await bot.start()
    await bot.connected_event.wait()
    await bot.authorized_event.wait()

    # await bot.run()

    try:

        res = await bot.edit_survey(
            message_id="c59154f3-ecd8-439b-a8ba-5d6a95fa2da0",
            title="🎨Test (edited) servey",
            survey_campaign_id = "1",
            survey_type=SurveyType.ANONYMOUS
        )

        print(res)

        res = await bot.send_document(chat_id="c7e8895729a3efdb23c1dcec70f2238b550ec88e", file_path="/Users/baadzianton/Downloads/Stray_v1.6.dmg")


        res = await bot.subscribe_file_progress(file_id="22c029e719850de7821707e68529248767f2f7a3")

        print(res)
        pass




        # print(await bot.get_user_display_name("bots_ru"))
        # pass
        # # res = await bot.get_chats(100,1)
        # # for chat in res.chats:
        # #     if chat.title == "bots_ru@video.example.net":
        # #         chat_id = chat.chat_id
        # #         break
        # r = await bot.create_private_chat("gaidenko")
        # chat_id = r.chat_id
        # for i in range(10):
        #     r = await bot.send_message(chat_id=chat_id, text="Hello!")
        #     await bot.remove_message(r.message_id, for_all=True)
        #     await asyncio.sleep()
        # # print(res)
        # res = await bot.forward_message(chat_id=chat_id,message_id=res.message_id)
        # print(res)
        # await bot.send_sticker(chat_id=chat_id,file_path="/Users/baadzianton/Downloads/geo_stiker/hello.webp")
        # await bot.send_sticker(chat_id=chat_id, file_path="/Users/baadzianton/Downloads/geo_stiker/blagodat.webp")
        # await bot.send_sticker(chat_id=chat_id, file_path="/Users/baadzianton/Downloads/geo_stiker/progress.webp")
        # await bot.send_sticker(chat_id=chat_id, file_path="/Users/baadzianton/Downloads/geo_stiker/mda.webp")
        # res = await bot.get_chat_history(chat_id="c7e8895729a3efdb23c1dcec70f2238b550ec88e", count=0)
        # res = await bot.forward_message(chat_id= res.chat_id, message_id= res.message_id)
        # res = await bot.get_message_by_id(message_id=res.message_id)

    except ApiError as e:
        print(e)

    await bot.stopped_event.wait()
    # await bot.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
