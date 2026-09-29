from __future__ import annotations

import sys
import unittest
from unittest.mock import MagicMock, patch
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
    persist_gateway_message_create,
    persist_gateway_message_delete,
    persist_gateway_message_delete_bulk,
    persist_gateway_message_update,
    process_gateway_message_create,
    process_gateway_message_update,
    process_pending_discord_source_item,
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


class _TestDatabaseConfig:
    dbname: str = "test_db"
    user: str = "test_user"
    password: str = "test_password"
    host: str = "127.0.0.1"
    port: int = 5432



class DiscordCreatePersistenceAndFilterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = DiscordCollectorConfig(
            allowed_guild_channels=frozenset({("1001", "2001")}),
            message_content_intent_enabled=True,
        )
        self.database = _TestDatabaseConfig()
        self.collected_at = datetime(
            2026,
            9,
            26,
            10,
            0,
            tzinfo=timezone.utc,
        )

    def _payload(
        self,
        *,
        content: str = "Freelance tester opportunity",
    ) -> dict[str, object]:
        return {
            "t": "MESSAGE_CREATE",
            "d": {
                "id": "3001",
                "guild_id": "1001",
                "channel_id": "2001",
                "author": {
                    "id": "4001",
                },
                "content": content,
                "timestamp": "2026-09-26T09:30:00+02:00",
                "edited_timestamp": None,
            },
        }

    def _mock_connection(
        self,
        *,
        fetchone_side_effect: list[tuple[object, ...] | None],
    ) -> tuple[MagicMock, MagicMock]:
        cursor = MagicMock()
        cursor.fetchone.side_effect = fetchone_side_effect

        cursor_context = MagicMock()
        cursor_context.__enter__.return_value = cursor

        connection = MagicMock()
        connection.cursor.return_value = cursor_context

        connection_context = MagicMock()
        connection_context.__enter__.return_value = connection

        return connection_context, cursor

    def test_message_create_inserts_pending_row(self) -> None:
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[
                None,
                (101,),
            ],
        )

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_create(
                self._payload(),
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(result, (101, True))
        self.assertEqual(cursor.execute.call_count, 2)

        insert_sql = cursor.execute.call_args_list[1].args[0]
        insert_params = cursor.execute.call_args_list[1].args[1]

        self.assertIn(
            "INSERT INTO discord_source_items",
            insert_sql,
        )
        self.assertEqual(insert_params[-1], "PENDING")

    def test_identical_duplicate_create_is_idempotent(self) -> None:
        message = parse_gateway_message_create(
            self._payload(),
            self.config,
            collected_at=self.collected_at,
        )
        dedup_key = build_dedup_key(message)

        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[
                (
                    101,
                    message.content_text,
                    dedup_key,
                    "PASS",
                ),
            ],
        )

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_create(
                self._payload(),
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(result, (101, False))
        self.assertEqual(cursor.execute.call_count, 1)

    def test_conflicting_duplicate_create_fails_without_overwrite(
        self,
    ) -> None:
        message = parse_gateway_message_create(
            self._payload(),
            self.config,
            collected_at=self.collected_at,
        )
        dedup_key = build_dedup_key(message)

        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[
                (
                    101,
                    "Unexpected different content",
                    dedup_key,
                    "PASS",
                ),
            ],
        )

        with (
            patch(
                "opportunity_scanner.discord_collector.psycopg.connect",
                return_value=connection_context,
            ),
            self.assertRaises(DiscordPayloadError),
        ):
            persist_gateway_message_create(
                self._payload(),
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(cursor.execute.call_count, 1)

    def test_pending_item_uses_existing_module_6_filter_engine(
        self,
    ) -> None:
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[
                ("Freelance tester opportunity", "PENDING"),
            ],
        )

        with (
            patch(
                "opportunity_scanner.discord_collector.psycopg.connect",
                return_value=connection_context,
            ),
            patch(
                "opportunity_scanner.discord_collector.evaluate_filter",
                return_value="PASS",
            ) as filter_mock,
            patch(
                "opportunity_scanner.discord_collector.persist_discord_filter_result",
                return_value="PASS",
            ) as persist_mock,
        ):
            result = process_pending_discord_source_item(
                101,
                self.database,
            )

        self.assertEqual(result, "PASS")
        filter_mock.assert_called_once_with(
            None,
            "Freelance tester opportunity",
        )
        persist_mock.assert_called_once_with(
            101,
            "PASS",
            self.database,
        )
        self.assertEqual(cursor.execute.call_count, 1)

    def test_message_create_processes_pending_row_through_filter(
        self,
    ) -> None:
        with (
            patch(
                "opportunity_scanner.discord_collector.persist_gateway_message_create",
                return_value=(101, True),
            ) as create_mock,
            patch(
                "opportunity_scanner.discord_collector.process_pending_discord_source_item",
                return_value="PASS",
            ) as filter_mock,
        ):
            result = process_gateway_message_create(
                self._payload(),
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(result, (101, True, "PASS"))
        create_mock.assert_called_once()
        filter_mock.assert_called_once_with(
            101,
            self.database,
        )

    def test_message_update_processes_reset_pending_row_through_filter(
        self,
    ) -> None:
        update_payload: dict[str, object] = {
            "t": "MESSAGE_UPDATE",
            "d": {
                "id": "3001",
                "guild_id": "1001",
                "channel_id": "2001",
                "content": "Edited freelance tester opportunity",
            },
        }

        with (
            patch(
                "opportunity_scanner.discord_collector.persist_gateway_message_update",
                return_value=(101, False),
            ) as update_mock,
            patch(
                "opportunity_scanner.discord_collector.process_pending_discord_source_item",
                return_value="PASS",
            ) as filter_mock,
        ):
            result = process_gateway_message_update(
                update_payload,
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(result, (101, False, "PASS"))
        update_mock.assert_called_once()
        filter_mock.assert_called_once_with(
            101,
            self.database,
        )


class DiscordLifecyclePersistenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = DiscordCollectorConfig(
            allowed_guild_channels=frozenset(
                {
                    ("1001", "2001"),
                    ("1002", "2001"),
                }
            ),
            message_content_intent_enabled=True,
        )
        self.database = _TestDatabaseConfig()
        self.collected_at = datetime(
            2026,
            9,
            26,
            10,
            0,
            tzinfo=timezone.utc,
        )

    def _mock_connection(
        self,
        *,
        fetchone_side_effect: list[tuple[object, ...] | None] | None = None,
        fetchall_side_effect: list[list[tuple[object, ...]]] | None = None,
    ) -> tuple[MagicMock, MagicMock]:
        cursor = MagicMock()

        if fetchone_side_effect is not None:
            cursor.fetchone.side_effect = fetchone_side_effect

        if fetchall_side_effect is not None:
            cursor.fetchall.side_effect = fetchall_side_effect

        cursor_context = MagicMock()
        cursor_context.__enter__.return_value = cursor

        connection = MagicMock()
        connection.cursor.return_value = cursor_context

        connection_context = MagicMock()
        connection_context.__enter__.return_value = connection

        return connection_context, cursor

    def test_existing_message_update_updates_in_place_and_resets_filter(self) -> None:
        published_at = datetime(
            2026,
            9,
            26,
            7,
            30,
            tzinfo=timezone.utc,
        )
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[
                (
                    101,
                    "1001",
                    "4001",
                    "Original message",
                    published_at,
                    None,
                ),
                (101,),
            ]
        )
        payload = {
            "t": "MESSAGE_UPDATE",
            "d": {
                "id": "3001",
                "guild_id": "1001",
                "channel_id": "2001",
                "content": "Edited message",
                "edited_timestamp": "2026-09-26T12:15:00+02:00",
            },
        }

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_update(
                payload,
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(result, (101, False))
        self.assertEqual(cursor.execute.call_count, 2)

        update_sql = cursor.execute.call_args_list[1].args[0]
        update_params = cursor.execute.call_args_list[1].args[1]

        self.assertIn("UPDATE discord_source_items", update_sql)
        self.assertIn("filter_state = 'PENDING'", update_sql)
        self.assertEqual(update_params[0], "4001")
        self.assertEqual(update_params[1], "Edited message")
        self.assertEqual(update_params[2], published_at)
        self.assertEqual(
            update_params[3],
            datetime(2026, 9, 26, 10, 15, tzinfo=timezone.utc),
        )
        self.assertEqual(update_params[4], self.collected_at)
        self.assertEqual(update_params[5], 101)

    def test_complete_unknown_message_update_can_create_row(self) -> None:
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[None, (102,)]
        )
        payload = {
            "t": "MESSAGE_UPDATE",
            "d": {
                "id": "3002",
                "guild_id": "1001",
                "channel_id": "2001",
                "author": {"id": "4002"},
                "content": "Complete unknown update",
                "timestamp": "2026-09-26T09:30:00+02:00",
                "edited_timestamp": "2026-09-26T10:00:00+02:00",
            },
        }

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_update(
                payload,
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(result, (102, True))
        self.assertEqual(cursor.execute.call_count, 2)
        self.assertIn(
            "INSERT INTO discord_source_items",
            cursor.execute.call_args_list[1].args[0],
        )

    def test_incomplete_unknown_message_update_fails_without_insert(self) -> None:
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[None]
        )
        payload = {
            "t": "MESSAGE_UPDATE",
            "d": {
                "id": "3003",
                "guild_id": "1001",
                "channel_id": "2001",
                "content": "Missing author and timestamp",
            },
        }

        with (
            patch(
                "opportunity_scanner.discord_collector.psycopg.connect",
                return_value=connection_context,
            ),
            self.assertRaises(DiscordPayloadError),
        ):
            persist_gateway_message_update(
                payload,
                self.config,
                self.database,
                collected_at=self.collected_at,
            )

        self.assertEqual(cursor.execute.call_count, 1)
        self.assertIn(
            "SELECT id",
            cursor.execute.call_args_list[0].args[0],
        )

    def test_message_delete_hard_deletes_using_stored_identity(self) -> None:
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[
                (201, "1001"),
                (201,),
            ]
        )
        payload = {
            "t": "MESSAGE_DELETE",
            "d": {
                "id": "3001",
                "channel_id": "2001",
            },
        }

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_delete(
                payload,
                self.config,
                self.database,
            )

        self.assertTrue(result)
        self.assertEqual(cursor.execute.call_count, 2)
        self.assertEqual(
            cursor.execute.call_args_list[0].args[1],
            ("2001", "3001"),
        )
        self.assertIn(
            "DELETE FROM discord_source_items",
            cursor.execute.call_args_list[1].args[0],
        )

    def test_absent_message_delete_is_idempotent_noop(self) -> None:
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[None]
        )
        payload = {
            "t": "MESSAGE_DELETE",
            "d": {
                "id": "3999",
                "channel_id": "2001",
            },
        }

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_delete(
                payload,
                self.config,
                self.database,
            )

        self.assertFalse(result)
        self.assertEqual(cursor.execute.call_count, 1)

    def test_message_delete_validates_present_guild_id_against_stored_row(
        self,
    ) -> None:
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[(202, "1001")]
        )
        payload = {
            "t": "MESSAGE_DELETE",
            "d": {
                "id": "3004",
                "channel_id": "2001",
                "guild_id": "1002",
            },
        }

        with (
            patch(
                "opportunity_scanner.discord_collector.psycopg.connect",
                return_value=connection_context,
            ),
            self.assertRaises(DiscordPayloadError),
        ):
            persist_gateway_message_delete(
                payload,
                self.config,
                self.database,
            )

        self.assertEqual(cursor.execute.call_count, 1)

    def test_delete_does_not_require_message_content_intent(self) -> None:
        config = DiscordCollectorConfig(
            allowed_guild_channels=frozenset({("1001", "2001")}),
            message_content_intent_enabled=False,
        )
        connection_context, cursor = self._mock_connection(
            fetchone_side_effect=[
                (203, "1001"),
                (203,),
            ]
        )
        payload = {
            "t": "MESSAGE_DELETE",
            "d": {
                "id": "3005",
                "channel_id": "2001",
            },
        }

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_delete(
                payload,
                config,
                self.database,
            )

        self.assertTrue(result)
        self.assertEqual(cursor.execute.call_count, 2)

    def test_bulk_delete_hard_deletes_only_existing_rows(self) -> None:
        connection_context, cursor = self._mock_connection(
            fetchall_side_effect=[
                [
                    ("3001", "1001"),
                    ("3002", "1001"),
                ],
                [
                    (301,),
                    (302,),
                ],
            ]
        )
        payload = {
            "t": "MESSAGE_DELETE_BULK",
            "d": {
                "ids": ["3001", "3002", "3999"],
                "channel_id": "2001",
            },
        }

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_delete_bulk(
                payload,
                self.config,
                self.database,
            )

        self.assertEqual(result, 2)
        self.assertEqual(cursor.execute.call_count, 2)
        self.assertIn(
            "DELETE FROM discord_source_items",
            cursor.execute.call_args_list[1].args[0],
        )

    def test_absent_bulk_delete_is_idempotent_noop(self) -> None:
        connection_context, cursor = self._mock_connection(
            fetchall_side_effect=[[]]
        )
        payload = {
            "t": "MESSAGE_DELETE_BULK",
            "d": {
                "ids": ["3998", "3999"],
                "channel_id": "2001",
            },
        }

        with patch(
            "opportunity_scanner.discord_collector.psycopg.connect",
            return_value=connection_context,
        ):
            result = persist_gateway_message_delete_bulk(
                payload,
                self.config,
                self.database,
            )

        self.assertEqual(result, 0)
        self.assertEqual(cursor.execute.call_count, 1)


if __name__ == "__main__":
    unittest.main()
