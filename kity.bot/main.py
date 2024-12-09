import os
import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import (
    CommandHandler, Updater, CallbackContext, MessageHandler, Filters
    )
from telegram.update import Update

from dotenv import load_dotenv

# Load environment variables
load_dotenv()
secret_token = os.getenv('TOKEN')

# Initialize the bot
updater = Updater(token=secret_token)

# URLs for random images and facts
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'
URL_CAT_FACT = 'https://meowfacts.herokuapp.com/'
URL_DOG_FACT = 'https://dog-api.kinduff.com/api/facts'


# Function to fetch a random cat image
def get_random_cat():
    response = requests.get(URL_CAT).json()
    return response[0].get('url')


# Function to fetch a random dog image
def get_random_dog():
    response = requests.get(URL_DOG).json()
    return response[0].get('url')


# Function to fetch a random cat fact
def get_cat_fact():
    response = requests.get(URL_CAT_FACT).json()
    return response.get('data')[0]


# Function to fetch a random dog fact
def get_dog_fact():
    response = requests.get(URL_DOG_FACT).json()
    return response.get('facts')[0]


# Handler to send a random cat image
def random_cat(update: Update, context: CallbackContext):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_random_cat())


# Handler to send a random dog image
def random_dog(update: Update, context: CallbackContext):
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_random_dog())


# Handler to send a random cat fact
def cat_fact(update: Update, context: CallbackContext):
    chat = update.effective_chat
    context.bot.send_message(chat.id, get_cat_fact())


# Handler to send a random dog fact
def dog_fact(update: Update, context: CallbackContext):
    chat = update.effective_chat
    context.bot.send_message(chat.id, get_dog_fact())


# Show the main menu
def main_menu(update: Update, context: CallbackContext):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Random Cat', 'Random Dog'], ['More Options']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text="Welcome back to the main menu! Choose an option:",
        reply_markup=button
    )


# Show the submenu
def submenu(update: Update, context: CallbackContext):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Cat Fact', 'Dog Fact'], ['Back to Main Menu']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text="Here are some interesting options:",
        reply_markup=button
    )


# Start handler
def start(update: Update, context: CallbackContext):
    chat = update.effective_chat
    button = ReplyKeyboardMarkup(
        [['Random Cat', 'Random Dog'], ['More Options']],
        resize_keyboard=True
    )
    context.bot.send_message(
        chat_id=chat.id,
        text=f"Hello, {update.message.chat.first_name}! Choose an option:",
        reply_markup=button
    )


# Register command handlers
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('main_menu', main_menu))
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    'Random Cat'), random_cat)
    )
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    'Random Dog'), random_dog)
    )
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    'More Options'), submenu)
    )
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    'Cat Fact'), cat_fact)
    )
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    'Dog Fact'), dog_fact)
    )
updater.dispatcher.add_handler(MessageHandler(Filters.text(
    'Back to Main Menu'), main_menu)
    )

# Start the bot
updater.start_polling()
updater.idle()
