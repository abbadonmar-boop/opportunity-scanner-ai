from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path
from urllib import request
from urllib.error import HTTPError, URLError
from xml.etree import ElementTree

import psycopg

from .telegram_bot import send_rss_candidate


class RssConfigError(RuntimeError):
    pass


def load_rss_feed_urls() -> list[str]:
    env_path = Path(__file__).resolve().parents[2] / ".env"

    if not env_path.is_file():
        raise RssConfigError(".env file is missing")

    values: dict[str, str] = {}

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        if not line or line.startswith("#"):
            continue

        key, separator, value = line.partition("=")

        if separator:
            values[key.strip()] = value.strip()

    raw_urls = values.get("RSS_FEED_URLS", "").strip()

    if not raw_urls:
        raise RssConfigError("RSS_FEED_URLS is missing")

    urls = [url.strip() for url in raw_urls.split(",") if url.strip()]

    if not urls:
        raise RssConfigError("RSS_FEED_URLS contains no feed URLs")

    for url in urls:
        if not url.startswith(("https://", "http://")):
            raise RssConfigError("RSS_FEED_URLS contains an invalid URL")

    return urls


class RssFeedError(RuntimeError):
    pass


@dataclass(frozen=True)
class DatabaseConfig:
    dbname: str
    user: str
    password: str
    host: str = '127.0.0.1'
    port: int = 5432


def load_database_config() -> DatabaseConfig:
    env_path = Path(__file__).resolve().parents[2] / '.env'

    if not env_path.is_file():
        raise RssConfigError('.env file is missing')

    values: dict[str, str] = {}

    for raw_line in env_path.read_text(encoding='utf-8').splitlines():
        line = raw_line.strip()

        if not line or line.startswith('#'):
            continue

        key, separator, value = line.partition('=')

        if separator:
            values[key.strip()] = value.strip()

    required = ('POSTGRES_DB', 'APP_DB_USER', 'APP_DB_PASSWORD')
    missing = [name for name in required if not values.get(name)]

    if missing:
        raise RssConfigError(
            'Missing database configuration: ' + ', '.join(missing)
        )

    return DatabaseConfig(
        dbname=values['POSTGRES_DB'],
        user=values['APP_DB_USER'],
        password=values['APP_DB_PASSWORD'],
    )


@dataclass(frozen=True)
class NormalizedFeedItem:
    feed_url: str
    source_name: str | None
    source_item_id: str | None
    title: str | None
    link: str | None
    content_text: str | None
    published_at: datetime | None
    collected_at: datetime


def _local_name(tag: str) -> str:
    return tag.rsplit('}', 1)[-1]


def _child_text(element: ElementTree.Element, name: str) -> str | None:
    for child in element:
        if _local_name(child.tag) == name:
            text = ''.join(child.itertext()).strip()
            return text or None

    return None


def _parse_datetime(value: str | None) -> datetime | None:
    if not value:
        return None

    try:
        parsed = parsedate_to_datetime(value)
    except (TypeError, ValueError):
        parsed = None

    if parsed is None:
        try:
            parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except ValueError:
            return None

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)

    return parsed.astimezone(timezone.utc)


def _atom_link(entry: ElementTree.Element) -> str | None:
    fallback: str | None = None

    for child in entry:
        if _local_name(child.tag) != 'link':
            continue

        href = str(child.attrib.get('href') or '').strip()

        if not href:
            continue

        rel = str(child.attrib.get('rel') or '').strip()

        if rel in ('', 'alternate'):
            return href

        if fallback is None:
            fallback = href

    return fallback


def parse_feed_xml(
    xml_text: str | bytes,
    feed_url: str,
    collected_at: datetime | None = None,
) -> list[NormalizedFeedItem]:
    try:
        root = ElementTree.fromstring(xml_text)
    except ElementTree.ParseError as exc:
        raise RssFeedError('Feed XML is invalid') from exc

    collected = collected_at or datetime.now(timezone.utc)
    root_name = _local_name(root.tag).lower()
    items: list[NormalizedFeedItem] = []

    if root_name == 'rss':
        channel = next(
            (child for child in root if _local_name(child.tag) == 'channel'),
            None,
        )

        if channel is None:
            raise RssFeedError('RSS channel is missing')

        source_name = _child_text(channel, 'title')

        for item in channel:
            if _local_name(item.tag) != 'item':
                continue

            items.append(
                NormalizedFeedItem(
                    feed_url=feed_url,
                    source_name=source_name,
                    source_item_id=_child_text(item, 'guid'),
                    title=_child_text(item, 'title'),
                    link=_child_text(item, 'link'),
                    content_text=_child_text(item, 'description'),
                    published_at=_parse_datetime(_child_text(item, 'pubDate')),
                    collected_at=collected,
                )
            )

        return items

    if root_name == 'feed':
        source_name = _child_text(root, 'title')

        for entry in root:
            if _local_name(entry.tag) != 'entry':
                continue

            content_text = _child_text(entry, 'summary')

            if content_text is None:
                content_text = _child_text(entry, 'content')

            published_text = _child_text(entry, 'published')

            if published_text is None:
                published_text = _child_text(entry, 'updated')

            items.append(
                NormalizedFeedItem(
                    feed_url=feed_url,
                    source_name=source_name,
                    source_item_id=_child_text(entry, 'id'),
                    title=_child_text(entry, 'title'),
                    link=_atom_link(entry),
                    content_text=content_text,
                    published_at=_parse_datetime(published_text),
                    collected_at=collected,
                )
            )

        return items

    raise RssFeedError('Unsupported feed format')


