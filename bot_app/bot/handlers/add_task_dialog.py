# bot/dialogs/add_task_dialog.py
import logging

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Radio
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.input import TextInput
from aiogram_dialog import DialogManager
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from datetime import datetime
import aiohttp

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

BACKEND_URL_CATEGORIES = "http://backend:8000/api/categories/"
BACKEND_URL_TASKS = "http://backend:8000/api/tasks/"


# Шаги диалога
class AddTaskDialogSG(StatesGroup):
    title = State()
    description = State()
    category = State()
    due_date = State()
    confirm = State()


# Вспомогательные обработчики (управляют dialog_data)
async def on_title_entered(msg: Message, widget: TextInput, dialog_manager: DialogManager, title: str):
    dialog_manager.dialog_data["title"] = title
    await dialog_manager.switch_to(AddTaskDialogSG.description)


async def on_description_entered(msg: Message, widget: TextInput, dialog_manager: DialogManager, description: str):
    dialog_manager.dialog_data["description"] = description
    await dialog_manager.switch_to(AddTaskDialogSG.category)


async def on_due_date_entered(msg: Message, widget: TextInput, dialog_manager: DialogManager, due: str):
    try:
        due_date = datetime.strptime(due, "%Y-%m-%d %H:%M")
        dialog_manager.dialog_data["due_date"] = due_date.isoformat()
        await dialog_manager.switch_to(AddTaskDialogSG.confirm)
    except ValueError:
        await msg.answer("❌ Неверный формат. Введите дату в формате: `2025-07-12 14:30`", parse_mode="Markdown")


async def on_category_selected(callback: CallbackQuery, widget: Radio, dialog_manager: DialogManager, item_id: str):
    dialog_manager.dialog_data["category_id"] = item_id
    await dialog_manager.switch_to(AddTaskDialogSG.due_date)


# Получение списка категорий с API
async def get_category_data(dialog_manager: DialogManager, **kwargs):
    categories = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(BACKEND_URL_CATEGORIES) as resp:
                if resp.status == 200:
                    json_data = await resp.json()
                    categories = [(cat["id"], cat["name"]) for cat in json_data]
    except Exception as e:
        print("Ошибка при получении категорий:", e)

    return {"categories": categories}


# Отправка задачи на сервер
async def submit_task(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    data = dialog_manager.dialog_data
    user_id = callback.from_user.id

    task_payload = {
        "title": data["title"],
        "description": data["description"],
        "user": user_id,
        "due_date": data["due_date"],
        "category_id": data["category_id"]
    }
    logger.info(f"📤 Отправка задачи в бекенд: {task_payload}")

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(BACKEND_URL_TASKS, json=task_payload) as resp:

                if resp.status in (200, 201):
                    await callback.message.answer("✅ Задача успешно добавлена!")
                else:
                    text = await resp.text()
                    logger.info(f"📥 Ответ от сервера: {resp.status} — {text}")
                    await callback.message.answer(f"❌ Ошибка при добавлении задачи: {resp.status}\n{text}")
    except Exception as e:
        await callback.message.answer(f"Ошибка: {str(e)}")

    await dialog_manager.done()


# ------------------------ DIALOG ------------------------

add_task_dialog = Dialog(
    Window(
        Const("Введите название задачи:"),
        TextInput(id="input_title", on_success=on_title_entered),
        state=AddTaskDialogSG.title,
    ),
    Window(
        Const("Введите описание задачи (можно пусто):"),
        TextInput(id="input_description", on_success=on_description_entered),
        state=AddTaskDialogSG.description,
    ),
    Window(
        Const("Выберите категорию задачи:"),
        Radio(
            checked_text=Format("✅ {item[1]}"),
            unchecked_text=Format("▫️ {item[1]}"),
            id="select_category",
            items="categories",
            item_id_getter=lambda x: x[0],
            on_click=on_category_selected,
        ),
        Cancel(Const("❌ Отмена")),
        state=AddTaskDialogSG.category,
        getter=get_category_data,
    ),
    Window(
        Const("Введите дату и время дедлайна\nФормат: `2025-07-15 14:30`"),
        TextInput(id="input_due_date", on_success=on_due_date_entered),
        Cancel(Const("❌ Отмена")),
        state=AddTaskDialogSG.due_date,
    ),
    Window(
        Format(
            "✅ Подтвердите добавление задачи:\n\n"
            "🔸 Название: {dialog_data[title]}\n"
            "📄 Описание: {dialog_data[description]}\n"
            "⏰ Дедлайн: {dialog_data[due_date]}"
        ),
        Button(Const("✅ Добавить задачу"), id="btn_submit", on_click=submit_task),
        Cancel(Const("❌ Отмена")),
        state=AddTaskDialogSG.confirm,
    ),
)