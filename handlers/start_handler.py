from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from keyboards.start_kb import start_kb

router = Router()


class UserState(StatesGroup):
    topic_inputting = State()
    description_inputting = State()
    time_choosing = State()
    date_choosing = State()
    picture_choosing = State()
    waiting_for_post = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(text="Привіт\!\n\n"
                              "Натисніть кнопку \"Створити пост\" для початку роботи",
                         reply_markup=start_kb())


@router.message(F.text.lower() == "скасувати")
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(text="Дію скасовано",
                         reply_markup=start_kb())