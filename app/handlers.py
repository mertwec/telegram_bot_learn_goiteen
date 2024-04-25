from typing import Union

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove

from app.fsm import FilmCreateForm
from app.keyboards import main_menu_keyboard, build_films_keyboard, build_film_details_keyboard, cancel_states_keyboard
from app.data.db import get_films, get_film_by_id, create_film
from settings import DB

router = Router()


@router.message(Command('start'))
@router.message(Command('menu'))
async def start_command(message: Message):
    if message.text == "/start":
        await message.answer(f"Привіт, {message.from_user.full_name}! Вітаємо у нашому боті!",
                             reply_markup=main_menu_keyboard())
    else:
        await message.answer(f"Доступні опції",
                             reply_markup=main_menu_keyboard())


# Обробник для команди /films та повідомлення із текстом films
@router.message(Command("films"))
@router.message(F.text == "Перелік фільмів")
async def list_films(message: Message):
    films = get_films(data_file=DB)

    if films:
        keyboard = build_films_keyboard(films)
        await message.answer("Виберіть будь-який фільм:", reply_markup=keyboard)
    else:
        await message.answer("Нажаль зараз відсутні фільми. Спробуйте /create_film для створення нового.")


# Обробник для inline-кнопки детального опису фільма
@router.callback_query(F.data.startswith("film_"))
async def show_film_details(callback: CallbackQuery) -> None:
    film_id = int(callback.data.split("_")[-1])
    film: dict = get_film_by_id(film_id=film_id)
    photo_id = film.get('photo')
    text = f"Назва: {film.get('title')}\nОпис: {film.get('desc')}\nРейтинг: {film.get('rating')}"
    keyboard = build_film_details_keyboard(film_id, film)

    await callback.message.answer_photo(photo_id, caption=text, reply_markup=keyboard)
    await callback.message.delete()


# Обробник для inline-кнопки back -- повертає до списку фільмів
@router.callback_query(F.data == "back")
async def back_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.answer()
    await list_films(callback.message)


@router.message(Command(commands=["cancel"]))
@router.message(F.text.lower() == "відміна")
@router.message(F.text == "Cancel creating film")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Дія відмінена",
        reply_markup=main_menu_keyboard()
    )






# ==== start FSM ===========================================

@router.message(Command("create_film"))
@router.message(F.text == "Додати новий фільм")
async def create_film_command(message: Message, state: FSMContext) -> None:
    # очистити кінцевий автомат на випадок, якщо він не був завершений коректно
    await state.clear()

    # починаємо кінцевий автомат з першого стану (State)
    await state.set_state(FilmCreateForm.title)
    await message.answer(text="Яка назва фільму?",
                         reply_markup=cancel_states_keyboard())
                         # reply_markup=ReplyKeyboardRemove())


# другий стан  (State) кінцевий автомат
@router.message(FilmCreateForm.title)
async def proces_title(message: Message, state: FSMContext) -> None:
    # збеігаемо попереднє значення title
    await state.update_data(title=message.text)

    # змінюємо стан на наступний
    await state.set_state(FilmCreateForm.desc)
    await message.answer("Який опис фільму?",
                         reply_markup=cancel_states_keyboard())


@router.message(FilmCreateForm.desc)
async def proces_description(message: Message, state: FSMContext) -> None:
    data = await state.update_data(desc=message.text)
    await state.set_state(FilmCreateForm.url)
    await message.answer(f"Надайте посилання на фільм: {data.get('title')}",
                         reply_markup=cancel_states_keyboard())


@router.message(FilmCreateForm.url)
async def proces_url(message: Message, state: FSMContext) -> None:
    if message.text.startswith("http"):
        data = await state.update_data(url=message.text)
        await state.set_state(FilmCreateForm.photo)
        await message.answer(f"Надайте фото для афіши фільму: {data.get('title')}",
                             reply_markup=cancel_states_keyboard())
    else:
        data = await state.get_data()
        print(data)
        await message.answer(f"Посилання некоректне, надайте інше: {data.get('title')}")


@router.message(FilmCreateForm.photo)
@router.message(F.photo)
async def proces_photo_binary(message: Message, state: FSMContext) -> None:
    # збережемо найбільший розмір фото
    print(message.photo)
    if message.photo:
        photo = message.photo[-1]
        photo_id = photo.file_id

        data = await state.update_data(photo=photo_id)
        await state.set_state(FilmCreateForm.rating)
        await message.answer(f"Надайте рейтинг фільму: {data.get('title')}",
                             reply_markup=ReplyKeyboardRemove())
    else:
        data = await state.get_data()
        await message.answer(f"Це не фото, додай афішу до : {data.get('title')}")


# Завершуемо кінцевий автомат
@router.message(FilmCreateForm.rating)
async def proces_rating(message: Message, state: FSMContext) -> None:
    data = await state.update_data(rating=message.text)
    await state.clear()  # stop FSM

    print(data)

    # додаемо фільм у файл
    create_film(data)
    await message.answer(f"Фільму  {data.get('title')} додано до бібліотеки",
                         reply_markup=main_menu_keyboard())


@router.message(Command("clear"))
async def clear_handler(message: Message, state: FSMContext):
    await state.clear()
    chat = message.chat
    _id = message.message_id
    while _id > 0:
        try:
            await chat.delete_message(_id)
            print(f"deleting {_id} message")
            _id -= 1
        except Exception:
            break