def fetch_feed_xml(feed_url: str) -> bytes:
    feed_request = request.Request(
        feed_url,
        method='GET',
        headers={'User-Agent': 'OpportunityScannerAI/1.0'},
    )

    try:
        with request.urlopen(feed_request, timeout=20) as response:
            body = response.read()
    except (HTTPError, URLError, TimeoutError, OSError) as exc:
        raise RssFeedError('Feed request failed') from exc

    if not body:
        raise RssFeedError('Feed response is empty')

    return body


def build_dedup_key(item: NormalizedFeedItem) -> str:
    feed_url = item.feed_url.strip()

    if not feed_url:
        raise RssFeedError('Feed URL is required for deduplication')

    source_item_id = (item.source_item_id or '').strip()
    link = (item.link or '').strip()

    if source_item_id:
        identity = 'source_item_id:' + source_item_id
    elif link:
        identity = 'link:' + link
    else:
        title = (item.title or '').strip()
        content_text = (item.content_text or '').strip()
        if item.published_at is None:
            published_at = ''
        else:
            published = item.published_at

            if published.tzinfo is None:
                published = published.replace(tzinfo=timezone.utc)

            published_at = published.astimezone(timezone.utc).isoformat()

        if not any((title, content_text, published_at)):
            raise RssFeedError('Feed item has no stable deduplication identity')

        identity = '|'.join(
            (
                'content',
                title,
                published_at,
                content_text,
            )
        )

    payload = (feed_url + '\n' + identity).encode('utf-8')
    return sha256(payload).hexdigest()


BASIC_FILTER_POSITIVE_KEYWORDS = (
    'freelance',
    'remote',
    'tester',
    'testing',
    'data annotation',
    'data labeling',
)

BASIC_FILTER_STOP_WORDS = (
    'unpaid',
    'volunteer',
    'giveaway',
    'lottery',
    'raffle',
)


def evaluate_basic_filter(item: NormalizedFeedItem) -> str:
    text = '\n'.join(
        value
        for value in (item.title, item.content_text)
        if value
    ).casefold()

    if any(stop_word in text for stop_word in BASIC_FILTER_STOP_WORDS):
        return 'REJECT'

    if any(keyword in text for keyword in BASIC_FILTER_POSITIVE_KEYWORDS):
        return 'PASS'

    return 'REJECT'


def persist_basic_filter_result(
    row_id: int,
    filter_state: str,
    config: DatabaseConfig | None = None,
) -> str:
    if filter_state not in ('PASS', 'REJECT'):
        raise RssFeedError('Invalid basic filter state')

    database = config or load_database_config()

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE rss_source_items
                SET filter_state = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING filter_state
                ''',
                (filter_state, row_id),
            )
            row = cursor.fetchone()

            if row is None:
                raise RssFeedError(
                    'RSS item for basic filter persistence was not found'
                )

            return str(row[0])


def mark_telegram_delivered(
    row_id: int,
    config: DatabaseConfig | None = None,
) -> str:
    database = config or load_database_config()

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                UPDATE rss_source_items
                SET telegram_delivery_state = 'DELIVERED',
                    telegram_delivered_at = CURRENT_TIMESTAMP,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                  AND filter_state = 'PASS'
                  AND telegram_delivery_state = 'PENDING'
                RETURNING telegram_delivery_state
                ''',
                (row_id,),
            )
            row = cursor.fetchone()

            if row is not None:
                return str(row[0])

            cursor.execute(
                '''
                SELECT filter_state, telegram_delivery_state
                FROM rss_source_items
                WHERE id = %s
                ''',
                (row_id,),
            )
            existing = cursor.fetchone()

            if existing is None:
                raise RssFeedError(
                    'RSS item for Telegram delivery persistence was not found'
                )

            filter_state, delivery_state = existing

            if filter_state != 'PASS':
                raise RssFeedError(
                    'Only PASS RSS items may be marked as delivered'
                )

            if delivery_state == 'DELIVERED':
                return 'DELIVERED'

            raise RssFeedError(
                'RSS item has an invalid Telegram delivery state'
            )


