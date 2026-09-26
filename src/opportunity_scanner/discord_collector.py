from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any


class DiscordCollectorError(RuntimeError):
    pass


class DiscordConfigError(DiscordCollectorError):
    pass


class DiscordAccessError(DiscordCollectorError):
    pass


class DiscordPayloadError(DiscordCollectorError):
    pass


@dataclass(frozen=True)
class DiscordCollectorConfig:
    allowed_guild_channels: frozenset[tuple[str, str]]
    message_content_intent_enabled: bool
    administrator_permission_requested: bool = False


@dataclass(frozen=True)
class NormalizedDiscordMessage:
    guild_id: str
    channel_id: str
    message_id: str
    author_id: str
    content_text: str
    published_at: datetime
    edited_at: datetime | None
    collected_at: datetime


def _require_snowflake(value: object, field_name: str) -> str:
    if not isinstance(value, str):
        raise DiscordPayloadError(f"{field_name} must be a string")

    normalized = value.strip()

    if not normalized or not normalized.isdigit():
        raise DiscordPayloadError(f"{field_name} must be a numeric Discord ID")

    return normalized


def _parse_timestamp(
    value: object,
    field_name: str,
    *,
    required: bool,
) -> datetime | None:
    if value is None:
        if required:
            raise DiscordPayloadError(f"{field_name} is required")
        return None

    if not isinstance(value, str) or not value.strip():
        raise DiscordPayloadError(f"{field_name} must be an ISO-8601 string")

    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise DiscordPayloadError(
            f"{field_name} must be a valid ISO-8601 timestamp"
        ) from exc

    if parsed.tzinfo is None:
        raise DiscordPayloadError(f"{field_name} must include a timezone")

    return parsed.astimezone(timezone.utc)


def validate_collector_config(config: DiscordCollectorConfig) -> None:
    if not config.allowed_guild_channels:
        raise DiscordConfigError(
            "At least one allowed guild/channel pair is required"
        )

    for pair in config.allowed_guild_channels:
        if not isinstance(pair, tuple) or len(pair) != 2:
            raise DiscordConfigError(
                "Every allowlist entry must be a guild/channel pair"
            )

        guild_id, channel_id = pair

        try:
            _require_snowflake(guild_id, "allowed guild ID")
            _require_snowflake(channel_id, "allowed channel ID")
        except DiscordPayloadError as exc:
            raise DiscordConfigError(str(exc)) from exc

    if not isinstance(config.message_content_intent_enabled, bool):
        raise DiscordConfigError(
            "message_content_intent_enabled must be a boolean"
        )

    if not isinstance(config.administrator_permission_requested, bool):
        raise DiscordConfigError(
            "administrator_permission_requested must be a boolean"
        )

    if config.administrator_permission_requested:
        raise DiscordConfigError(
            "Administrator permission is prohibited by D-050"
        )


def validate_message_access(
    guild_id: str,
    channel_id: str,
    config: DiscordCollectorConfig,
) -> None:
    validate_collector_config(config)

    try:
        normalized_guild_id = _require_snowflake(guild_id, "guild_id")
        normalized_channel_id = _require_snowflake(channel_id, "channel_id")
    except DiscordPayloadError as exc:
        raise DiscordAccessError(str(exc)) from exc

    if not config.message_content_intent_enabled:
        raise DiscordAccessError(
            "MESSAGE_CONTENT intent is not enabled for collection"
        )

    if (
        normalized_guild_id,
        normalized_channel_id,
    ) not in config.allowed_guild_channels:
        raise DiscordAccessError(
            "Guild/channel pair is not in the configured allowlist"
        )


def parse_gateway_message_create(
    payload: Mapping[str, Any],
    config: DiscordCollectorConfig,
    collected_at: datetime | None = None,
) -> NormalizedDiscordMessage:
    if payload.get("t") != "MESSAGE_CREATE":
        raise DiscordPayloadError("Gateway event is not MESSAGE_CREATE")

    data = payload.get("d")

    if not isinstance(data, Mapping):
        raise DiscordPayloadError("Gateway MESSAGE_CREATE data is missing")

    guild_id = _require_snowflake(data.get("guild_id"), "guild_id")
    channel_id = _require_snowflake(data.get("channel_id"), "channel_id")
    message_id = _require_snowflake(data.get("id"), "message_id")

    validate_message_access(guild_id, channel_id, config)

    author = data.get("author")

    if not isinstance(author, Mapping):
        raise DiscordPayloadError("Message author is missing")

    author_id = _require_snowflake(author.get("id"), "author_id")

    content = data.get("content")

    if not isinstance(content, str):
        raise DiscordPayloadError("Message content must be a string")

    published_at = _parse_timestamp(
        data.get("timestamp"),
        "timestamp",
        required=True,
    )
    edited_at = _parse_timestamp(
        data.get("edited_timestamp"),
        "edited_timestamp",
        required=False,
    )

    if published_at is None:
        raise DiscordPayloadError("timestamp is required")

    collected = collected_at or datetime.now(timezone.utc)

    if collected.tzinfo is None:
        raise DiscordPayloadError("collected_at must include a timezone")

    return NormalizedDiscordMessage(
        guild_id=guild_id,
        channel_id=channel_id,
        message_id=message_id,
        author_id=author_id,
        content_text=content,
        published_at=published_at,
        edited_at=edited_at,
        collected_at=collected.astimezone(timezone.utc),
    )


def build_dedup_key(message: NormalizedDiscordMessage) -> str:
    payload = "\n".join(
        (
            "discord",
            message.guild_id,
            message.channel_id,
            message.message_id,
        )
    ).encode("utf-8")

    return sha256(payload).hexdigest()
