from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import requests
import logging

BOT_TOKEN = '8013489594:AAG9qcJUYmiDzE5fCdBpg4sQO1vkvYSBxL81234'
GOOGLE_SCRIPT_URL = 'https://script.google.com/macros/s/AKfycbx6eullBzqcrTxFmiZ5CNw65mpj-PPvFwmZE3fWApYtMakXYtFs9sOk5l5ITaPl4MyY/exec'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)


def start(update, context):
    update.message.reply_text(
        "Hi! Send me the patient's name to get the report date.")


def get_report(update, context):
    patient_name = update.message.text.strip()
    try:
        response = requests.get(GOOGLE_SCRIPT_URL, params={'name': patient_name}, timeout=10)
        response.raise_for_status()  # This will raise an error if the status is 4xx or 5xx
        update.message.reply_text(response.text)
    except Exception as e:
        update.message.reply_text("Something went wrong while fetching the report.")
        logging.error(f"Error fetching report: {e}")


def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, get_report))

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
