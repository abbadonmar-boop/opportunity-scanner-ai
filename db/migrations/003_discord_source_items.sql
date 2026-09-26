BEGIN;

CREATE TABLE IF NOT EXISTS discord_source_items (
    id bigserial PRIMARY KEY,
    guild_id text NOT NULL,
    channel_id text NOT NULL,
    message_id text NOT NULL,
    author_id text NOT NULL,
    content_text text NOT NULL,
    published_at timestamptz NOT NULL,
    edited_at timestamptz,
    collected_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    dedup_key text NOT NULL UNIQUE,
    filter_state text NOT NULL DEFAULT 'PENDING'
        CHECK (filter_state IN ('PENDING', 'PASS', 'REJECT')),
    created_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamptz NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (guild_id, channel_id, message_id)
);

CREATE INDEX IF NOT EXISTS idx_discord_source_items_channel_message
    ON discord_source_items (channel_id, message_id);

INSERT INTO schema_migrations (version)
VALUES (3)
ON CONFLICT (version) DO NOTHING;

COMMIT;
