from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from app.data.db import get_films


# Клавіатура основного меню
def main_menu_keyboard():
    builder = ReplyKeyboardBuilder()

    builder.button(text="Перелік фільмів")
    builder.button(text="Додати новий фільм")

    markup = builder.as_markup()
    markup.resize_keyboard = True

    return markup


# Inline клавіатура для списку фільмів
def build_films_keyboard(films: list):
    builder = InlineKeyboardBuilder()
    for index, film in enumerate(films):
        builder.button(text=film.get("title"), callback_data=f"film_{index}")
    return builder.as_markup()


# Inline клавіатура для детального опису фільма
def build_film_details_keyboard(film_id, film):
    builder = InlineKeyboardBuilder()
    if film_id > 0:
        builder.button(text="Попередній", callback_data=f"film_{film_id-1}")
    builder.button(text="Перейти за посиланням", url=film.get("url"))
    builder.button(text="Go back", callback_data="back")
    if film_id < len(get_films()) - 1:
        builder.button(text="Наступний", callback_data=f"film_{film_id+1}")
    return builder.as_markup()


def cancel_states_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Cancel creating film")
    markup = builder.as_markup()
    markup.resize_keyboard = True
    return markup
