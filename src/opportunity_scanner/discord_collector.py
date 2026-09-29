from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from hashlib import sha256
from typing import Any, Protocol

import psycopg

from .filter_engine import evaluate_filter


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

class DiscordDatabaseConfig(Protocol):
    dbname: str
    user: str
    password: str
    host: str
    port: int



def _validate_existing_message_create(
    row: tuple[object, ...],
    message: NormalizedDiscordMessage,
    dedup_key: str,
) -> tuple[int, str]:
    row_id, stored_content, stored_dedup_key, stored_filter_state = row

    if str(stored_content) != message.content_text:
        raise DiscordPayloadError(
            "Conflicting duplicate MESSAGE_CREATE must not overwrite stored content"
        )

    if str(stored_dedup_key) != dedup_key:
        raise DiscordCollectorError(
            "Stored Discord dedup identity does not match MESSAGE_CREATE identity"
        )

    filter_state = str(stored_filter_state)

    if filter_state not in ("PENDING", "PASS", "REJECT"):
        raise DiscordCollectorError(
            "Stored Discord filter_state is invalid"
        )

    return int(row_id), filter_state


def persist_gateway_message_create(
    payload: Mapping[str, Any],
    config: DiscordCollectorConfig,
    database: DiscordDatabaseConfig,
    collected_at: datetime | None = None,
) -> tuple[int, bool]:
    message = parse_gateway_message_create(
        payload,
        config,
        collected_at=collected_at,
    )
    dedup_key = build_dedup_key(message)

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id,
                       content_text,
                       dedup_key,
                       filter_state
                FROM discord_source_items
                WHERE guild_id = %s
                  AND channel_id = %s
                  AND message_id = %s
                """,
                (
                    message.guild_id,
                    message.channel_id,
                    message.message_id,
                ),
            )
            existing = cursor.fetchone()

            if existing is not None:
                row_id, _filter_state = _validate_existing_message_create(
                    existing,
                    message,
                    dedup_key,
                )
                return row_id, False

            cursor.execute(
                """
                INSERT INTO discord_source_items (
                    guild_id,
                    channel_id,
                    message_id,
                    author_id,
                    content_text,
                    published_at,
                    edited_at,
                    collected_at,
                    dedup_key,
                    filter_state
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (guild_id, channel_id, message_id)
                DO NOTHING
                RETURNING id
                """,
                (
                    message.guild_id,
                    message.channel_id,
                    message.message_id,
                    message.author_id,
                    message.content_text,
                    message.published_at,
                    message.edited_at,
                    message.collected_at,
                    dedup_key,
                    "PENDING",
                ),
            )
            inserted = cursor.fetchone()

            if inserted is not None:
                return int(inserted[0]), True

            # A concurrent identical CREATE may have won the insert race.
            cursor.execute(
                """
                SELECT id,
                       content_text,
                       dedup_key,
                       filter_state
                FROM discord_source_items
                WHERE guild_id = %s
                  AND channel_id = %s
                  AND message_id = %s
                """,
                (
                    message.guild_id,
                    message.channel_id,
                    message.message_id,
                ),
            )
            concurrent = cursor.fetchone()

            if concurrent is None:
                raise DiscordCollectorError(
                    "MESSAGE_CREATE persistence failed"
                )

            row_id, _filter_state = _validate_existing_message_create(
                concurrent,
                message,
                dedup_key,
            )
            return row_id, False


def persist_discord_filter_result(
    row_id: int,
    filter_state: str,
    database: DiscordDatabaseConfig,
) -> str:
    if filter_state not in ("PASS", "REJECT"):
        raise DiscordCollectorError(
            "Discord filter result must be PASS or REJECT"
        )

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE discord_source_items
                SET filter_state = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                  AND filter_state = 'PENDING'
                RETURNING filter_state
                """,
                (
                    filter_state,
                    row_id,
                ),
            )
            row = cursor.fetchone()

            if row is None:
                raise DiscordCollectorError(
                    "Discord PENDING filter-state persistence failed"
                )

            return str(row[0])