def deliver_rss_candidate_if_pending(
    row_id: int,
    token: str,
    target_chat_id: int,
    config: DatabaseConfig | None = None,
) -> bool:
    database = config or load_database_config()

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                SELECT filter_state,
                       telegram_delivery_state,
                       title,
                       source_name,
                       link
                FROM rss_source_items
                WHERE id = %s
                ''',
                (row_id,),
            )
            row = cursor.fetchone()

    if row is None:
        raise RssFeedError(
            'RSS item for Telegram delivery was not found'
        )

    (
        filter_state,
        delivery_state,
        title,
        source_name,
        link,
    ) = row

    if filter_state != 'PASS':
        return False

    if delivery_state == 'DELIVERED':
        return False

    if delivery_state != 'PENDING':
        raise RssFeedError(
            'RSS item has an invalid Telegram delivery state'
        )

    send_rss_candidate(
        token,
        target_chat_id,
        title,
        source_name,
        link,
    )

    mark_telegram_delivered(row_id, database)

    return True


def persist_feed_item(
    item: NormalizedFeedItem,
    config: DatabaseConfig | None = None,
) -> tuple[int, bool]:
    database = config or load_database_config()
    dedup_key = build_dedup_key(item)

    with psycopg.connect(
        host=database.host,
        port=database.port,
        dbname=database.dbname,
        user=database.user,
        password=database.password,
    ) as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO rss_source_items (
                    feed_url,
                    source_name,
                    source_item_id,
                    title,
                    link,
                    content_text,
                    published_at,
                    collected_at,
                    dedup_key
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (dedup_key) DO NOTHING
                RETURNING id
                ''',
                (
                    item.feed_url,
                    item.source_name,
                    item.source_item_id,
                    item.title,
                    item.link,
                    item.content_text,
                    item.published_at,
                    item.collected_at,
                    dedup_key,
                ),
            )

            row = cursor.fetchone()

            if row is not None:
                return int(row[0]), True

            cursor.execute(
                'SELECT id FROM rss_source_items WHERE dedup_key = %s',
                (dedup_key,),
            )
            existing = cursor.fetchone()

            if existing is None:
                raise RssFeedError(
                    'RSS item persistence conflict could not be resolved'
                )

            return int(existing[0]), False

@dataclass(frozen=True)
class BoundedFeedVerificationResult:
    feed_url: str
    parsed_item_count: int
    selected_item: bool
    row_id: int | None
    created: bool | None
    filter_state: str | None
    telegram_sent: bool


def process_bounded_feed_xml(
    xml_text: str | bytes,
    feed_url: str,
    token: str,
    target_chat_id: int,
    config: DatabaseConfig | None = None,
) -> BoundedFeedVerificationResult:
    items = parse_feed_xml(xml_text, feed_url)

    if not items:
        return BoundedFeedVerificationResult(
            feed_url=feed_url,
            parsed_item_count=0,
            selected_item=False,
            row_id=None,
            created=None,
            filter_state=None,
            telegram_sent=False,
        )

    selected_item = items[0]

    row_id, created = persist_feed_item(
        selected_item,
        config,
    )

    filter_state = evaluate_basic_filter(selected_item)

    persisted_filter_state = persist_basic_filter_result(
        row_id,
        filter_state,
        config,
    )

    telegram_sent = deliver_rss_candidate_if_pending(
        row_id,
        token,
        target_chat_id,
        config,
    )

    return BoundedFeedVerificationResult(
        feed_url=feed_url,
        parsed_item_count=len(items),
        selected_item=True,
        row_id=row_id,
        created=created,
        filter_state=persisted_filter_state,
        telegram_sent=telegram_sent,
    )


def run_bounded_live_feed_verification(
    feed_url: str,
    token: str,
    target_chat_id: int,
    config: DatabaseConfig | None = None,
) -> BoundedFeedVerificationResult:
    configured_feed_urls = load_rss_feed_urls()

    if feed_url not in configured_feed_urls:
        raise RssConfigError(
            'Bounded verification feed URL is not in RSS_FEED_URLS'
        )

    xml_text = fetch_feed_xml(feed_url)

    return process_bounded_feed_xml(
        xml_text,
        feed_url,
        token,
        target_chat_id,
        config,
    )
