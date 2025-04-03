from aiogram import executor

async def on_startup(dp):
    import time

    from loguru import logger
    from source import handlers

    logger.add(
        f'logs/{time.strftime("%Y-%m-%d__%H-%M")}.log',
        level="DEBUG",
        rotation="500 MB",
        compression="zip",
    )

    handlers.setup(dp)

    logger.success("[+] Bot started successfully")



if __name__ == "__main__":
    # Launch
    from aiogram import executor

    from source.handlers import dp

    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
