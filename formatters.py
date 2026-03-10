import json


def format_full_profile(user: dict) -> str:
    """Return the full formatted profile string for a user."""
    try:
        history = json.loads(user.get("name_history") or "[]")
        history_str = ", ".join(history) if history else "—"
    except (json.JSONDecodeError, TypeError):
        history_str = str(user.get("name_history", "—"))

    username_display = f"@{user['username']}" if user.get("username") else "—"

    return (
        "📋 <b>Profile:</b>\n"
        f"  🆔 ID: <code>{user['telegram_id']}</code>\n"
        f"  👤 Username: {username_display}\n"
        f"  📛 Name: {user.get('first_name') or '—'}\n"
        "\n"
        "📊 <b>Statistics:</b>\n"
        f"  💬 Messages: <b>{user.get('messages_count', 0):,}</b>\n"
        f"  👥 Groups: <b>{user.get('groups_count', 0)}</b>\n"
        f"  📢 Channels: <b>{user.get('channels_count', 0)}</b>\n"
        f"  🖼 Media: <b>{user.get('media_percent', 0.0):.1f}%</b>\n"
        f"  💬 Replies: <b>{user.get('reply_percent', 0.0):.1f}%</b>\n"
        "\n"
        "✨ <b>Extra:</b>\n"
        f"  ⭐ Favorite chat: {user.get('favorite_chat') or '—'}\n"
        f"  🕓 Name history: {history_str}"
    )


def format_profile_section(user: dict) -> str:
    username_display = f"@{user['username']}" if user.get("username") else "—"
    return (
        "👤 <b>Profile</b>\n\n"
        f"🆔 <b>ID:</b> <code>{user['telegram_id']}</code>\n"
        f"👤 <b>Username:</b> {username_display}\n"
        f"📛 <b>Name:</b> {user.get('first_name') or '—'}"
    )


def format_groups_section(user: dict) -> str:
    return (
        "👥 <b>Groups & Channels</b>\n\n"
        f"👥 <b>Groups joined:</b> {user.get('groups_count', 0)}\n"
        f"📢 <b>Channels joined:</b> {user.get('channels_count', 0)}\n"
        f"⭐ <b>Favorite chat:</b> {user.get('favorite_chat') or '—'}"
    )


def format_messages_section(user: dict) -> str:
    return (
        "💬 <b>Messages</b>\n\n"
        f"📨 <b>Total messages:</b> {user.get('messages_count', 0):,}\n"
        f"🖼 <b>Media share:</b> {user.get('media_percent', 0.0):.1f}%\n"
        f"↩️ <b>Reply rate:</b> {user.get('reply_percent', 0.0):.1f}%"
    )


def format_analysis_section(user: dict) -> str:
    msg = user.get("messages_count", 0)
    media = user.get("media_percent", 0.0)
    replies = user.get("reply_percent", 0.0)
    groups = user.get("groups_count", 0)

    # Simple activity label
    if msg >= 5000:
        activity = "🔥 Very Active"
    elif msg >= 2000:
        activity = "✅ Active"
    elif msg >= 500:
        activity = "😐 Moderate"
    else:
        activity = "😴 Low Activity"

    # Communication style
    if replies >= 50:
        style = "💬 Highly conversational"
    elif media >= 50:
        style = "📸 Media-heavy sender"
    elif replies >= 25:
        style = "↩️ Responsive"
    else:
        style = "📝 Broadcaster"

    return (
        "📊 <b>Analysis</b>\n\n"
        f"🏃 <b>Activity level:</b> {activity}\n"
        f"🎭 <b>Communication style:</b> {style}\n"
        f"📈 <b>Avg msgs per group:</b> {msg // groups if groups else msg:,}\n"
        f"🖼 <b>Media usage:</b> {media:.1f}%\n"
        f"↩️ <b>Reply engagement:</b> {replies:.1f}%"
    )


def format_share_text(user: dict) -> str:
    username_display = f"@{user['username']}" if user.get("username") else "—"
    return (
        f"👤 <b>{user.get('first_name') or 'User'}</b> ({username_display})\n"
        f"🆔 ID: <code>{user['telegram_id']}</code>\n"
        f"💬 Messages: {user.get('messages_count', 0):,} | "
        f"👥 Groups: {user.get('groups_count', 0)} | "
        f"📢 Channels: {user.get('channels_count', 0)}\n"
        f"⭐ Favorite: {user.get('favorite_chat') or '—'}\n\n"
        "📲 <i>Analyzed by @DatabaseAnalyzerBot</i>"
    )
