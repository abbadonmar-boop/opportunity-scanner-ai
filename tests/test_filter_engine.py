from __future__ import annotations

import sys
import unittest
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"

if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))


from opportunity_scanner.filter_engine import (  # noqa: E402
    HARD_REJECT_RULES,
    POSITIVE_RULES,
    FilterEngineError,
    evaluate_filter,
)
from opportunity_scanner import rss_collector  # noqa: E402
from opportunity_scanner.rss_collector import (  # noqa: E402
    NormalizedFeedItem,
    evaluate_basic_filter,
)


class FilterEngineTests(unittest.TestCase):
    def test_every_hard_reject_rule_rejects(self) -> None:
        for rule in HARD_REJECT_RULES:
            with self.subTest(rule=rule):
                self.assertEqual(
                    evaluate_filter("freelance", rule),
                    "REJECT",
                )

    def test_every_positive_rule_passes(self) -> None:
        for rule in POSITIVE_RULES:
            with self.subTest(rule=rule):
                self.assertEqual(evaluate_filter(rule, None), "PASS")

    def test_hard_reject_has_priority_over_positive(self) -> None:
        self.assertEqual(
            evaluate_filter("Freelance tester", "Volunteer opportunity"),
            "REJECT",
        )

    def test_matching_is_casefolded(self) -> None:
        self.assertEqual(evaluate_filter("FREELANCE", None), "PASS")

    def test_phrase_rule_requires_contiguous_phrase(self) -> None:
        self.assertEqual(evaluate_filter("remote work", None), "PASS")
        self.assertEqual(evaluate_filter("remote flexible work", None), "REJECT")

    def test_single_word_rule_matches_complete_token(self) -> None:
        self.assertEqual(evaluate_filter("tester.", None), "PASS")

    def test_single_word_rule_does_not_match_inside_larger_token(self) -> None:
        self.assertEqual(evaluate_filter("contesttester", None), "REJECT")
        self.assertEqual(evaluate_filter("tester123", None), "REJECT")
        self.assertEqual(evaluate_filter("prefix_tester_suffix", None), "REJECT")

    def test_multilingual_positive_rules(self) -> None:
        cases = (
            "freelance",
            "тестировщик",
            "тестувальник",
            "softwaretester",
        )

        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(evaluate_filter(text, None), "PASS")

    def test_multilingual_hard_reject_rules(self) -> None:
        cases = (
            "unpaid",
            "без оплаты",
            "без оплати",
            "unbezahlt",
        )

        for text in cases:
            with self.subTest(text=text):
                self.assertEqual(evaluate_filter(text, None), "REJECT")

    def test_default_is_reject(self) -> None:
        self.assertEqual(
            evaluate_filter("general project announcement", None),
            "REJECT",
        )

    def test_none_values_are_supported(self) -> None:
        self.assertEqual(evaluate_filter(None, None), "REJECT")

    def test_invalid_input_type_is_rejected_safely(self) -> None:
        with self.assertRaises(FilterEngineError):
            evaluate_filter(123, None)  # type: ignore[arg-type]

    def test_negation_is_not_semantically_interpreted(self) -> None:
        self.assertEqual(
            evaluate_filter("freelance opportunity", "not unpaid"),
            "REJECT",
        )

    def test_downstream_risk_terms_do_not_force_hard_reject(self) -> None:
        self.assertEqual(
            evaluate_filter("freelance wallet connection task", None),
            "PASS",
        )

    def test_payout_amount_is_not_a_module_6_filter_rule(self) -> None:
        self.assertEqual(
            evaluate_filter("freelance task paying $1", None),
            "PASS",
        )


class RssFilterIntegrationTests(unittest.TestCase):
    def _item(
        self,
        *,
        title: str | None,
        content_text: str | None,
    ) -> NormalizedFeedItem:
        return NormalizedFeedItem(
            feed_url="https://example.com/feed.xml",
            source_name="Example",
            source_item_id="item-1",
            title=title,
            link="https://example.com/item-1",
            content_text=content_text,
            published_at=None,
            collected_at=datetime.now(timezone.utc),
        )

    def test_rss_wrapper_passes_positive_candidate(self) -> None:
        item = self._item(
            title="Freelance tester opportunity",
            content_text=None,
        )

        self.assertEqual(evaluate_basic_filter(item), "PASS")

    def test_rss_wrapper_rejects_hard_reject_candidate(self) -> None:
        item = self._item(
            title="Freelance tester opportunity",
            content_text="Volunteer position",
        )

        self.assertEqual(evaluate_basic_filter(item), "REJECT")

    def test_rss_wrapper_uses_content_text(self) -> None:
        item = self._item(
            title="General announcement",
            content_text="Remote work opportunity",
        )

        self.assertEqual(evaluate_basic_filter(item), "PASS")


