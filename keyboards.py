from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu_keyboard() -> InlineKeyboardMarkup:
    """Main menu with 5 action buttons."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👤 Profile",   callback_data="menu_profile"),
        InlineKeyboardButton(text="👥 Groups",    callback_data="menu_groups"),
    )
    builder.row(
        InlineKeyboardButton(text="💬 Messages",  callback_data="menu_messages"),
        InlineKeyboardButton(text="📊 Analysis",  callback_data="menu_analysis"),
    )
    builder.row(
        InlineKeyboardButton(text="🔗 Share",     callback_data="menu_share"),
    )
    return builder.as_markup()


def search_result_keyboard(telegram_id: int) -> InlineKeyboardMarkup:
    """Buttons shown after a successful user lookup."""
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="👤 Profile",   callback_data=f"view_profile_{telegram_id}"),
        InlineKeyboardButton(text="📊 Analysis",  callback_data=f"view_analysis_{telegram_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="💬 Messages",  callback_data=f"view_messages_{telegram_id}"),
        InlineKeyboardButton(text="👥 Groups",    callback_data=f"view_groups_{telegram_id}"),
    )
    builder.row(
        InlineKeyboardButton(text="🔗 Share",     callback_data=f"share_{telegram_id}"),
        InlineKeyboardButton(text="🔙 Menu",      callback_data="back_to_menu"),
    )
    return builder.as_markup()


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="🔙 Back to Menu", callback_data="back_to_menu")
    )
    return builder.as_markup()
