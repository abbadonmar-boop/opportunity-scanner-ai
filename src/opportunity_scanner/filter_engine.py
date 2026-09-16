from __future__ import annotations

import re


class FilterEngineError(ValueError):
    """Raised when Filter Engine input is invalid."""


FILTER_LANGUAGES = ("EN", "RU", "UA", "DE")


HARD_REJECT_RULES_BY_LANGUAGE = {
    "EN": (
        "unpaid",
        "volunteer",
        "giveaway",
        "lottery",
        "raffle",
        "xp only",
        "points only",
    ),
    "RU": (
        "без оплаты",
        "неоплачиваем",
        "волонтёр",
        "волонтер",
        "розыгрыш",
        "лотерея",
        "только xp",
        "только баллы",
    ),
    "UA": (
        "без оплати",
        "неоплачув",
        "волонтер",
        "розіграш",
        "лотерея",
        "лише xp",
        "лише бали",
    ),
    "DE": (
        "unbezahlt",
        "ehrenamt",
        "gewinnspiel",
        "lotterie",
        "verlosung",
        "nur xp",
        "nur punkte",
    ),
}


POSITIVE_RULES_BY_LANGUAGE = {
    "EN": (
        "freelance",
        "freelance task",
        "remote work",
        "remote job",
        "part-time remote",
        "entry level",
        "no experience",
        "hiring now",
        "contributors wanted",
        "tester",
        "testing",
        "qa tester",
        "bug testing",
        "usability testing",
        "paid beta testing",
        "beta tester",
        "data annotation",
        "data labeling",
        "ai rater",
        "ai evaluator",
        "llm trainer",
        "model reviewer",
        "search evaluator",
        "data collection",
        "paid testnet",
        "web3 task",
    ),
    "RU": (
        "фриланс",
        "удалённая работа",
        "удаленная работа",
        "удалённая подработка",
        "удаленная подработка",
        "без опыта",
        "тестировщик",
        "тестирование",
        "qa тестировщик",
        "поиск багов",
        "юзабилити тестирование",
        "платное бета-тестирование",
        "разметка данных",
        "оценщик ии",
        "оценщик ai",
        "тренер llm",
        "проверка модели",
        "проверка ответов ии",
        "сбор данных",
        "платный тестнет",
        "оплачиваемое web3 задание",
    ),
    "UA": (
        "фриланс",
        "віддалена робота",
        "віддалена підробітка",
        "без досвіду",
        "тестувальник",
        "тестування",
        "qa тестувальник",
        "пошук багів",
        "юзабіліті тестування",
        "платне бета-тестування",
        "розмітка даних",
        "оцінювач ші",
        "оцінювач ai",
        "тренер llm",
        "перевірка моделі",
        "перевірка відповідей ші",
        "збір даних",
        "платний тестнет",
        "оплачуване web3 завдання",
    ),
    "DE": (
        "freelance",
        "freiberuflich",
        "remote arbeit",
        "remote-arbeit",
        "homeoffice",
        "teilzeit remote",
        "berufseinsteiger",
        "ohne erfahrung",
        "tester",
        "softwaretester",
        "testing",
        "qa tester",
        "bug testing",
        "usability testing",
        "bezahlter betatest",
        "datenannotation",
        "datenlabeling",
        "datenerfassung",
        "ki-bewertung",
        "ai evaluator",
        "llm-trainer",
        "modellbewertung",
        "bezahltes testnet",
        "bezahlte web3-aufgabe",
    ),
}


HARD_REJECT_RULES = tuple(
    rule
    for language in FILTER_LANGUAGES
    for rule in HARD_REJECT_RULES_BY_LANGUAGE[language]
)

POSITIVE_RULES = tuple(
    rule
    for language in FILTER_LANGUAGES
    for rule in POSITIVE_RULES_BY_LANGUAGE[language]
)


def _normalize_input(value: str | None, field_name: str) -> str:
    if value is None:
        return ""

    if not isinstance(value, str):
        raise FilterEngineError(f"{field_name} must be str or None")

    return value


def _is_phrase(rule: str) -> bool:
    return any(character.isspace() for character in rule)


def _matches_rule(normalized_text: str, rule: str) -> bool:
    normalized_rule = rule.casefold()

    if _is_phrase(normalized_rule):
        return normalized_rule in normalized_text

    pattern = rf"(?<!\w){re.escape(normalized_rule)}(?!\w)"
    return re.search(pattern, normalized_text, flags=re.UNICODE) is not None


def evaluate_filter(
    title: str | None,
    content_text: str | None,
) -> str:
    normalized_title = _normalize_input(title, "title")
    normalized_content = _normalize_input(content_text, "content_text")

    normalized_text = "\n".join(
        value
        for value in (normalized_title, normalized_content)
        if value
    ).casefold()

    if any(
        _matches_rule(normalized_text, rule)
        for rule in HARD_REJECT_RULES
    ):
        return "REJECT"

    if any(
        _matches_rule(normalized_text, rule)
        for rule in POSITIVE_RULES
    ):
        return "PASS"

    return "REJECT"
