import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from googletrans import Translator
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7935112375:AAGkNvdmQ9zivPu8vs760pq3Ee4j1bCN28Y'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Uzbek alphabet
uz_letters = "abcdefghijklmnopqrstuvwxyz"

# List of supported languages
languages = {
    'ru': 'Russian',
    'en': 'English',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'it': 'Italian',
    'tr': 'Turkish',
    'zh-cn': 'Chinese',
    'ar': 'Arabic',
    'ko': 'Korean'
}

# Dictionary to keep track of user text and state
user_data = {}


@dp.message(Command(commands=['start', 'help']))
async def send_welcome(message: types.Message):
    await message.answer("Hi!\nThis bot translates text from Uzbek to other languages.\nJust type something in Uzbek.")


@dp.message()
async def handle_uz_text(message: types.Message):
    text = message.text

    if message.from_user.id in user_data and user_data[message.from_user.id]['state'] == 'awaiting_language':
        # Process language selection and perform translation
        await process_translation(message)
    elif text[0].lower() in uz_letters:
        # Store user's original text and prompt for language selection
        user_data[message.from_user.id] = {'original_text': text, 'state': 'awaiting_language'}

        # Prompt user to select a target language
        keyboard_buttons = [[KeyboardButton(text=lang_name)] for lang_name in languages.values()]
        keyboard = ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)
        await message.answer("Choose the language you want to translate to:", reply_markup=keyboard)
    else:
        await message.answer('I only understand Uzbek text.')


async def process_translation(message: types.Message):
    user_id = message.from_user.id
    selected_language = None

    # Find the selected language
    for code, name in languages.items():
        if message.text == name:
            selected_language = code
            break

    if selected_language and user_id in user_data:
        original_text = user_data[user_id]['original_text']
        translator = Translator()
        translation = translator.translate(original_text, dest=selected_language).text

        # Send the translation
        await message.answer(translation, reply_markup=types.ReplyKeyboardRemove())

        # Clear user's data after translation
        del user_data[user_id]
    else:
        await message.answer('Invalid language selection. Please choose a valid language.')


async def on_startup():
    logging.info("Bot is online!")


if __name__ == '__main__':
    dp.startup.register(on_startup)
    
    # Start polling
    asyncio.run(dp.start_polling(bot))
