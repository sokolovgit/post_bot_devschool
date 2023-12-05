from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from datetime import date, timedelta, datetime
from contextlib import suppress
from aiogram.exceptions import TelegramBadRequest


from handlers.start_handler import UserState
from keyboards.cancel_kb import cancel_kb
from keyboards.start_kb import start_kb
from keyboards.time_inline_kb import time_chose_kb, TimeCallbackFactory
from keyboards.picture_cancellation_inline_kb import picture_cancellation_kb

router = Router()


@router.message(F.text == "Створити пост")
async def make_post(message: Message, state: FSMContext):
    await message.answer(text="Введіть тему для майбутнього допису",
                         reply_markup=cancel_kb())
    await state.set_state(UserState.topic_inputting)


@router.message(UserState.topic_inputting, F.text)
async def get_topic(message: Message, state: FSMContext):
    await state.update_data(chosen_topic=message.text)
    await message.answer(text="Тепер введіть опис для допису",
                         reply_markup=cancel_kb())
    await state.set_state(UserState.description_inputting)


@router.message(UserState.topic_inputting)
async def empty_topic(message: Message):
    await message.answer(text="Допис не може бути без теми\!\n\n"
                              "Будь ласка, введіть тему для допису",
                         reply_markup=cancel_kb())


@router.message(UserState.description_inputting, F.text)
async def get_description(message: Message, state: FSMContext):
    await state.update_data(chosen_description=message.text)
    await state.update_data(sender_time=message.date)
    user_data = await state.get_data()
    await message.answer(text="Оберіть запланований час для допису",
                         reply_markup=time_chose_kb(user_data['sender_time']))
    await state.set_state(UserState.time_choosing)


@router.message(UserState.description_inputting)
async def empty_description(message: Message):
    await message.answer(text="Допис не може бути без опису\!\n\n"
                              "Будь ласка, введіть опис для допису",
                         reply_markup=cancel_kb())


async def update_time_chosen(message: Message, new_value: date):
    with suppress(TelegramBadRequest):
        await message.edit_text(text="Оберіть запланований час для допису",
                                reply_markup=time_chose_kb(new_value))


@router.callback_query(TimeCallbackFactory.filter(F.action == "change"),
                       UserState.time_choosing)
async def callbacks_time_change(callback: CallbackQuery,
                                callback_data: TimeCallbackFactory,
                                state: FSMContext):
    user_data = await state.get_data()

    await state.update_data(sender_time=user_data['sender_time'] + callback_data.value)

    user_data = await state.get_data()

    await update_time_chosen(callback.message, user_data['sender_time'])
    await callback.answer()


@router.callback_query(TimeCallbackFactory.filter(F.action == "set"),
                       UserState.time_choosing)
async def callback_time_set(callback: CallbackQuery,
                            state: FSMContext):

    user_data = await state.get_data()
    time = (user_data['sender_time'] + timedelta(hours=2)).strftime("%H:%M")

    await state.update_data(sender_time=time)

    await callback.message.edit_text(text=f"Ваш запланований час: {time}")
    await callback.answer()

    await callback.message.answer(text="Введіть заплановану дату в форматі дд\.мм\.РР "
                                       "\(дата не може бути в минулому\)",
                                  reply_markup=cancel_kb())

    await state.set_state(UserState.date_choosing)


def is_valid_date(date_str):
    try:
        user_date = datetime.strptime(date_str, '%d.%m.%Y')
        if user_date.date() >= date.today():
            return True
    except ValueError:
        return False


@router.message(UserState.date_choosing, F.text)
async def get_date(message: Message, state: FSMContext):

    if not is_valid_date(message.text):
        await message.answer(text="Неправильний формат введеня або дата в минулому\. Спробуйте ще раз",
                             reply_markup=cancel_kb())
        return

    await state.update_data(user_date=message.text)
    await message.answer("Відправте зображення до цього допису",
                         reply_markup=picture_cancellation_kb())
    await state.set_state(UserState.picture_choosing)


@router.callback_query(F.data == "cancel_picture")
async def picture_cancelled(callback: CallbackQuery, state: FSMContext):

    await state.update_data(file_id=None)

    await callback.answer()

    await callback.message.answer(text="Ваш допис має такий вигляд:",
                                  reply_markup=start_kb())

    user_data = await state.get_data()
    topic = user_data['chosen_topic']
    description = user_data['chosen_description'].replace('.', '\.')
    time = user_data['sender_time'].replace('.', '\.')
    user_date = user_data['user_date'].replace('.', '\.')

    post_text = (f"*Тема*: {topic}\n\n"
                 f"*Опис*: {description}\n\n"
                 f"*Час та дата*: {time} {user_date}")

    await callback.message.answer(text=post_text,
                                  reply_markup=start_kb())
    await state.clear()


@router.message(UserState.picture_choosing, F.photo)
async def get_picture(message: Message, state: FSMContext):

    await state.update_data(file_id=message.photo[-1].file_id)

    await message.answer(text="Ваш допис має такий вигляд:",
                         reply_markup=start_kb())

    user_data = await state.get_data()

    topic = user_data['chosen_topic']
    description = user_data['chosen_description'].replace('.', '\.')
    time = user_data['sender_time'].replace('.', '\.')
    user_date = user_data['user_date'].replace('.', '\.')
    picture = user_data['file_id']

    post_text = (f"*Тема*: {topic}\n\n"
                 f"*Опис*: {description}\n\n"
                 f"*Час та дата*: {time} {user_date}")

    await message.answer_photo(picture,
                               caption=post_text,
                               reply_markup=start_kb())
