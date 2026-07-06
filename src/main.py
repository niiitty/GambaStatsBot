import logging
from telegram import Update
from telegram.ext import filters, ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler

from constants import BOT_TOKEN

from slotmachine import handle_result

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def check_roll(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    roll_value = update.effective_message.dice.value
    handle_result(roll_value)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    slot_machine_handler = MessageHandler(filters.Dice.SLOT_MACHINE, check_roll)
    
    application.add_handler(slot_machine_handler)
    
    application.run_polling()