def process_pending_discord_source_item(
    row_id: int,
    database: DiscordDatabaseConfig,
) -> str:
    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT content_text, filter_state
                FROM discord_source_items
                WHERE id = %s
                """,
                (row_id,),
            )
            row = cursor.fetchone()

    if row is None:
        raise DiscordCollectorError(
            "Discord source item for filtering was not found"
        )

    content_text, stored_filter_state = row
    filter_state = str(stored_filter_state)

    if filter_state in ("PASS", "REJECT"):
        return filter_state

    if filter_state != "PENDING":
        raise DiscordCollectorError(
            "Stored Discord filter_state is invalid"
        )

    result = evaluate_filter(
        None,
        str(content_text),
    )

    return persist_discord_filter_result(
        row_id,
        result,
        database,
    )


def process_gateway_message_create(
    payload: Mapping[str, Any],
    config: DiscordCollectorConfig,
    database: DiscordDatabaseConfig,
    collected_at: datetime | None = None,
) -> tuple[int, bool, str]:
    row_id, created = persist_gateway_message_create(
        payload,
        config,
        database,
        collected_at=collected_at,
    )

    filter_state = process_pending_discord_source_item(
        row_id,
        database,
    )

    return row_id, created, filter_state


def process_gateway_message_update(
    payload: Mapping[str, Any],
    config: DiscordCollectorConfig,
    database: DiscordDatabaseConfig,
    collected_at: datetime | None = None,
) -> tuple[int, bool, str]:
    row_id, created = persist_gateway_message_update(
        payload,
        config,
        database,
        collected_at=collected_at,
    )

    filter_state = process_pending_discord_source_item(
        row_id,
        database,
    )

    return row_id, created, filter_state


def _normalize_collected_at(
    collected_at: datetime | None,
) -> datetime:
    collected = collected_at or datetime.now(timezone.utc)

    if collected.tzinfo is None:
        raise DiscordPayloadError("collected_at must include a timezone")

    return collected.astimezone(timezone.utc)


def _validate_lifecycle_pair(
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

    if (
        normalized_guild_id,
        normalized_channel_id,
    ) not in config.allowed_guild_channels:
        raise DiscordAccessError(
            "Guild/channel pair is not in the configured allowlist"
        )


def persist_gateway_message_update(
    payload: Mapping[str, Any],
    collector_config: DiscordCollectorConfig,
    database: DiscordDatabaseConfig,
    collected_at: datetime | None = None,
) -> tuple[int, bool]:
    if payload.get("t") != "MESSAGE_UPDATE":
        raise DiscordPayloadError("Gateway event is not MESSAGE_UPDATE")

    data = payload.get("d")

    if not isinstance(data, Mapping):
        raise DiscordPayloadError("Gateway MESSAGE_UPDATE data is missing")

    guild_id = _require_snowflake(data.get("guild_id"), "guild_id")
    channel_id = _require_snowflake(data.get("channel_id"), "channel_id")
    message_id = _require_snowflake(data.get("id"), "message_id")

    validate_message_access(guild_id, channel_id, collector_config)

    collected = _normalize_collected_at(collected_at)

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id,
                       guild_id,
                       author_id,
                       content_text,
                       published_at,
                       edited_at
                FROM discord_source_items
                WHERE channel_id = %s
                  AND message_id = %s
                """,
                (channel_id, message_id),
            )
            existing = cursor.fetchone()

            if existing is None:
                author = data.get("author")

                if not isinstance(author, Mapping):
                    raise DiscordPayloadError(
                        "Unknown MESSAGE_UPDATE requires message author"
                    )

                author_id = _require_snowflake(
                    author.get("id"),
                    "author_id",
                )

                content = data.get("content")

                if not isinstance(content, str):
                    raise DiscordPayloadError(
                        "Unknown MESSAGE_UPDATE requires message content"
                    )

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
                    raise DiscordPayloadError(
                        "Unknown MESSAGE_UPDATE requires timestamp"
                    )

                message = NormalizedDiscordMessage(
                    guild_id=guild_id,
                    channel_id=channel_id,
                    message_id=message_id,
                    author_id=author_id,
                    content_text=content,
                    published_at=published_at,
                    edited_at=edited_at,
                    collected_at=collected,
                )

                cursor.execute(
                    """
                    INSERT INTO discord_source_items (
                        guild_id,
                        channel_id,
                        message_id,
                        author_id,
                        content_text,
                        published_at,
                        edited_at,
                        collected_at,
                        dedup_key
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        message.guild_id,
                        message.channel_id,
                        message.message_id,
                        message.author_id,
                        message.content_text,
                        message.published_at,
                        message.edited_at,
                        message.collected_at,
                        build_dedup_key(message),
                    ),
                )
                inserted = cursor.fetchone()

                if inserted is None:
                    raise DiscordCollectorError(
                        "Unknown MESSAGE_UPDATE persistence failed"
                    )

                return int(inserted[0]), True

            (
                row_id,
                stored_guild_id,
                stored_author_id,
                stored_content_text,
                stored_published_at,
                stored_edited_at,
            ) = existing

            if str(stored_guild_id) != guild_id:
                raise DiscordPayloadError(
                    "MESSAGE_UPDATE guild_id does not match stored message"
                )

            author_id = str(stored_author_id)

            if "author" in data:
                author = data.get("author")

                if not isinstance(author, Mapping):
                    raise DiscordPayloadError(
                        "MESSAGE_UPDATE author must be an object"
                    )

                author_id = _require_snowflake(
                    author.get("id"),
                    "author_id",
                )

            content_text = str(stored_content_text)

            if "content" in data:
                content = data.get("content")

                if not isinstance(content, str):
                    raise DiscordPayloadError(
                        "MESSAGE_UPDATE content must be a string"
                    )

                content_text = content

            published_at = stored_published_at

            if "timestamp" in data:
                parsed_published_at = _parse_timestamp(
                    data.get("timestamp"),
                    "timestamp",
                    required=True,
                )

                if parsed_published_at is None:
                    raise DiscordPayloadError("timestamp is required")

                published_at = parsed_published_at

            edited_at = stored_edited_at

            if "edited_timestamp" in data:
                edited_at = _parse_timestamp(
                    data.get("edited_timestamp"),
                    "edited_timestamp",
                    required=False,
                )

            cursor.execute(
                """
                UPDATE discord_source_items
                SET author_id = %s,
                    content_text = %s,
                    published_at = %s,
                    edited_at = %s,
                    collected_at = %s,
                    filter_state = 'PENDING',
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id
                """,
                (
                    author_id,
                    content_text,
                    published_at,
                    edited_at,
                    collected,
                    row_id,
                ),
            )
            updated = cursor.fetchone()

            if updated is None:
                raise DiscordCollectorError(
                    "MESSAGE_UPDATE persistence failed"
                )

            return int(updated[0]), False


def persist_gateway_message_delete(
    payload: Mapping[str, Any],
    collector_config: DiscordCollectorConfig,
    database: DiscordDatabaseConfig,
) -> bool:
    if payload.get("t") != "MESSAGE_DELETE":
        raise DiscordPayloadError("Gateway event is not MESSAGE_DELETE")

    data = payload.get("d")

    if not isinstance(data, Mapping):
        raise DiscordPayloadError("Gateway MESSAGE_DELETE data is missing")

    channel_id = _require_snowflake(data.get("channel_id"), "channel_id")
    message_id = _require_snowflake(data.get("id"), "message_id")

    event_guild_id: str | None = None

    if data.get("guild_id") is not None:
        event_guild_id = _require_snowflake(
            data.get("guild_id"),
            "guild_id",
        )
        _validate_lifecycle_pair(
            event_guild_id,
            channel_id,
            collector_config,
        )
    else:
        validate_collector_config(collector_config)

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, guild_id
                FROM discord_source_items
                WHERE channel_id = %s
                  AND message_id = %s
                """,
                (channel_id, message_id),
            )
            existing = cursor.fetchone()

            if existing is None:
                return False

            row_id, stored_guild_id = existing
            stored_guild = str(stored_guild_id)

            _validate_lifecycle_pair(
                stored_guild,
                channel_id,
                collector_config,
            )

            if (
                event_guild_id is not None
                and event_guild_id != stored_guild
            ):
                raise DiscordPayloadError(
                    "MESSAGE_DELETE guild_id does not match stored message"
                )

            cursor.execute(
                """
                DELETE FROM discord_source_items
                WHERE id = %s
                RETURNING id
                """,
                (row_id,),
            )
            deleted = cursor.fetchone()

            if deleted is None:
                raise DiscordCollectorError(
                    "MESSAGE_DELETE persistence failed"
                )

            return True


