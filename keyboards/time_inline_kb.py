from datetime import date, timedelta
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from typing import Optional


class TimeCallbackFactory(CallbackData, prefix="timeset"):
    action: str
    value: Optional[timedelta] = None


def time_chose_kb(current_time: date):

    formatted_time = (current_time + timedelta(hours=2)).strftime("%H:%M")

    builder = InlineKeyboardBuilder()
    builder.button(text="⬆️ 1 год.", callback_data=TimeCallbackFactory(action="change",
                                                                       value=timedelta(hours=1)))
    builder.button(text="⬆️ 10 хв.", callback_data=TimeCallbackFactory(action="change",
                                                                       value=timedelta(minutes=10)))
    builder.button(text=f"{formatted_time}", callback_data=TimeCallbackFactory(action="set"))
    builder.button(text="⬇️ 1 год.", callback_data=TimeCallbackFactory(action="change",
                                                                       value=-timedelta(hours=1)))
    builder.button(text="⬇️ 10 хв.", callback_data=TimeCallbackFactory(action="change",
                                                                       value=-timedelta(minutes=10)))

    builder.adjust(2, 1, 2)
    return builder.as_markup()
