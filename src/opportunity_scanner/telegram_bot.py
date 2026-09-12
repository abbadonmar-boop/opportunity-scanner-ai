from __future__ import annotations

import json
import sys
from pathlib import Path
from urllib import parse, request
from urllib.error import HTTPError, URLError


TELEGRAM_API_ROOT = "https://api.telegram.org"


class ConfigError(RuntimeError):
    pass


class TelegramApiError(RuntimeError):
    pass


def load_config() -> tuple[str, int, int]:
    env_path = Path(__file__).resolve().parents[2] / ".env"

    if not env_path.is_file():
        raise ConfigError(".env file is missing")

    values: dict[str, str] = {}

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        key, separator, value = line.partition("=")

        if separator:
            values[key.strip()] = value.strip()

    token = values.get("TELEGRAM_BOT_TOKEN", "")
    owner_id_text = values.get("TELEGRAM_OWNER_ID", "")
    target_chat_id_text = values.get("TELEGRAM_TARGET_CHAT_ID", "")

    if not token:
        raise ConfigError("TELEGRAM_BOT_TOKEN is missing")

    try:
        owner_id = int(owner_id_text)
    except ValueError as exc:
        raise ConfigError("TELEGRAM_OWNER_ID is invalid") from exc

    try:
        target_chat_id = int(target_chat_id_text)
    except ValueError as exc:
        raise ConfigError("TELEGRAM_TARGET_CHAT_ID is invalid") from exc

    return token, owner_id, target_chat_id


def telegram_api_call(
    token: str,
    method: str,
    payload: dict[str, object] | None = None,
) -> object:
    url = f"{TELEGRAM_API_ROOT}/bot{token}/{method}"
    body = parse.urlencode(payload or {}).encode("utf-8")

    api_request = request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    try:
        with request.urlopen(api_request, timeout=40) as response:
            response_text = response.read().decode("utf-8")
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise TelegramApiError(f"{method} request failed") from exc

    try:
        response_data = json.loads(response_text)
    except json.JSONDecodeError as exc:
        raise TelegramApiError(f"{method} returned invalid JSON") from exc

    if not isinstance(response_data, dict) or response_data.get("ok") is not True:
        raise TelegramApiError(f"{method} returned ok=false")

    return response_data.get("result")


def verify_no_webhook(token: str) -> bool:
    result = telegram_api_call(token, "getWebhookInfo")

    if not isinstance(result, dict):
        raise TelegramApiError("getWebhookInfo returned invalid result")

    webhook_url = str(result.get("url") or "")

    return webhook_url == ""


def send_message(
    token: str,
    chat_id: int,
    text: str,
    reply_markup: dict[str, object] | None = None,
) -> None:
    payload: dict[str, object] = {
        "chat_id": chat_id,
        "text": text,
    }

    if reply_markup is not None:
        payload["reply_markup"] = json.dumps(
            reply_markup,
            ensure_ascii=False,
        )

    telegram_api_call(token, "sendMessage", payload)


def format_test_opportunity() -> tuple[str, dict[str, object]]:
    source_url = "https://example.com/"

    text = (
        "Тестовая возможность\n\n"
        "Название: Example Opportunity\n"
        "Источник: Тестовый источник\n"
        "Категория: AI / Data\n"
        "Оплата: $25\n"
        "KYC: NO\n"
        "Депозит: NO\n"
        "География: Весь мир\n"
        "Дедлайн: 31.12.2026\n"
        "Риск: Низкий\n"
        "Итог: Подходит для проверки Telegram-интерфейса.\n"
        f"Ссылка: {source_url}"
    )

    reply_markup: dict[str, object] = {
        "inline_keyboard": [
            [
                {
                    "text": "Открыть",
                    "url": source_url,
                }
            ]
        ]
    }

    return text, reply_markup


def send_test_opportunity(token: str, target_chat_id: int) -> None:
    text, reply_markup = format_test_opportunity()

    send_message(
        token,
        target_chat_id,
        text,
        reply_markup=reply_markup,
    )


