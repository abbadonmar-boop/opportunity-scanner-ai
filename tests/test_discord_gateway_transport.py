from __future__ import annotations

import asyncio
import json
import sys
import unittest
from pathlib import Path

import websockets
from websockets.asyncio.server import serve


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from opportunity_scanner.discord_collector import (  # noqa: E402
    DiscordBoundedGatewayTransport,
    DiscordGatewayStopFail,
)


class _RecordingWebSocket:
    def __init__(self) -> None:
        self.sent: list[str] = []

    async def send(self, payload: str) -> None:
        self.sent.append(payload)


class DiscordBoundedGatewayTransportTests(
    unittest.IsolatedAsyncioTestCase
):
    @staticmethod
    def _identify_payload() -> dict[str, object]:
        return {
            "op": 2,
            "d": {
                "synthetic_local_loopback": True,
            },
        }

    @staticmethod
    async def _run_loopback(
        handler,
        transport: DiscordBoundedGatewayTransport,
    ):
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

            return await transport.run(
                uri,
                DiscordBoundedGatewayTransportTests._identify_payload(),
            )

    def test_websockets_version_is_exactly_17_1(self) -> None:
        self.assertEqual(websockets.__version__, "17.1")

    async def test_successful_single_connection_sequence_and_close(
        self,
    ) -> None:
        connection_count = 0
        received_payloads: list[dict[str, object]] = []
        client_closed = asyncio.Event()

        async def handler(websocket) -> None:
            nonlocal connection_count
            connection_count += 1

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

            received_payloads.append(
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
                    "d": {},
                },
                {
                    "op": 0,
                    "s": 3,
                    "t": "MESSAGE_UPDATE",
                    "d": {},
                },
                {
                    "op": 0,
                    "s": 4,
                    "t": "MESSAGE_DELETE",
                    "d": {},
                },
            ):
                await websocket.send(json.dumps(payload))

            await websocket.wait_closed()
            client_closed.set()

        transport = DiscordBoundedGatewayTransport()

        result = await self._run_loopback(
            handler,
            transport,
        )

        await asyncio.wait_for(
            client_closed.wait(),
            timeout=1.0,
        )

        self.assertEqual(connection_count, 1)
        self.assertEqual(len(received_payloads), 1)
        self.assertEqual(received_payloads[0]["op"], 2)

        self.assertEqual(result.connection_attempts, 1)
        self.assertEqual(result.identify_count, 1)
        self.assertEqual(result.session_start_count, 1)
        self.assertEqual(
            result.lifecycle_events,
            (
                "MESSAGE_CREATE",
                "MESSAGE_UPDATE",
                "MESSAGE_DELETE",
            ),
        )

    async def test_opcode_1_heartbeat_request_is_serviced(
        self,
    ) -> None:
        received_heartbeat: list[dict[str, object]] = []

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

            identify = json.loads(await websocket.recv())
            self.assertEqual(identify["op"], 2)

            await websocket.send(
                json.dumps(
                    {
                        "op": 0,
                        "s": 1,
                        "t": "READY",
                        "d": {},
                    }
                )
            )

            await websocket.send(
                json.dumps(
                    {
                        "op": 1,
                        "d": None,
                    }
                )
            )

            received_heartbeat.append(
                json.loads(await websocket.recv())
            )

            await websocket.send(
                json.dumps(
                    {
                        "op": 11,
                        "d": None,
                    }
                )
            )

            for sequence, event_type in (
                (2, "MESSAGE_CREATE"),
                (3, "MESSAGE_UPDATE"),
                (4, "MESSAGE_DELETE"),
            ):
                await websocket.send(
                    json.dumps(
                        {
                            "op": 0,
                            "s": sequence,
                            "t": event_type,
                            "d": {},
                        }
                    )
                )

            await websocket.wait_closed()

        transport = DiscordBoundedGatewayTransport()

        result = await self._run_loopback(
            handler,
            transport,
        )

        self.assertEqual(len(received_heartbeat), 1)
        self.assertEqual(
            received_heartbeat[0],
            {
                "op": 1,
                "d": 1,
            },
        )
        self.assertEqual(
            result.lifecycle_events,
            (
                "MESSAGE_CREATE",
                "MESSAGE_UPDATE",
                "MESSAGE_DELETE",
            ),
        )

    async def test_missing_heartbeat_ack_is_stop_fail(
        self,
    ) -> None:
        connection_count = 0
        heartbeat_received = asyncio.Event()

        async def handler(websocket) -> None:
            nonlocal connection_count
            connection_count += 1

            await websocket.send(
                json.dumps(
                    {
                        "op": 10,
                        "d": {
                            "heartbeat_interval": 25,
                        },
                    }
                )
            )

            identify = json.loads(await websocket.recv())
            self.assertEqual(identify["op"], 2)

            await websocket.send(
                json.dumps(
                    {
                        "op": 0,
                        "s": 1,
                        "t": "READY",
                        "d": {},
                    }
                )
            )

            heartbeat = json.loads(await websocket.recv())
            self.assertEqual(heartbeat["op"], 1)
            heartbeat_received.set()

            await websocket.wait_closed()

        transport = DiscordBoundedGatewayTransport()

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "Heartbeat ACK",
        ):
            await asyncio.wait_for(
                self._run_loopback(
                    handler,
                    transport,
                ),
                timeout=1.0,
            )

        self.assertTrue(heartbeat_received.is_set())
        self.assertEqual(connection_count, 1)
        self.assertEqual(transport.connection_attempts, 1)
        self.assertEqual(transport.identify_count, 1)

    async def test_opcode_7_is_stop_fail_without_reconnect(
        self,
    ) -> None:
        connection_count = 0

        async def handler(websocket) -> None:
            nonlocal connection_count
            connection_count += 1

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

            await websocket.recv()

            await websocket.send(
                json.dumps(
                    {
                        "op": 0,
                        "s": 1,
                        "t": "READY",
                        "d": {},
                    }
                )
            )

            await websocket.send(
                json.dumps(
                    {
                        "op": 7,
                        "d": None,
                    }
                )
            )

            await websocket.wait_closed()

        transport = DiscordBoundedGatewayTransport()

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "Reconnect opcode 7",
        ):
            await self._run_loopback(
                handler,
                transport,
            )

        self.assertEqual(connection_count, 1)
        self.assertEqual(transport.connection_attempts, 1)
        self.assertEqual(transport.identify_count, 1)
        self.assertEqual(transport.session_start_count, 1)

    async def test_opcode_9_is_stop_fail_without_reconnect(
        self,
    ) -> None:
        connection_count = 0

        async def handler(websocket) -> None:
            nonlocal connection_count
            connection_count += 1

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

            await websocket.recv()

            await websocket.send(
                json.dumps(
                    {
                        "op": 0,
                        "s": 1,
                        "t": "READY",
                        "d": {},
                    }
                )
            )

            await websocket.send(
                json.dumps(
                    {
                        "op": 9,
                        "d": True,
                    }
                )
            )

            await websocket.wait_closed()

        transport = DiscordBoundedGatewayTransport()

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "Invalid Session opcode 9",
        ):
            await self._run_loopback(
                handler,
                transport,
            )

        self.assertEqual(connection_count, 1)
        self.assertEqual(transport.connection_attempts, 1)
        self.assertEqual(transport.identify_count, 1)
        self.assertEqual(transport.session_start_count, 1)

    async def test_unexpected_disconnect_is_stop_fail_without_reconnect(
        self,
    ) -> None:
        connection_count = 0

        async def handler(websocket) -> None:
            nonlocal connection_count
            connection_count += 1

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

            await websocket.recv()

            await websocket.send(
                json.dumps(
                    {
                        "op": 0,
                        "s": 1,
                        "t": "READY",
                        "d": {},
                    }
                )
            )

            await websocket.close(
                code=1000,
                reason="synthetic local disconnect",
            )

        transport = DiscordBoundedGatewayTransport()

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "connection closed",
        ):
            await self._run_loopback(
                handler,
                transport,
            )

        self.assertEqual(connection_count, 1)
        self.assertEqual(transport.connection_attempts, 1)
        self.assertEqual(transport.identify_count, 1)
        self.assertEqual(transport.session_start_count, 1)

    async def test_second_run_is_rejected_before_second_connection(
        self,
    ) -> None:
        connection_count = 0

        async def handler(websocket) -> None:
            nonlocal connection_count
            connection_count += 1

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

            await websocket.recv()

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
                    "d": {},
                },
                {
                    "op": 0,
                    "s": 3,
                    "t": "MESSAGE_UPDATE",
                    "d": {},
                },
                {
                    "op": 0,
                    "s": 4,
                    "t": "MESSAGE_DELETE",
                    "d": {},
                },
            ):
                await websocket.send(json.dumps(payload))

            await websocket.wait_closed()

        transport = DiscordBoundedGatewayTransport()

        await self._run_loopback(
            handler,
            transport,
        )

        self.assertEqual(connection_count, 1)

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "second Gateway connection attempt",
        ):
            await transport.run(
                "ws://127.0.0.1:1",
                self._identify_payload(),
            )

        self.assertEqual(connection_count, 1)
        self.assertEqual(transport.connection_attempts, 1)

    async def test_resume_and_repeated_identify_are_rejected(
        self,
    ) -> None:
        websocket = _RecordingWebSocket()
        transport = DiscordBoundedGatewayTransport()

        await transport._send_gateway_payload(
            websocket,
            self._identify_payload(),
        )

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "Repeated Gateway IDENTIFY",
        ):
            await transport._send_gateway_payload(
                websocket,
                self._identify_payload(),
            )

        with self.assertRaisesRegex(
            DiscordGatewayStopFail,
            "RESUME is prohibited",
        ):
            await transport._send_gateway_payload(
                websocket,
                {
                    "op": 6,
                    "d": {
                        "synthetic": True,
                    },
                },
            )

        self.assertEqual(len(websocket.sent), 1)
        self.assertEqual(
            json.loads(websocket.sent[0])["op"],
            2,
        )


if __name__ == "__main__":
    unittest.main()
