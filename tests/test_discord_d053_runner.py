from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

from websockets.asyncio.server import serve


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from opportunity_scanner.discord_collector import (  # noqa: E402
    DiscordBoundedGatewayTransport,
    DiscordConfigError,
)
from opportunity_scanner.discord_d053_runner import (  # noqa: E402
    DISCORD_D053_INTENTS,
    build_d053_identify_payload,
    load_d053_local_env,
    run_d053_gateway_verification,
)
from opportunity_scanner.discord_d053_verifier import (  # noqa: E402
    D053_CREATE_TEXT,
    D053_UPDATE_TEXT,
)


GUILD_ID = "111111111111111111"
CHANNEL_ID = "222222222222222222"
MESSAGE_ID = "333333333333333333"
AUTHOR_ID = "444444444444444444"
TOKEN = "synthetic-local-test-token"


class DiscordD053RunnerTests(
    unittest.IsolatedAsyncioTestCase
):
    def test_intents_are_exact_least_privilege_value(self) -> None:
        self.assertEqual(DISCORD_D053_INTENTS, 33280)
        self.assertEqual(DISCORD_D053_INTENTS & (1 << 0), 0)
        self.assertNotEqual(DISCORD_D053_INTENTS & (1 << 9), 0)
        self.assertNotEqual(DISCORD_D053_INTENTS & (1 << 15), 0)

    def test_identify_payload_contains_exact_intents(self) -> None:
        payload = build_d053_identify_payload(TOKEN)

        self.assertEqual(payload["op"], 2)
        self.assertEqual(payload["d"]["token"], TOKEN)
        self.assertEqual(payload["d"]["intents"], 33280)

    def test_local_env_loader_reads_required_values(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    (
                        f"DISCORD_BOT_TOKEN={TOKEN}",
                        f"DISCORD_TEST_GUILD_ID={GUILD_ID}",
                        f"DISCORD_TEST_CHANNEL_ID={CHANNEL_ID}",
                    )
                )
                + "\n",
                encoding="utf-8",
            )

            token, guild_id, channel_id = load_d053_local_env(
                env_path
            )

        self.assertEqual(token, TOKEN)
        self.assertEqual(guild_id, GUILD_ID)
        self.assertEqual(channel_id, CHANNEL_ID)

    def test_local_env_loader_rejects_duplicate_required_key(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            env_path = Path(temp_dir) / ".env"
            env_path.write_text(
                "\n".join(
                    (
                        f"DISCORD_BOT_TOKEN={TOKEN}",
                        "DISCORD_BOT_TOKEN=duplicate",
                        f"DISCORD_TEST_GUILD_ID={GUILD_ID}",
                        f"DISCORD_TEST_CHANNEL_ID={CHANNEL_ID}",
                    )
                )
                + "\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(
                DiscordConfigError,
                "Duplicate required D-053 environment key",
            ):
                load_d053_local_env(env_path)

    async def test_local_loopback_runner_completes_d053(
        self,
    ) -> None:
        output_lines: list[str] = []
        identify_payloads: list[dict[str, object]] = []

        async def handler(websocket) -> None:
            await websocket.send(
                json.dumps(
                    {
                        "op": 10,
                        "d": {
                            "heartbeat_interval": 1000,
                        },
                    }
                )
            )

            identify_payloads.append(
                json.loads(await websocket.recv())
            )

            for payload in (
                {
                    "op": 0,
                    "s": 1,
                    "t": "READY",
                    "d": {},
                },
                {
                    "op": 0,
                    "s": 2,
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
                },
                {
                    "op": 0,
                    "s": 3,
                    "t": "MESSAGE_UPDATE",
                    "d": {
                        "guild_id": GUILD_ID,
                        "channel_id": CHANNEL_ID,
                        "id": MESSAGE_ID,
                        "content": D053_UPDATE_TEXT,
                    },
                },
                {
                    "op": 0,
                    "s": 4,
                    "t": "MESSAGE_DELETE",
                    "d": {
                        "guild_id": GUILD_ID,
                        "channel_id": CHANNEL_ID,
                        "id": MESSAGE_ID,
                    },
                },
            ):
                await websocket.send(json.dumps(payload))

            await websocket.wait_closed()

        async with serve(
            handler,
            "127.0.0.1",
            0,
            ping_interval=None,
            compression=None,
        ) as server:
            sockets = server.sockets

            if not sockets:
                raise AssertionError(
                    "Local-loopback server has no listening socket"
                )

            port = sockets[0].getsockname()[1]
            uri = f"ws://127.0.0.1:{port}"

            result = await run_d053_gateway_verification(
                TOKEN,
                GUILD_ID,
                CHANNEL_ID,
                uri=uri,
                output=output_lines.append,
                transport=DiscordBoundedGatewayTransport(),
            )

        self.assertEqual(len(identify_payloads), 1)
        self.assertEqual(identify_payloads[0]["op"], 2)
        self.assertEqual(
            identify_payloads[0]["d"]["intents"],
            33280,
        )

        self.assertEqual(result.transport.connection_attempts, 1)
        self.assertEqual(result.transport.identify_count, 1)
        self.assertEqual(result.transport.session_start_count, 1)

        self.assertEqual(
            result.transport.lifecycle_events,
            (
                "MESSAGE_CREATE",
                "MESSAGE_UPDATE",
                "MESSAGE_DELETE",
            ),
        )

        self.assertEqual(
            result.verifier.create_filter_state,
            "PASS",
        )
        self.assertEqual(
            result.verifier.update_filter_state,
            "REJECT",
        )
        self.assertTrue(result.verifier.deleted)

        combined_output = "\n".join(output_lines)

        self.assertIn("D053_GATEWAY_READY=YES", combined_output)
        self.assertIn("D053_STATUS=PASS", combined_output)
        self.assertNotIn(TOKEN, combined_output)


if __name__ == "__main__":
    unittest.main()
