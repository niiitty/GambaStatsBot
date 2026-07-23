import logging

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, MessageHandler

from config import Config
from db import init_postgres, close_postgres
from slotmachine import handle_result


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def check_spin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    roll_value = update.effective_message.dice.value
    handle_result(roll_value)


def main() -> None:
    config = Config.get_env()

    application = (
        ApplicationBuilder()
        .token(config.bot_token)
        .post_init(init_postgres)
        .post_shutdown(close_postgres)
        .build()
    )

    slot_machine_handler = MessageHandler(filters.Dice.SLOT_MACHINE, check_spin)

    application.add_handler(slot_machine_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