class RssPersistenceAndDeliveryAcceptanceTests(unittest.TestCase):
    def _database_config(self) -> rss_collector.DatabaseConfig:
        return rss_collector.DatabaseConfig(
            dbname="test_db",
            user="test_user",
            password="test_password",
        )

    def _mock_connection(
        self,
        fetchone_result: tuple[object, ...] | None,
    ) -> tuple[MagicMock, MagicMock]:
        cursor = MagicMock()
        cursor.fetchone.return_value = fetchone_result

        cursor_context = MagicMock()
        cursor_context.__enter__.return_value = cursor

        connection = MagicMock()
        connection.cursor.return_value = cursor_context

        connection_context = MagicMock()
        connection_context.__enter__.return_value = connection

        return connection_context, cursor

    def test_pass_filter_state_is_persisted(self) -> None:
        connection_context, cursor = self._mock_connection(("PASS",))
        config = self._database_config()

        with patch.object(
            rss_collector.psycopg,
            "connect",
            return_value=connection_context,
        ):
            result = rss_collector.persist_basic_filter_result(
                101,
                "PASS",
                config,
            )

        self.assertEqual(result, "PASS")
        self.assertEqual(cursor.execute.call_args.args[1], ("PASS", 101))

    def test_reject_filter_state_is_persisted(self) -> None:
        connection_context, cursor = self._mock_connection(("REJECT",))
        config = self._database_config()

        with patch.object(
            rss_collector.psycopg,
            "connect",
            return_value=connection_context,
        ):
            result = rss_collector.persist_basic_filter_result(
                102,
                "REJECT",
                config,
            )

        self.assertEqual(result, "REJECT")
        self.assertEqual(cursor.execute.call_args.args[1], ("REJECT", 102))

    def test_reject_item_is_not_telegram_eligible(self) -> None:
        connection_context, _ = self._mock_connection(
            (
                "REJECT",
                "PENDING",
                "Freelance tester opportunity",
                "Example",
                "https://example.com/item",
            )
        )
        config = self._database_config()

        with (
            patch.object(
                rss_collector.psycopg,
                "connect",
                return_value=connection_context,
            ),
            patch.object(rss_collector, "send_rss_candidate") as send_mock,
            patch.object(
                rss_collector,
                "mark_telegram_delivered",
            ) as delivered_mock,
        ):
            result = rss_collector.deliver_rss_candidate_if_pending(
                103,
                "token",
                123456,
                config,
            )

        self.assertFalse(result)
        send_mock.assert_not_called()
        delivered_mock.assert_not_called()

    def test_pass_pending_item_is_sent_and_marked_delivered(self) -> None:
        connection_context, _ = self._mock_connection(
            (
                "PASS",
                "PENDING",
                "Freelance tester opportunity",
                "Example",
                "https://example.com/item",
            )
        )
        config = self._database_config()

        with (
            patch.object(
                rss_collector.psycopg,
                "connect",
                return_value=connection_context,
            ),
            patch.object(rss_collector, "send_rss_candidate") as send_mock,
            patch.object(
                rss_collector,
                "mark_telegram_delivered",
                return_value="DELIVERED",
            ) as delivered_mock,
        ):
            result = rss_collector.deliver_rss_candidate_if_pending(
                104,
                "token",
                123456,
                config,
            )

        self.assertTrue(result)
        send_mock.assert_called_once_with(
            "token",
            123456,
            "Freelance tester opportunity",
            "Example",
            "https://example.com/item",
        )
        delivered_mock.assert_called_once_with(104, config)

    def test_delivered_pass_item_is_not_sent_again(self) -> None:
        connection_context, _ = self._mock_connection(
            (
                "PASS",
                "DELIVERED",
                "Freelance tester opportunity",
                "Example",
                "https://example.com/item",
            )
        )
        config = self._database_config()

        with (
            patch.object(
                rss_collector.psycopg,
                "connect",
                return_value=connection_context,
            ),
            patch.object(rss_collector, "send_rss_candidate") as send_mock,
            patch.object(
                rss_collector,
                "mark_telegram_delivered",
            ) as delivered_mock,
        ):
            result = rss_collector.deliver_rss_candidate_if_pending(
                105,
                "token",
                123456,
                config,
            )

        self.assertFalse(result)
        send_mock.assert_not_called()
        delivered_mock.assert_not_called()


if __name__ == "__main__":
    unittest.main()