def format_rss_candidate(
    title: str | None,
    source_name: str | None,
    link: str | None,
) -> tuple[str, dict[str, object] | None]:
    lines = ['Предварительная RSS-возможность']

    clean_title = (title or '').strip()
    clean_source_name = (source_name or '').strip()
    clean_link = (link or '').strip()

    if clean_title:
        lines.extend(('', f'Название: {clean_title}'))

    if clean_source_name:
        lines.append(f'Источник: {clean_source_name}')

    if clean_link:
        lines.append(f'Ссылка: {clean_link}')

    reply_markup: dict[str, object] | None = None

    if clean_link:
        reply_markup = {
            'inline_keyboard': [
                [
                    {
                        'text': 'Открыть',
                        'url': clean_link,
                    }
                ]
            ]
        }

    return '\n'.join(lines), reply_markup


def send_rss_candidate(
    token: str,
    target_chat_id: int,
    title: str | None,
    source_name: str | None,
    link: str | None,
) -> None:
    text, reply_markup = format_rss_candidate(
        title,
        source_name,
        link,
    )

    send_message(
        token,
        target_chat_id,
        text,
        reply_markup=reply_markup,
    )


def handle_update(
    token: str,
    owner_id: int,
    target_chat_id: int,
    update: object,
) -> None:
    if not isinstance(update, dict):
        return

    message = update.get("message")

    if not isinstance(message, dict):
        return

    sender = message.get("from")
    chat = message.get("chat")

    if not isinstance(sender, dict) or not isinstance(chat, dict):
        return

    if sender.get("id") != owner_id:
        print("UNAUTHORIZED_UPDATE_IGNORED")
        return

    text = str(message.get("text") or "").strip()

    if not text:
        return

    command = text.split(maxsplit=1)[0].split("@", 1)[0]

    if command == "/start":
        chat_id = chat.get("id")

        if not isinstance(chat_id, int):
            return

        send_message(
            token,
            chat_id,
            "Opportunity Scanner AI запущен. Доступ владельца подтверждён.",
        )

        print("OWNER_START_HANDLED")
        return

    if command == "/test":
        send_test_opportunity(token, target_chat_id)
        print("TEST_OPPORTUNITY_SENT")


def run_bot() -> int:
    token, owner_id, target_chat_id = load_config()

    if not verify_no_webhook(token):
        print("BOT_STATUS=BLOCKED_EXISTING_WEBHOOK")
        return 2

    print("WEBHOOK_CHECK=PASS EMPTY")
    print("TELEGRAM_CONFIG=READY")
    print("BOT_STATUS=RUNNING")

    offset: int | None = None

    while True:
        payload: dict[str, object] = {
            "timeout": 30,
            "allowed_updates": json.dumps(["message"]),
        }

        if offset is not None:
            payload["offset"] = offset

        updates = telegram_api_call(token, "getUpdates", payload)

        if not isinstance(updates, list):
            raise TelegramApiError("getUpdates returned invalid result")

        for update in updates:
            if isinstance(update, dict):
                update_id = update.get("update_id")

                if isinstance(update_id, int):
                    next_offset = update_id + 1

                    if offset is None or next_offset > offset:
                        offset = next_offset

            handle_update(
                token,
                owner_id,
                target_chat_id,
                update,
            )


def main() -> int:
    try:
        return run_bot()
    except ConfigError as exc:
        print(f"BOT_STATUS=FAIL CONFIG: {exc}")
        return 1
    except TelegramApiError as exc:
        print(f"BOT_STATUS=FAIL API: {exc}")
        return 1
    except KeyboardInterrupt:
        print("BOT_STATUS=STOPPED")
        return 0
    except Exception:
        print("BOT_STATUS=FAIL UNEXPECTED")
        return 1


if __name__ == "__main__":
    sys.exit(main())