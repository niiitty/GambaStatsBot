import logging

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)

from src.commands import begin, help, leaderboard, stats
from src.config import Config
from src.db import close_postgres, init_postgres
from src.slotmachine import check_spin

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
    application.add_handler(CommandHandler("leaderboard", leaderboard))

    application.run_polling()


if __name__ == "__main__":
    main()
