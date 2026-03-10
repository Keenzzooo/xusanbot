import json
import logging
from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from database import get_user_by_id, get_user_by_username, get_top_users, get_all_users
from keyboards import main_menu_keyboard, search_result_keyboard, back_to_menu_keyboard
from formatters import (
    format_full_profile,
    format_profile_section,
    format_groups_section,
    format_messages_section,
    format_analysis_section,
    format_share_text,
)

logger = logging.getLogger(__name__)
router = Router()


# ─── FSM States ────────────────────────────────────────────────────────────────

class SearchStates(StatesGroup):
    waiting_for_input = State()


# ─── Helpers ───────────────────────────────────────────────────────────────────

WELCOME_TEXT = (
    "👋 <b>Welcome to Database Analyzer Bot!</b>\n\n"
    "I can look up any user stored in the database and show you detailed statistics.\n\n"
    "📌 <b>How to search:</b>\n"
    "  • Send a <b>Telegram ID</b> (e.g. <code>123456789</code>)\n"
    "  • Send a <b>username</b> (e.g. <code>@john_doe</code> or <code>john_doe</code>)\n\n"
    "Use /menu to open the main menu."
)

MENU_TEXT = (
    "🗂 <b>Main Menu</b>\n\n"
    "Choose an option below:"
)


async def resolve_user(query: str) -> dict | None:
    """Try to find user by ID or username."""
    query = query.strip()
    if query.lstrip("@").isdigit():
        return await get_user_by_id(int(query.lstrip("@")))
    return await get_user_by_username(query)


# ─── Commands ──────────────────────────────────────────────────────────────────

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(WELCOME_TEXT, parse_mode="HTML", reply_markup=main_menu_keyboard())


@router.message(Command("menu"))
async def cmd_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(MENU_TEXT, parse_mode="HTML", reply_markup=main_menu_keyboard())


@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "🆘 <b>Help</b>\n\n"
        "<b>Commands:</b>\n"
        "/start — Welcome screen\n"
        "/menu — Open main menu\n"
        "/help — This message\n\n"
        "<b>Search:</b>\n"
        "Just send a Telegram ID or username to look someone up.",
        parse_mode="HTML",
        reply_markup=main_menu_keyboard(),
    )


# ─── Plain text search ─────────────────────────────────────────────────────────

@router.message(F.text)
async def handle_search(message: Message, state: FSMContext):
    """Treat any plain text message as a user search query."""
    query = message.text.strip()

    # ignore accidental command-like inputs
    if query.startswith("/"):
        return

    thinking = await message.answer("🔍 <i>Searching…</i>", parse_mode="HTML")

    user = await resolve_user(query)

    if not user:
        await thinking.edit_text(
            f"❌ <b>User not found</b>\n\nNo record for <code>{query}</code> in the database.\n\n"
            "Try another ID or username.",
            parse_mode="HTML",
            reply_markup=back_to_menu_keyboard(),
        )
        return

    text = format_full_profile(user)
    await thinking.edit_text(
        text,
        parse_mode="HTML",
        reply_markup=search_result_keyboard(user["telegram_id"]),
    )


# ─── Menu callbacks ────────────────────────────────────────────────────────────

