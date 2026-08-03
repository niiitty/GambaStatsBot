import logging

from telegram.ext import (
    filters,
    ApplicationBuilder,
    MessageHandler,
    CommandHandler,
)

from src.config import Config
from src.db import init_postgres, close_postgres
from src.slotmachine import check_spin
from src.commands import help, begin, stats


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def main() -> None:
    config = Config.get_env()

    application = (
        ApplicationBuilder()
        .token(config.bot_token)
        .post_init(init_postgres)
        .post_shutdown(close_postgres)
        .build()
    )

    slot_machine_handler = MessageHandler(
        filters.Dice.SLOT_MACHINE & (~filters.FORWARDED), check_spin
    )
    application.add_handler(slot_machine_handler)

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("begin", begin))
    application.add_handler(CommandHandler("stats", stats))

    application.run_polling()


if __name__ == "__main__":
    main()
