import logging
from dataclasses import dataclass

from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from config import Config
from slotmachine import handle_result


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def check_spin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    roll_value = update.effective_message.dice.value
    handle_result(roll_value)


def main() -> None:
    config = Config.get_env()

    application = ApplicationBuilder().token(config.bot_token).build()

    slot_machine_handler = MessageHandler(filters.Dice.SLOT_MACHINE, check_spin)
    
    application.add_handler(slot_machine_handler)
    
    application.run_polling()


if __name__ == "__main__":
    main()