import json
import os
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Нет BOT_TOKEN. Создай .env и добавь BOT_TOKEN=...")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DAYS = [("пн", "Пн"), ("вт", "Вт"), ("ср", "Ср"), ("чт", "Чт"), ("пт", "Пт")]
WEEKS = [("числитель", "Числитель"), ("знаменатель", "Знаменатель")]

# В памяти держим выбор пользователя: { user_id: {"week": "...", "day": "..."} }
user_state = {}


def load_schedule():
    with open("schedule.json", "r", encoding="utf-8") as f:
        return json.load(f)


def week_keyboard():
    kb = InlineKeyboardBuilder()
    for key, title in WEEKS:
        kb.button(text=title, callback_data=f"week:{key}")
    kb.adjust(2)
    return kb.as_markup()


def day_keyboard(selected_week=None):
    kb = InlineKeyboardBuilder()
    for key, title in DAYS:
        kb.button(text=title, callback_data=f"day:{key}")
    kb.adjust(5)

    # Кнопка "поменять неделю"
    kb.row()
    if selected_week:
        kb.button(text=f"Неделя: {selected_week}", callback_data="change_week")
    else:
        kb.button(text="Выбрать неделю", callback_data="change_week")

    return kb.as_markup()


def format_day(schedule, week, day):
    items = schedule.get(week, {}).get(day, [])
    day_name = dict(DAYS).get(day, day)

    header = f"📅 *{day_name.upper()}* — *{week}*\n"
    if not items:
        return header + "\nНет пар ✅"

    lines = [header]
    for i, it in enumerate(items, 1):
        time = (it.get("time") or "").strip()
        subject = (it.get("subject") or "").strip()
        kind = (it.get("kind") or "").strip()
        teacher = (it.get("teacher") or "").strip()
        room = (it.get("room") or "").strip()

        title = subject
        if kind:
            title = f"{subject} ({kind})"

        block = [f"{i}) ⏰ *{time}*", f"   📚 {title}"]

        if teacher:
            block.append(f"   👤 {teacher}")
        if room:
            block.append(f"   🏫 {room}")

        lines.append("\n".join(block))

    return "\n\n".join(lines).strip()


@dp.message(F.text.in_({"/start", "start"}))
async def start(message: Message):
    user_state[message.from_user.id] = {"week": None, "day": None}
    await message.answer(
        "Привет! Выбери неделю 👇",
        reply_markup=week_keyboard()
    )


@dp.callback_query(F.data == "change_week")
async def change_week(cb: CallbackQuery):
    await cb.message.edit_text("Выбери неделю 👇", reply_markup=week_keyboard())
    await cb.answer()


@dp.callback_query(F.data.startswith("week:"))
async def set_week(cb: CallbackQuery):
    week = cb.data.split(":", 1)[1]
    st = user_state.setdefault(cb.from_user.id, {"week": None, "day": None})
    st["week"] = week

    await cb.message.edit_text(
        f"Ок! Неделя: *{week}*\nТеперь выбери день 👇",
        reply_markup=day_keyboard(selected_week=week),
        parse_mode="Markdown"
    )
    await cb.answer()


@dp.callback_query(F.data.startswith("day:"))
async def set_day(cb: CallbackQuery):
    day = cb.data.split(":", 1)[1]
    st = user_state.setdefault(cb.from_user.id, {"week": None, "day": None})
    week = st.get("week")

    if not week:
        await cb.answer("Сначала выбери неделю 🙂", show_alert=True)
        return

    schedule = load_schedule()
    text = format_day(schedule, week, day)

    st["day"] = day
    await cb.message.edit_text(
        text,
        reply_markup=day_keyboard(selected_week=week),
        parse_mode="Markdown"
    )
    await cb.answer()


@dp.message()
async def fallback(message: Message):
    await message.answer("Напиши /start чтобы открыть меню расписания 🙂")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())