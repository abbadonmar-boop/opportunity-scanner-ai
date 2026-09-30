from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from .discord_collector import (
    DiscordCollectorConfig,
    DiscordGatewayStopFail,
    NormalizedDiscordMessage,
    build_dedup_key,
    parse_gateway_message_create,
    validate_message_access,
)
from .filter_engine import evaluate_filter


D053_CREATE_TEXT = "Synthetic D053 paid beta testing opportunity"
D053_UPDATE_TEXT = "Synthetic D053 unpaid testing opportunity"

D053_LIFECYCLE_SEQUENCE = (
    "MESSAGE_CREATE",
    "MESSAGE_UPDATE",
    "MESSAGE_DELETE",
)


@dataclass(frozen=True)
class DiscordD053InMemoryResult:
    message_id: str
    dedup_key: str
    create_filter_state: str
    update_filter_state: str
    lifecycle_events: tuple[str, ...]
    deleted: bool


def _require_event_data(
    payload: Mapping[str, Any],
    event_type: str,
) -> Mapping[str, Any]:
    data = payload.get("d")

    if not isinstance(data, Mapping):
        raise DiscordGatewayStopFail(
            f"{event_type} data is missing"
        )

    return data


def _require_numeric_id(
    value: object,
    field_name: str,
) -> str:
    if not isinstance(value, str):
        raise DiscordGatewayStopFail(
            f"{field_name} must be a string"
        )

    normalized = value.strip()

    if not normalized or not normalized.isdigit():
        raise DiscordGatewayStopFail(
            f"{field_name} must be a numeric Discord ID"
        )

    return normalized


class DiscordD053InMemoryVerifier:
    """
    D-053 lifecycle verification state.

    No persistence, REST, Gateway connection, Telegram or AI / LLM work
    is performed by this class.
    """

    def __init__(
        self,
        config: DiscordCollectorConfig,
    ) -> None:
        self._config = config
        self._events: list[str] = []
        self._message: NormalizedDiscordMessage | None = None
        self._message_id: str | None = None
        self._dedup_key: str | None = None
        self._create_filter_state: str | None = None
        self._update_filter_state: str | None = None
        self._deleted = False

    def handle(
        self,
        payload: Mapping[str, Any],
    ) -> None:
        if len(self._events) >= len(D053_LIFECYCLE_SEQUENCE):
            raise DiscordGatewayStopFail(
                "D-053 lifecycle already completed"
            )

        event_type = payload.get("t")
        expected_event = D053_LIFECYCLE_SEQUENCE[
            len(self._events)
        ]

        if event_type != expected_event:
            raise DiscordGatewayStopFail(
                "D-053 lifecycle event order is invalid"
            )

        if event_type == "MESSAGE_CREATE":
            self._handle_create(payload)
        elif event_type == "MESSAGE_UPDATE":
            self._handle_update(payload)
        elif event_type == "MESSAGE_DELETE":
            self._handle_delete(payload)
        else:
            raise DiscordGatewayStopFail(
                "Unexpected D-053 lifecycle event"
            )

        self._events.append(event_type)

    def _handle_create(
        self,
        payload: Mapping[str, Any],
    ) -> None:
        if self._message is not None:
            raise DiscordGatewayStopFail(
                "D-053 MESSAGE_CREATE was already processed"
            )

        message = parse_gateway_message_create(
            payload,
            self._config,
        )

        if message.content_text != D053_CREATE_TEXT:
            raise DiscordGatewayStopFail(
                "D-053 CREATE content does not match the approved synthetic text"
            )

        filter_state = evaluate_filter(
            None,
            message.content_text,
        )

        if filter_state != "PASS":
            raise DiscordGatewayStopFail(
                "D-053 CREATE did not produce expected Module 6 PASS"
            )

        self._message = message
        self._message_id = message.message_id
        self._dedup_key = build_dedup_key(message)
        self._create_filter_state = filter_state

    def _handle_update(
        self,
        payload: Mapping[str, Any],
    ) -> None:
        if self._message is None or self._message_id is None:
            raise DiscordGatewayStopFail(
                "D-053 UPDATE received before CREATE"
            )

        data = _require_event_data(
            payload,
            "MESSAGE_UPDATE",
        )

        guild_id = _require_numeric_id(
            data.get("guild_id"),
            "guild_id",
        )
        channel_id = _require_numeric_id(
            data.get("channel_id"),
            "channel_id",
        )
        message_id = _require_numeric_id(
            data.get("id"),
            "message_id",
        )

        validate_message_access(
            guild_id,
            channel_id,
            self._config,
        )

        if (
            guild_id != self._message.guild_id
            or channel_id != self._message.channel_id
            or message_id != self._message_id
        ):
            raise DiscordGatewayStopFail(
                "D-053 UPDATE stable message identity does not match CREATE"
            )

        content = data.get("content")

        if content != D053_UPDATE_TEXT:
            raise DiscordGatewayStopFail(
                "D-053 UPDATE content does not match the approved synthetic text"
            )

        filter_state = evaluate_filter(
            None,
            content,
        )

        if filter_state != "REJECT":
            raise DiscordGatewayStopFail(
                "D-053 UPDATE did not produce expected Module 6 REJECT"
            )

        current_identity = (
            guild_id,
            channel_id,
            message_id,
        )
        create_identity = (
            self._message.guild_id,
            self._message.channel_id,
            self._message.message_id,
        )

        if current_identity != create_identity:
            raise DiscordGatewayStopFail(
                "D-053 dedup identity changed after UPDATE"
            )

        self._update_filter_state = filter_state

    def _handle_delete(
        self,
        payload: Mapping[str, Any],
    ) -> None:
        if (
            self._message is None
            or self._message_id is None
            or self._update_filter_state != "REJECT"
        ):
            raise DiscordGatewayStopFail(
                "D-053 DELETE received before verified UPDATE"
            )

        data = _require_event_data(
            payload,
            "MESSAGE_DELETE",
        )

        guild_id = _require_numeric_id(
            data.get("guild_id"),
            "guild_id",
        )
        channel_id = _require_numeric_id(
            data.get("channel_id"),
            "channel_id",
        )
        message_id = _require_numeric_id(
            data.get("id"),
            "message_id",
        )

        validate_message_access(
            guild_id,
            channel_id,
            self._config,
        )

        if (
            guild_id != self._message.guild_id
            or channel_id != self._message.channel_id
            or message_id != self._message_id
        ):
            raise DiscordGatewayStopFail(
                "D-053 DELETE stable message identity does not match CREATE"
            )

        self._deleted = True
        self._message = None

    def result(self) -> DiscordD053InMemoryResult:
        if tuple(self._events) != D053_LIFECYCLE_SEQUENCE:
            raise DiscordGatewayStopFail(
                "D-053 lifecycle is incomplete"
            )

        if (
            self._message_id is None
            or self._dedup_key is None
            or self._create_filter_state != "PASS"
            or self._update_filter_state != "REJECT"
            or not self._deleted
        ):
            raise DiscordGatewayStopFail(
                "D-053 in-memory verification state is incomplete"
            )

        return DiscordD053InMemoryResult(
            message_id=self._message_id,
            dedup_key=self._dedup_key,
            create_filter_state=self._create_filter_state,
            update_filter_state=self._update_filter_state,
            lifecycle_events=tuple(self._events),
            deleted=self._deleted,
        )
