import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from deep_translator import GoogleTranslator
import uuid
import logging
from aiogram.types import FSInputFile
from config import TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


IMG_FOLDER = 'img'


os.makedirs(IMG_FOLDER, exist_ok=True)

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот, который может:\n"
        "- Сохранять фото\n"
        "- Отправлять голосовые сообщения\n"
        "- Переводить текст на английский"
    )





@dp.message()
async def handle_message(message: types.Message):
    try:
        # Обработка фотографий
        if message.photo:
            await handle_photo(message)

        # Перевод текста
        if message.text:
            await handle_translation(message)

            
            if message.text.lower() in ['/voice', 'голос', 'voice']:
                await send_voice_message(message)

    except Exception as e:
        logger.error(f"Ошибка при обработке сообщения: {e}")
        await message.reply("Произошла ошибка при обработке сообщения.")


async def handle_photo(message: types.Message):
    """Сохранение входящих фотографий"""
    try:
        # Получаем самый большой файл фото
        photo = message.photo[-1]
        file = await bot.get_file(photo.file_id)

        # Генерируем уникальное имя файла
        filename = os.path.join(IMG_FOLDER, f"{uuid.uuid4()}.jpg")

        # Скачиваем и сохраняем фото
        await bot.download_file(file.file_path, filename)
        logger.info(f"Фото сохранено: {filename}")
        await message.reply(f"Фото сохранено как {os.path.basename(filename)}")

    except Exception as e:
        logger.error(f"Ошибка при сохранении фото: {e}")
        await message.reply("Не удалось сохранить фото.")


async def handle_translation(message: types.Message):
    """Перевод текста на английский"""
    try:
        if message.text.startswith('/'):
            return

        # Переводим текст на английский
        translated = GoogleTranslator(source='auto', target='en').translate(message.text)
        await message.reply(f"Перевод на английский: {translated}")

    except Exception as e:
        logger.error(f"Ошибка при переводе текста: {e}")
        await message.reply("Не удалось перевести текст.")





async def send_voice_message(message, audio_path='voice/voice.mp3'):
    audio = FSInputFile(audio_path)
    await message.bot.send_voice(message.chat.id, audio)







async def main():
    logger.info("Запуск бота...")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")


if __name__ == '__main__':
    asyncio.run(main())
