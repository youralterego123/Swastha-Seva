import constants as keys
from telegram.ext import *
import response as R
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
import logging
from test import rendering_prescription, image2base64, html2pdf

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

NAME, AGE, SYMP = range(3)
print("Bot started")
global name1, age1


def start_command(update, context):
    update.message.reply_text("Hi! My name is SwasthSeva Bot. I will hold a conversation with you. "
                              "Watch yo name?")

    return NAME


def name(update, context):
    """Stores the name and asks for a age."""
    global name1
    name1 = update.message.text
    print("1", name1)
    update.message.reply_text(
        "Enter Your age"
    )

    return AGE


def age(update, context):
    """Stores the age and asks for Symptoms."""
    global age1
    age1 = update.message.text
    print("2", age1)

    update.message.reply_text(
        "Enter 6 symptoms"
    )
    return SYMP


def symp(update, context):
    global name1, age1
    symptoms = update.message.text
    print("3", symptoms)
    text = str(symptoms).lower()
    response = R.sample(text)
    print(response)
    rendering_prescription(name1, age1, symptoms, response)
    html2pdf()
    update.message.reply_text(response)
    update.message.reply_document(document=open('output/prescription.pdf', 'rb'))
    return ConversationHandler.END


def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start_command)],
        states={
            NAME: [MessageHandler(Filters.text, name)],
            AGE: [MessageHandler(Filters.text, age)],
            SYMP: [
                MessageHandler(Filters.text, symp)]
        },
        fallbacks=[CommandHandler("start", start_command)],
    )

    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


main()
