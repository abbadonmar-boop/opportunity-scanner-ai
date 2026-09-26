from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from opportunity_scanner.discord_collector import (  # noqa: E402
    DiscordAccessError,
    DiscordCollectorConfig,
    DiscordConfigError,
    DiscordPayloadError,
    NormalizedDiscordMessage,
    build_dedup_key,
    parse_gateway_message_create,
    validate_collector_config,
    validate_message_access,
)


class DiscordCollectorConfigTests(unittest.TestCase):
    def _config(
        self,
        *,
        allowed_guild_channels: frozenset[tuple[str, str]] | None = None,
        message_content_intent_enabled: bool = True,
        administrator_permission_requested: bool = False,
    ) -> DiscordCollectorConfig:
        return DiscordCollectorConfig(
            allowed_guild_channels=allowed_guild_channels
            or frozenset({("1001", "2001")}),
            message_content_intent_enabled=message_content_intent_enabled,
            administrator_permission_requested=administrator_permission_requested,
        )

    def test_valid_config_passes(self) -> None:
        validate_collector_config(self._config())

    def test_empty_allowlist_is_rejected(self) -> None:
        config = DiscordCollectorConfig(
            allowed_guild_channels=frozenset(),
            message_content_intent_enabled=True,
        )

        with self.assertRaises(DiscordConfigError):
            validate_collector_config(config)

    def test_administrator_permission_is_rejected(self) -> None:
        config = self._config(administrator_permission_requested=True)

        with self.assertRaises(DiscordConfigError):
            validate_collector_config(config)

    def test_invalid_allowlist_id_is_rejected(self) -> None:
        config = self._config(
            allowed_guild_channels=frozenset({("guild-one", "2001")})
        )

        with self.assertRaises(DiscordConfigError):
            validate_collector_config(config)

    def test_malformed_allowlist_pair_is_rejected(self) -> None:
        config = DiscordCollectorConfig(
            allowed_guild_channels=frozenset(
                {("1001", "2001", "unexpected")}  # type: ignore[arg-type]
            ),
            message_content_intent_enabled=True,
        )

        with self.assertRaises(DiscordConfigError):
            validate_collector_config(config)

    def test_non_boolean_message_content_flag_is_rejected(self) -> None:
        config = DiscordCollectorConfig(
            allowed_guild_channels=frozenset({("1001", "2001")}),
            message_content_intent_enabled="yes",  # type: ignore[arg-type]
        )

        with self.assertRaises(DiscordConfigError):
            validate_collector_config(config)


class DiscordAccessTests(unittest.TestCase):
    def _config(
        self,
        *,
        message_content_intent_enabled: bool = True,
    ) -> DiscordCollectorConfig:
        return DiscordCollectorConfig(
            allowed_guild_channels=frozenset(
                {
                    ("1001", "2001"),
                    ("1002", "2002"),
                }
            ),
            message_content_intent_enabled=message_content_intent_enabled,
        )

    def test_allowed_guild_channel_pair_passes(self) -> None:
        validate_message_access("1001", "2001", self._config())

    def test_cross_guild_channel_pair_is_rejected(self) -> None:
        with self.assertRaises(DiscordAccessError):
            validate_message_access("1001", "2002", self._config())

    def test_unlisted_guild_channel_pair_is_rejected(self) -> None:
        with self.assertRaises(DiscordAccessError):
            validate_message_access("9999", "8888", self._config())

    def test_message_content_intent_is_required(self) -> None:
        with self.assertRaises(DiscordAccessError):
            validate_message_access(
                "1001",
                "2001",
                self._config(message_content_intent_enabled=False),
            )

    def test_invalid_runtime_id_is_rejected_as_access_error(self) -> None:
        with self.assertRaises(DiscordAccessError):
            validate_message_access("invalid", "2001", self._config())


class DiscordGatewayParsingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = DiscordCollectorConfig(
            allowed_guild_channels=frozenset({("1001", "2001")}),
            message_content_intent_enabled=True,
        )
        self.collected_at = datetime(
            2026,
            9,
            26,
            8,
            0,
            tzinfo=timezone.utc,
        )

    def _payload(self) -> dict[str, object]:
        return {
            "t": "MESSAGE_CREATE",
            "d": {
                "id": "3001",
                "guild_id": "1001",
                "channel_id": "2001",
                "author": {
                    "id": "4001",
                },
                "content": "Freelance tester opportunity",
                "timestamp": "2026-09-26T09:30:00+02:00",
                "edited_timestamp": None,
            },
        }

    def test_message_create_is_normalized(self) -> None:
        result = parse_gateway_message_create(
            self._payload(),
            self.config,
            collected_at=self.collected_at,
        )

        self.assertEqual(result.guild_id, "1001")
        self.assertEqual(result.channel_id, "2001")
        self.assertEqual(result.message_id, "3001")
        self.assertEqual(result.author_id, "4001")
        self.assertEqual(
            result.content_text,
            "Freelance tester opportunity",
        )
        self.assertEqual(
            result.published_at,
            datetime(2026, 9, 26, 7, 30, tzinfo=timezone.utc),
        )
        self.assertIsNone(result.edited_at)
        self.assertEqual(result.collected_at, self.collected_at)

    def test_edited_timestamp_is_normalized_to_utc(self) -> None:
        payload = self._payload()
        data = payload["d"]
        self.assertIsInstance(data, dict)
        data["edited_timestamp"] = "2026-09-26T10:00:00+02:00"

        result = parse_gateway_message_create(
            payload,
            self.config,
            collected_at=self.collected_at,
        )

        self.assertEqual(
            result.edited_at,
            datetime(2026, 9, 26, 8, 0, tzinfo=timezone.utc),
        )

    def test_non_message_create_event_is_rejected(self) -> None:
        payload = self._payload()
        payload["t"] = "READY"

        with self.assertRaises(DiscordPayloadError):
            parse_gateway_message_create(
                payload,
                self.config,
                collected_at=self.collected_at,
            )

    def test_missing_gateway_data_is_rejected(self) -> None:
        payload = {
            "t": "MESSAGE_CREATE",
            "d": None,
        }

        with self.assertRaises(DiscordPayloadError):
            parse_gateway_message_create(
                payload,
                self.config,
                collected_at=self.collected_at,
            )

    def test_disallowed_channel_is_rejected_before_normalization(self) -> None:
        payload = self._payload()
        data = payload["d"]
        self.assertIsInstance(data, dict)
        data["channel_id"] = "9999"

        with self.assertRaises(DiscordAccessError):
            parse_gateway_message_create(
                payload,
                self.config,
                collected_at=self.collected_at,
            )

    def test_missing_author_is_rejected(self) -> None:
        payload = self._payload()
        data = payload["d"]
        self.assertIsInstance(data, dict)
        data.pop("author")

        with self.assertRaises(DiscordPayloadError):
            parse_gateway_message_create(
                payload,
                self.config,
                collected_at=self.collected_at,
            )

    def test_invalid_timestamp_is_rejected(self) -> None:
        payload = self._payload()
        data = payload["d"]
        self.assertIsInstance(data, dict)
        data["timestamp"] = "not-a-timestamp"

        with self.assertRaises(DiscordPayloadError):
            parse_gateway_message_create(
                payload,
                self.config,
                collected_at=self.collected_at,
            )

    def test_timezone_is_required_for_timestamp(self) -> None:
        payload = self._payload()
        data = payload["d"]
        self.assertIsInstance(data, dict)
        data["timestamp"] = "2026-09-26T09:30:00"

        with self.assertRaises(DiscordPayloadError):
            parse_gateway_message_create(
                payload,
                self.config,
                collected_at=self.collected_at,
            )

    def test_timezone_is_required_for_collected_at(self) -> None:
        naive_collected_at = datetime(2026, 9, 26, 8, 0)

        with self.assertRaises(DiscordPayloadError):
            parse_gateway_message_create(
                self._payload(),
                self.config,
                collected_at=naive_collected_at,
            )


class DiscordDedupTests(unittest.TestCase):
    def _message(
        self,
        *,
        content_text: str = "Original message",
        edited_at: datetime | None = None,
    ) -> NormalizedDiscordMessage:
        return NormalizedDiscordMessage(
            guild_id="1001",
            channel_id="2001",
            message_id="3001",
            author_id="4001",
            content_text=content_text,
            published_at=datetime(
                2026,
                9,
                26,
                7,
                30,
                tzinfo=timezone.utc,
            ),
            edited_at=edited_at,
            collected_at=datetime(
                2026,
                9,
                26,
                8,
                0,
                tzinfo=timezone.utc,
            ),
        )

    def test_same_message_has_deterministic_dedup_key(self) -> None:
        message = self._message()

        self.assertEqual(
            build_dedup_key(message),
            build_dedup_key(message),
        )

    def test_content_edit_keeps_same_logical_dedup_identity(self) -> None:
        original = self._message()
        edited = self._message(
            content_text="Edited message",
            edited_at=datetime(
                2026,
                9,
                26,
                8,
                15,
                tzinfo=timezone.utc,
            ),
        )

        self.assertEqual(
            build_dedup_key(original),
            build_dedup_key(edited),
        )

    def test_different_message_id_changes_dedup_key(self) -> None:
        first = self._message()
        second = NormalizedDiscordMessage(
            guild_id=first.guild_id,
            channel_id=first.channel_id,
            message_id="3002",
            author_id=first.author_id,
            content_text=first.content_text,
            published_at=first.published_at,
            edited_at=first.edited_at,
            collected_at=first.collected_at,
        )

        self.assertNotEqual(
            build_dedup_key(first),
            build_dedup_key(second),
        )


if __name__ == "__main__":
    unittest.main()