@router.callback_query(F.data == "back_to_menu")
async def cb_back_to_menu(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.edit_text(
        MENU_TEXT, parse_mode="HTML", reply_markup=main_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_profile")
async def cb_menu_profile(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SearchStates.waiting_for_input)
    await state.update_data(section="profile")
    await callback.message.edit_text(
        "👤 <b>Profile Lookup</b>\n\nSend me a Telegram ID or username:",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_groups")
async def cb_menu_groups(callback: CallbackQuery):
    top = await get_top_users(5)
    lines = ["👥 <b>Top Users by Groups</b>\n"]
    for i, u in enumerate(top, 1):
        uname = f"@{u['username']}" if u.get("username") else f"ID {u['telegram_id']}"
        lines.append(f"{i}. {uname} — <b>{u['groups_count']}</b> groups")
    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_messages")
async def cb_menu_messages(callback: CallbackQuery):
    top = await get_top_users(5)
    lines = ["💬 <b>Top Users by Messages</b>\n"]
    for i, u in enumerate(top, 1):
        uname = f"@{u['username']}" if u.get("username") else f"ID {u['telegram_id']}"
        lines.append(f"{i}. {uname} — <b>{u['messages_count']:,}</b> msgs")
    await callback.message.edit_text(
        "\n".join(lines),
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


@router.callback_query(F.data == "menu_analysis")
async def cb_menu_analysis(callback: CallbackQuery):
    all_users = await get_all_users()
    if not all_users:
        await callback.answer("No data available.", show_alert=True)
        return

    total_msgs = sum(u.get("messages_count", 0) for u in all_users)
    avg_msgs = total_msgs // len(all_users) if all_users else 0
    avg_media = sum(u.get("media_percent", 0) for u in all_users) / len(all_users)
    avg_reply = sum(u.get("reply_percent", 0) for u in all_users) / len(all_users)
    top = max(all_users, key=lambda u: u.get("messages_count", 0))
    top_uname = f"@{top['username']}" if top.get("username") else f"ID {top['telegram_id']}"

    text = (
        "📊 <b>Database Analysis</b>\n\n"
        f"👤 Total users: <b>{len(all_users)}</b>\n"
        f"💬 Total messages: <b>{total_msgs:,}</b>\n"
        f"📈 Avg messages/user: <b>{avg_msgs:,}</b>\n"
        f"🖼 Avg media usage: <b>{avg_media:.1f}%</b>\n"
        f"↩️ Avg reply rate: <b>{avg_reply:.1f}%</b>\n"
        f"🏆 Most active: <b>{top_uname}</b> ({top.get('messages_count', 0):,} msgs)"
    )
    await callback.message.edit_text(
        text, parse_mode="HTML", reply_markup=back_to_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "menu_share")
async def cb_menu_share(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔗 <b>Share a Profile</b>\n\nSend me a Telegram ID or username to generate a shareable profile card:",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer()


# ─── Per-user detail callbacks ─────────────────────────────────────────────────

async def _get_user_from_callback(callback: CallbackQuery, prefix: str) -> dict | None:
    tid_str = callback.data.replace(prefix, "")
    try:
        user = await get_user_by_id(int(tid_str))
    except ValueError:
        user = None
    if not user:
        await callback.answer("User not found.", show_alert=True)
    return user


@router.callback_query(F.data.startswith("view_profile_"))
async def cb_view_profile(callback: CallbackQuery):
    user = await _get_user_from_callback(callback, "view_profile_")
    if not user:
        return
    await callback.message.edit_text(
        format_profile_section(user),
        parse_mode="HTML",
        reply_markup=search_result_keyboard(user["telegram_id"]),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("view_groups_"))
async def cb_view_groups(callback: CallbackQuery):
    user = await _get_user_from_callback(callback, "view_groups_")
    if not user:
        return
    await callback.message.edit_text(
        format_groups_section(user),
        parse_mode="HTML",
        reply_markup=search_result_keyboard(user["telegram_id"]),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("view_messages_"))
async def cb_view_messages(callback: CallbackQuery):
    user = await _get_user_from_callback(callback, "view_messages_")
    if not user:
        return
    await callback.message.edit_text(
        format_messages_section(user),
        parse_mode="HTML",
        reply_markup=search_result_keyboard(user["telegram_id"]),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("view_analysis_"))
async def cb_view_analysis(callback: CallbackQuery):
    user = await _get_user_from_callback(callback, "view_analysis_")
    if not user:
        return
    await callback.message.edit_text(
        format_analysis_section(user),
        parse_mode="HTML",
        reply_markup=search_result_keyboard(user["telegram_id"]),
    )
    await callback.answer()


@router.callback_query(F.data.startswith("share_"))
async def cb_share(callback: CallbackQuery):
    user = await _get_user_from_callback(callback, "share_")
    if not user:
        return
    share_text = format_share_text(user)
    # Send as a new (forwardable) message so the user can forward it
    await callback.message.answer(
        f"🔗 <b>Share this profile card:</b>\n\n{share_text}",
        parse_mode="HTML",
        reply_markup=back_to_menu_keyboard(),
    )
    await callback.answer("Profile card ready to share! ✅")
