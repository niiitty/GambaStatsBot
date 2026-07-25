import logging

from telegram import Update
from telegram.ext import (
    filters,
    ApplicationBuilder,
    ContextTypes,
    MessageHandler,
    CommandHandler,
)

from src.config import Config
from src.db import init_postgres, close_postgres
from src.slotmachine import handle_result
from src.commands import help, begin, stats


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


async def check_spin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = user.id
    chat_id = chat.id

    await handle_result(message.dice.value, user_id, chat_id)


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

    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("begin", begin))
    application.add_handler(CommandHandler("stats", stats))

    application.run_polling()


if __name__ == "__main__":
    main()
