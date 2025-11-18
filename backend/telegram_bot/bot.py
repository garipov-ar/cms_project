import logging
import os
import requests
import io
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.types import InputFile

API = os.getenv("API_BASE", "http://web:8000/api")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")  # базовый адрес для медиа


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

# /start
@dp.message(Command("start"))
async def start(message: types.Message):
    r = requests.get(f"{API}/catalog/")
    r.raise_for_status()
    cats = r.json()

    buttons = [
        [InlineKeyboardButton(text=f"📁 {c['name']}", callback_data=f"cat:{c['id']}")]
        for c in cats
    ]
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await message.answer("Выберите категорию:", reply_markup=kb)

# Категории
@dp.callback_query(lambda c: c.data.startswith("cat:"))
async def open_cat(callback: types.CallbackQuery):
    cat_id = callback.data.split(":")[1]
    r = requests.get(f"{API}/catalog/{cat_id}/")
    r.raise_for_status()
    cat = r.json()

    buttons = []

    for ch in cat.get("children", []):
        buttons.append([InlineKeyboardButton(text=f"📁 {ch['name']}", callback_data=f"cat:{ch['id']}")])

    for d in cat.get("documents", []):
        buttons.append([InlineKeyboardButton(text=f"📄 {d['title']}", callback_data=f"doc:{d['id']}")])

    if not buttons:
        await callback.answer("Нет подкатегорий или документов")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.edit_text(text=f"Раздел: {cat['name']}", reply_markup=kb)
    await callback.answer()

# Документы
@dp.callback_query(lambda c: c.data.startswith("doc:"))
async def open_doc(callback: types.CallbackQuery):
    doc_id = callback.data.split(":")[1]

    try:
        r = requests.get(f"{API}/documents/{doc_id}/")
        r.raise_for_status()
        doc = r.json()
    except requests.RequestException as e:
        await callback.answer(f"Ошибка при получении документа", show_alert=True)
        return

    if "file" not in doc or not doc["file"]:
        await callback.answer("Файл не найден", show_alert=True)
        return

    # URL файла
    file_path = doc["file"]
    if file_path.startswith("/"):
        file_url = f"{BASE_URL}{file_path}"
    else:
        file_url = f"{BASE_URL}/{file_path}"

    try:
        file_resp = requests.get(file_url)
        file_resp.raise_for_status()
    except requests.RequestException:
        # Если не удалось скачать файл, просто даём ссылку
        await callback.message.answer(f"Не удалось скачать файл. Ссылка для скачивания: {file_url}")
        await callback.answer()
        return

    # Ограничение Telegram на файлы
    MAX_FILE_SIZE = 50 * 1024 * 1024
    if len(file_resp.content) > MAX_FILE_SIZE:
        await callback.message.answer(f"Файл слишком большой для Telegram. Ссылка: {file_url}")
        await callback.answer()
        return

    # Отправляем файл
    filename = os.path.basename(file_path)
    input_file = InputFile.from_buffer(file_resp.content, filename=filename)
    await callback.message.answer_document(document=input_file)
    await callback.answer()




async def main():
    logging.info("Start polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
