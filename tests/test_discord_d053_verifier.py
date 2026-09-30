import unittest

from opportunity_scanner.discord_collector import (
    DiscordCollectorConfig,
    DiscordGatewayStopFail,
)
from opportunity_scanner.discord_d053_verifier import (
    D053_CREATE_TEXT,
    D053_LIFECYCLE_SEQUENCE,
    D053_UPDATE_TEXT,
    DiscordD053InMemoryVerifier,
)


GUILD_ID = "111111111111111111"
CHANNEL_ID = "222222222222222222"
MESSAGE_ID = "333333333333333333"
AUTHOR_ID = "444444444444444444"


def _config() -> DiscordCollectorConfig:
    return DiscordCollectorConfig(
        allowed_guild_channels=frozenset(
            {(GUILD_ID, CHANNEL_ID)}
        ),
        message_content_intent_enabled=True,
        administrator_permission_requested=False,
    )


def _create_payload() -> dict:
    return {
        "op": 0,
        "t": "MESSAGE_CREATE",
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "id": MESSAGE_ID,
            "author": {
                "id": AUTHOR_ID,
            },
            "content": D053_CREATE_TEXT,
            "timestamp": "2026-09-30T19:00:00+00:00",
            "edited_timestamp": None,
        },
    }


def _update_payload(
    message_id: str = MESSAGE_ID,
) -> dict:
    return {
        "op": 0,
        "t": "MESSAGE_UPDATE",
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "id": message_id,
            "content": D053_UPDATE_TEXT,
        },
    }


def _delete_payload(
    message_id: str = MESSAGE_ID,
) -> dict:
    return {
        "op": 0,
        "t": "MESSAGE_DELETE",
        "d": {
            "guild_id": GUILD_ID,
            "channel_id": CHANNEL_ID,
            "id": message_id,
        },
    }


class DiscordD053InMemoryVerifierTests(unittest.TestCase):
    def test_d053_in_memory_lifecycle_passes(self) -> None:
        verifier = DiscordD053InMemoryVerifier(_config())

        verifier.handle(_create_payload())
        verifier.handle(_update_payload())
        verifier.handle(_delete_payload())

        result = verifier.result()

        self.assertEqual(result.message_id, MESSAGE_ID)
        self.assertEqual(result.create_filter_state, "PASS")
        self.assertEqual(result.update_filter_state, "REJECT")
        self.assertEqual(
            result.lifecycle_events,
            D053_LIFECYCLE_SEQUENCE,
        )
        self.assertTrue(result.deleted)
        self.assertEqual(len(result.dedup_key), 64)

    def test_d053_rejects_update_with_changed_message_identity(
        self,
    ) -> None:
        verifier = DiscordD053InMemoryVerifier(_config())
        verifier.handle(_create_payload())

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "stable message identity",
        ):
            verifier.handle(
                _update_payload("555555555555555555")
            )

    def test_d053_rejects_delete_with_changed_message_identity(
        self,
    ) -> None:
        verifier = DiscordD053InMemoryVerifier(_config())

        verifier.handle(_create_payload())
        verifier.handle(_update_payload())

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "stable message identity",
        ):
            verifier.handle(
                _delete_payload("555555555555555555")
            )

    def test_d053_rejects_invalid_lifecycle_order(self) -> None:
        verifier = DiscordD053InMemoryVerifier(_config())

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "event order",
        ):
            verifier.handle(_update_payload())

    def test_d053_result_rejects_incomplete_lifecycle(self) -> None:
        verifier = DiscordD053InMemoryVerifier(_config())
        verifier.handle(_create_payload())

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "lifecycle is incomplete",
        ):
            verifier.result()


if __name__ == "__main__":
    unittest.main()