def persist_gateway_message_delete_bulk(
    payload: Mapping[str, Any],
    collector_config: DiscordCollectorConfig,
    database: DiscordDatabaseConfig,
) -> int:
    if payload.get("t") != "MESSAGE_DELETE_BULK":
        raise DiscordPayloadError(
            "Gateway event is not MESSAGE_DELETE_BULK"
        )

    data = payload.get("d")

    if not isinstance(data, Mapping):
        raise DiscordPayloadError(
            "Gateway MESSAGE_DELETE_BULK data is missing"
        )

    channel_id = _require_snowflake(data.get("channel_id"), "channel_id")

    raw_ids = data.get("ids")

    if not isinstance(raw_ids, list) or not raw_ids:
        raise DiscordPayloadError(
            "MESSAGE_DELETE_BULK ids must be a non-empty list"
        )

    message_ids = list(
        dict.fromkeys(
            _require_snowflake(value, "message_id")
            for value in raw_ids
        )
    )

    event_guild_id: str | None = None

    if data.get("guild_id") is not None:
        event_guild_id = _require_snowflake(
            data.get("guild_id"),
            "guild_id",
        )
        _validate_lifecycle_pair(
            event_guild_id,
            channel_id,
            collector_config,
        )
    else:
        validate_collector_config(collector_config)

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT message_id, guild_id
                FROM discord_source_items
                WHERE channel_id = %s
                  AND message_id = ANY(%s)
                """,
                (channel_id, message_ids),
            )
            existing_rows = cursor.fetchall()

            for stored_message_id, stored_guild_id in existing_rows:
                stored_guild = str(stored_guild_id)

                _validate_lifecycle_pair(
                    stored_guild,
                    channel_id,
                    collector_config,
                )

                if (
                    event_guild_id is not None
                    and event_guild_id != stored_guild
                ):
                    raise DiscordPayloadError(
                        "MESSAGE_DELETE_BULK guild_id does not match "
                        f"stored message {stored_message_id}"
                    )

            if not existing_rows:
                return 0

            cursor.execute(
                """
                DELETE FROM discord_source_items
                WHERE channel_id = %s
                  AND message_id = ANY(%s)
                RETURNING id
                """,
                (channel_id, message_ids),
            )

            return len(cursor.fetchall())
