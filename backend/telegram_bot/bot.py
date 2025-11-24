import os
import logging
import asyncio
import httpx
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError

# --- Настройки ---
API = os.getenv("API_BASE", "http://web:8000/api")
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

if not TOKEN:
    raise RuntimeError("TELEGRAM_BOT_TOKEN не задан!")

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB

# --- Вспомогательные функции ---

def build_keyboard(items, parent_id=None):
    buttons = []

    for item in items:
        if item["type"] == "cat":
            buttons.append([InlineKeyboardButton(
                text=f"📁 {item['name']}",
                callback_data=f"cat:{item['id']}"
            )])
        elif item["type"] == "doc":
            buttons.append([InlineKeyboardButton(
                text=f"📄 {item['title']}",
                callback_data=f"doc:{item['id']}:{parent_id if parent_id is not None else 'None'}"
            )])

    nav_buttons = []
    if parent_id is not None:
        nav_buttons.append(InlineKeyboardButton(
            text="⬅️ Назад",
            callback_data=f"cat:{parent_id}"
        ))
    nav_buttons.append(InlineKeyboardButton(
        text="🏠 Главная",
        callback_data="home"
    ))

    if nav_buttons:
        buttons.append(nav_buttons)

    return InlineKeyboardMarkup(inline_keyboard=buttons)

async def fetch_json(client, url):
    resp = await client.get(url)
    resp.raise_for_status()
    return resp.json()

async def fetch_file(client, url):
    resp = await client.get(url)
    resp.raise_for_status()
    return resp.content

# --- Хэндлеры ---

@dp.message(Command("start"))
async def start(message: types.Message):
    async with httpx.AsyncClient() as client:
        cats = await fetch_json(client, f"{API}/catalog/")

    items = [{"type": "cat", "id": c["id"], "name": c["name"]} for c in cats]
    kb = build_keyboard(items)
    await message.answer("Выберите категорию:", reply_markup=kb)

@dp.callback_query(lambda c: c.data.startswith("cat:"))
async def open_cat(callback: types.CallbackQuery):
    cat_id = callback.data.split(":")[1]

    async with httpx.AsyncClient() as client:
        cat = await fetch_json(client, f"{API}/catalog/{cat_id}/")

    items = []
    for ch in cat.get("children", []):
        items.append({"type": "cat", "id": ch["id"], "name": ch["name"]})
    for d in cat.get("documents", []):
        items.append({"type": "doc", "id": d["id"], "title": d["title"]})

    kb = build_keyboard(items, parent_id=cat.get("parent"))

    try:
        await callback.message.edit_text(f"Раздел: {cat['name']}", reply_markup=kb)
    except TelegramAPIError as e:
        if "message is not modified" not in str(e):
            raise
    await callback.answer()

@dp.callback_query(lambda c: c.data == "home")
async def go_home(callback: types.CallbackQuery):
    async with httpx.AsyncClient() as client:
        cats = await fetch_json(client, f"{API}/catalog/")

    items = [{"type": "cat", "id": c["id"], "name": c["name"]} for c in cats]
    kb = build_keyboard(items)

    try:
        await callback.message.edit_text("Выберите категорию:", reply_markup=kb)
    except TelegramAPIError as e:
        if "message is not modified" not in str(e):
            raise
    await callback.answer()

@dp.callback_query(lambda c: c.data.startswith("doc:"))
async def open_doc(callback: types.CallbackQuery):
    # Получаем id документа и parent_id категории
    doc_id, _ = callback.data.split(":")[1:3]

    async with httpx.AsyncClient() as client:
        # Получаем метаданные документа
        doc = await fetch_json(client, f"{API}/documents/{doc_id}/")
        file_path = doc.get("file")
        if not file_path:
            await callback.answer("Файл не найден", show_alert=True)
            return
        
        # Используем категорию документа для кнопки "Назад"
        parent_id = doc.get("category")

        # Формируем корректный URL для скачивания
        file_url = f"{BASE_URL}/{file_path.lstrip('/')}" if not file_path.startswith(("http://", "https://")) else file_path
        file_content = await fetch_file(client, file_url)

    # Проверка размера
    if len(file_content) > MAX_FILE_SIZE:
        await callback.message.answer(f"Файл слишком большой. Ссылка: {file_url}")
        await callback.answer()
        return

    # Отправляем файл отдельным сообщением
    input_file = BufferedInputFile(file_content, os.path.basename(file_path))
    await callback.message.answer_document(input_file)

    # Обновляем кнопки навигации в том же сообщении
    kb = build_keyboard([], parent_id=parent_id)
    try:
        await callback.message.edit_reply_markup(reply_markup=kb)
    except TelegramAPIError as e:
        # Игнорируем ошибку "message is not modified"
        if "message is not modified" not in str(e):
            raise

    await callback.answer()


# --- Запуск ---

async def main():
    logging.info("Start polling")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
