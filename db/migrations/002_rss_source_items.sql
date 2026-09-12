BEGIN;

CREATE TABLE IF NOT EXISTS rss_source_items (
    id bigserial PRIMARY KEY,
    feed_url text NOT NULL,
    source_name text,
    source_item_id text,
    title text,
    link text,
    content_text text,
    published_at timestamptz,
    collected_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dedup_key text NOT NULL UNIQUE,
    filter_state text NOT NULL DEFAULT 'PENDING'
        CHECK (filter_state IN ('PENDING', 'PASS', 'REJECT')),
    telegram_delivery_state text NOT NULL DEFAULT 'PENDING'
        CHECK (telegram_delivery_state IN ('PENDING', 'DELIVERED')),
    telegram_delivered_at timestamptz,
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO schema_migrations (version)
VALUES (2)
ON CONFLICT (version) DO NOTHING;

COMMIT;
