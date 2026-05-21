"""Telegram-бот «Генератор случайных отмазок».

Бот присылает случайную смешную отмазку по нажатию кнопки.
С шансом ~5% выпадает особая «легендарная отмазка».
"""

import asyncio
import logging
import os
import random

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# ===== Список отмазок =====
EXCUSES = [
    "Я в лесу",
    "Мне гулять с собакой",
    "Завтра рано вставать, поэтому сегодня нельзя веселиться",
    "Рубрика рандомный слив",
    "Послезавтра надо работать, вдруг опоздаю",
    "Нечего надеть",
    "Рубрика молчаливый слив",
    "Кот в мешке - сгенерируй сам",
    "Нужно немного насилия",
    "Татарские посиделки",
]

# Легендарная отмазка — выпадает примерно в 5% случаев
LEGENDARY_EXCUSE = (
    "Я не пришёл, потому что в этот момент спасал котёнка, "
    "доставлял пиццу бабушке и одновременно изобретал "
    "лекарство от понедельников."
)

LEGENDARY_CHANCE = 0.05


def generate_excuse() -> tuple[str, bool]:
    """Возвращает (текст отмазки, признак легендарной)."""
    if random.random() < LEGENDARY_CHANCE:
        return LEGENDARY_EXCUSE, True
    return random.choice(EXCUSES), False


def excuse_keyboard(excuse_text: str) -> InlineKeyboardMarkup:
    """Клавиатура под отмазкой: копирование и повторная генерация."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            # copy_text позволяет скопировать отмазку одним нажатием
            [
                InlineKeyboardButton(
                    text="📋 Скопировать отмазку",
                    copy_text={"text": excuse_text},
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎲 Сгенерировать ещё",
                    callback_data="generate",
                )
            ],
        ]
    )


def start_keyboard() -> InlineKeyboardMarkup:
    """Стартовая клавиатура с одной кнопкой генерации."""
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎲 Сгенерировать отмазку",
                    callback_data="generate",
                )
            ]
        ]
    )


async def send_excuse(message: Message) -> None:
    """Генерирует отмазку и отправляет её сообщением."""
    text, is_legendary = generate_excuse()
    if is_legendary:
        # Легендарная отмазка оформляется особым образом
        body = f"✨🏆 <b>ЛЕГЕНДАРНАЯ ОТМАЗКА</b> 🏆✨\n\n<i>{text}</i>"
    else:
        body = text
    await message.answer(body, reply_markup=excuse_keyboard(text))


dp = Dispatcher()


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    """Приветствие при команде /start."""
    await message.answer(
        "Привет! Я генератор случайных отмазок 😏\n\n"
        "Нажми кнопку — и получи готовую отмазку на любой случай.",
        reply_markup=start_keyboard(),
    )


@dp.callback_query(F.data == "generate")
async def on_generate(callback: CallbackQuery) -> None:
    """Обработка нажатия кнопки генерации."""
    await send_excuse(callback.message)
    await callback.answer()


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    # Токен бота берётся из переменной окружения BOT_TOKEN
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "Не задан токен бота. Установите переменную окружения BOT_TOKEN."
        )

    bot = Bot(
        token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
