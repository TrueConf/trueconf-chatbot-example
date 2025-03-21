import asyncio
import logging
from logging.handlers import RotatingFileHandler
from logging import Formatter
import os

from app import echo_bot, monitoring_bot, hospital_bot, gpt_bot

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    filename="logs/bot.log",
    encoding="utf-8",
)

async def run_bots():

    await echo_bot.start()
    await monitoring_bot.start()
    await hospital_bot.start()
    await gpt_bot.start()

    await asyncio.gather(
        await echo_bot.run(),
        await monitoring_bot.run(),
        await hospital_bot.run(),
        await gpt_bot.run(),
    )

def main():
    try:
        asyncio.run(run_bots())
    except KeyboardInterrupt:
        print("\nЗавершение работы всех ботов...")
    except Exception as e:
        print(f"\nОшибка: {e}")


if __name__ == "__main__":
    main()
