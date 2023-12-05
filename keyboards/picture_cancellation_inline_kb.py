from aiogram.utils.keyboard import InlineKeyboardBuilder


def picture_cancellation_kb():

    builder = InlineKeyboardBuilder()
    builder.button(text="Нажміть сюди, щоб пропустити цей крок",
                   callback_data="cancel_picture")
    builder.adjust(1)
    return builder.as_markup()
