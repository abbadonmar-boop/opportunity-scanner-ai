from __future__ import annotations

import asyncio
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any

from .discord_collector import (
    DiscordBoundedGatewayResult,
    DiscordBoundedGatewayTransport,
    DiscordCollectorConfig,
    DiscordCollectorError,
    DiscordConfigError,
    DiscordGatewayStopFail,
    validate_collector_config,
)
from .discord_d053_verifier import (
    D053_CREATE_TEXT,
    D053_UPDATE_TEXT,
    DiscordD053InMemoryResult,
    DiscordD053InMemoryVerifier,
)


DISCORD_D053_GATEWAY_URI = (
    "wss://gateway.discord.gg/?v=10&encoding=json"
)

DISCORD_D053_GUILD_MESSAGES_INTENT = 1 << 9
DISCORD_D053_MESSAGE_CONTENT_INTENT = 1 << 15
DISCORD_D053_INTENTS = (
    DISCORD_D053_GUILD_MESSAGES_INTENT
    | DISCORD_D053_MESSAGE_CONTENT_INTENT
)

_D053_REQUIRED_ENV_KEYS = (
    "DISCORD_BOT_TOKEN",
    "DISCORD_TEST_GUILD_ID",
    "DISCORD_TEST_CHANNEL_ID",
)


@dataclass(frozen=True)
class DiscordD053RunnerResult:
    transport: DiscordBoundedGatewayResult
    verifier: DiscordD053InMemoryResult


def _default_env_path() -> Path:
    return Path(__file__).resolve().parents[2] / ".env"


def load_d053_local_env(
    path: Path | None = None,
) -> tuple[str, str, str]:
    env_path = path if path is not None else _default_env_path()

    if not env_path.is_file():
        raise DiscordConfigError(
            "Local .env file required for D-053 was not found"
        )

    values: dict[str, str] = {}

    for raw_line in env_path.read_text(
        encoding="utf-8",
    ).splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        if "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()

        if key not in _D053_REQUIRED_ENV_KEYS:
            continue

        if key in values:
            raise DiscordConfigError(
                f"Duplicate required D-053 environment key: {key}"
            )

        value = value.strip()

        if (
            len(value) >= 2
            and value[0] == value[-1]
            and value[0] in {"'", '"'}
        ):
            value = value[1:-1]

        if not value:
            raise DiscordConfigError(
                f"Required D-053 environment key is empty: {key}"
            )

        values[key] = value

    missing = [
        key
        for key in _D053_REQUIRED_ENV_KEYS
        if key not in values
    ]

    if missing:
        raise DiscordConfigError(
            "Missing required D-053 environment key(s): "
            + ", ".join(missing)
        )

    return (
        values["DISCORD_BOT_TOKEN"],
        values["DISCORD_TEST_GUILD_ID"],
        values["DISCORD_TEST_CHANNEL_ID"],
    )


def build_d053_collector_config(
    guild_id: str,
    channel_id: str,
) -> DiscordCollectorConfig:
    config = DiscordCollectorConfig(
        allowed_guild_channels=frozenset(
            {
                (
                    guild_id,
                    channel_id,
                )
            }
        ),
        message_content_intent_enabled=True,
        administrator_permission_requested=False,
    )

    validate_collector_config(config)

    return config


def build_d053_identify_payload(
    token: str,
) -> dict[str, Any]:
    normalized_token = token.strip()

    if not normalized_token:
        raise DiscordConfigError(
            "DISCORD_BOT_TOKEN must be non-empty"
        )

    return {
        "op": 2,
        "d": {
            "token": normalized_token,
            "intents": DISCORD_D053_INTENTS,
            "properties": {
                "os": "windows",
                "browser": "opportunity-scanner-ai-d053",
                "device": "opportunity-scanner-ai-d053",
            },
        },
    }


async def run_d053_gateway_verification(
    token: str,
    guild_id: str,
    channel_id: str,
    *,
    uri: str = DISCORD_D053_GATEWAY_URI,
    output: Callable[[str], None] = print,
    transport: DiscordBoundedGatewayTransport | None = None,
) -> DiscordD053RunnerResult:
    config = build_d053_collector_config(
        guild_id,
        channel_id,
    )
    identify_payload = build_d053_identify_payload(token)

    verifier = DiscordD053InMemoryVerifier(config)
    gateway_transport = (
        transport
        if transport is not None
        else DiscordBoundedGatewayTransport()
    )

    def ready_handler() -> None:
        output("D053_GATEWAY_READY=YES")
        output("NEXT_ACTION=CREATE_SYNTHETIC_MESSAGE")
        output(f"CREATE_TEXT={D053_CREATE_TEXT}")

    def lifecycle_handler(
        payload: Mapping[str, Any],
    ) -> None:
        verifier.handle(payload)

        event_type = payload.get("t")
        output(f"D053_EVENT={event_type} VERIFIED")

        if event_type == "MESSAGE_CREATE":
            output("NEXT_ACTION=EDIT_THE_SAME_MESSAGE")
            output(f"UPDATE_TEXT={D053_UPDATE_TEXT}")
        elif event_type == "MESSAGE_UPDATE":
            output("NEXT_ACTION=DELETE_THE_SAME_MESSAGE")

    transport_result = await gateway_transport.run(
        uri,
        identify_payload,
        lifecycle_handler=lifecycle_handler,
        ready_handler=ready_handler,
    )

    verifier_result = verifier.result()

    if (
        transport_result.lifecycle_events
        != verifier_result.lifecycle_events
    ):
        raise DiscordGatewayStopFail(
            "Transport/verifier lifecycle results do not match"
        )

    output("D053_STATUS=PASS")
    output(
        "CONNECTION_ATTEMPTS="
        f"{transport_result.connection_attempts}"
    )
    output(
        "IDENTIFY_COUNT="
        f"{transport_result.identify_count}"
    )
    output(
        "SESSION_STARTS="
        f"{transport_result.session_start_count}"
    )
    output(
        "CREATE_FILTER="
        f"{verifier_result.create_filter_state}"
    )
    output(
        "UPDATE_FILTER="
        f"{verifier_result.update_filter_state}"
    )
    output(
        "DELETED="
        f"{'YES' if verifier_result.deleted else 'NO'}"
    )

    return DiscordD053RunnerResult(
        transport=transport_result,
        verifier=verifier_result,
    )


async def run_live_d053() -> int:
    token, guild_id, channel_id = load_d053_local_env()

    await run_d053_gateway_verification(
        token,
        guild_id,
        channel_id,
    )

    return 0


def main() -> int:
    try:
        return asyncio.run(run_live_d053())
    except DiscordCollectorError as exc:
        print(f"D053_STATUS=FAIL: {exc}")
        return 1
    except KeyboardInterrupt:
        print("D053_STATUS=STOPPED")
        return 1
    except Exception:
        print("D053_STATUS=FAIL UNEXPECTED")
        return 1


if __name__ == "__main__":
    sys.exit(main())
