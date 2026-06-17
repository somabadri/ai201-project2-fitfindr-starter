from unittest.mock import MagicMock, patch

import pytest

from tools import create_fit_card, search_listings, suggest_outfit


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def sample_item():
    return {
        "id": "lst_002",
        "title": "Y2K Baby Tee — Butterfly Print",
        "description": "Super cute early 2000s baby tee with butterfly graphic.",
        "category": "tops",
        "style_tags": ["y2k", "vintage", "graphic tee"],
        "size": "S/M",
        "condition": "excellent",
        "price": 18.00,
        "colors": ["white", "pink", "purple"],
        "brand": None,
        "platform": "depop",
    }


@pytest.fixture
def mock_groq_response():
    """Returns a factory that builds a fake Groq API response."""
    def _make(text: str):
        response = MagicMock()
        response.choices[0].message.content = text
        return response
    return _make


# ── search_listings ───────────────────────────────────────────────────────────

def test_search_returns_results():
    results = search_listings("vintage graphic tee", size=None, max_price=50)
    assert isinstance(results, list)
    assert len(results) > 0


def test_search_empty_results():
    # Failure mode: no listings match → empty list, no exception
    results = search_listings("designer ballgown", size="XXS", max_price=5)
    assert results == []


def test_search_price_filter():
    results = search_listings("jacket", size=None, max_price=10)
    assert all(item["price"] <= 10 for item in results)


def test_search_size_filter_case_insensitive():
    # "m" should match listings sized "S/M" or "M"
    results = search_listings("tee", size="m", max_price=None)
    assert all("m" in item["size"].lower() for item in results)


def test_search_results_are_sorted_by_relevance():
    # The first result should be more relevant than the last
    results = search_listings("vintage denim jeans", size=None, max_price=None)
    assert len(results) > 1
    # Titles/tags of the top result should include at least one query word
    top = results[0]
    searchable = " ".join([top["title"], top["description"], " ".join(top["style_tags"])]).lower()
    assert any(word in searchable for word in ["vintage", "denim", "jeans"])


# ── suggest_outfit ────────────────────────────────────────────────────────────

@patch("tools._get_groq_client")
def test_suggest_outfit_with_wardrobe(mock_client, sample_item, mock_groq_response):
    mock_client.return_value.chat.completions.create.return_value = mock_groq_response(
        "Pair the tee with your baggy jeans and chunky sneakers."
    )
    wardrobe = {"items": [{"name": "baggy jeans", "style_tags": ["streetwear"]}]}
    result = suggest_outfit(sample_item, wardrobe)
    assert isinstance(result, str)
    assert len(result) > 0


@patch("tools._get_groq_client")
def test_suggest_outfit_empty_wardrobe(mock_client, sample_item, mock_groq_response):
    # Failure mode: wardrobe is empty → general advice, no exception
    mock_client.return_value.chat.completions.create.return_value = mock_groq_response(
        "This tee pairs well with high-waisted bottoms and sneakers."
    )
    result = suggest_outfit(sample_item, {"items": []})
    assert isinstance(result, str)
    assert len(result) > 0


@patch("tools._get_groq_client")
def test_suggest_outfit_missing_items_key(mock_client, sample_item, mock_groq_response):
    # Wardrobe dict with no 'items' key at all should not crash
    mock_client.return_value.chat.completions.create.return_value = mock_groq_response(
        "Style this tee with wide-leg trousers."
    )
    result = suggest_outfit(sample_item, {})
    assert isinstance(result, str)
    assert len(result) > 0


# ── create_fit_card ───────────────────────────────────────────────────────────

@patch("tools._get_groq_client")
def test_create_fit_card_returns_caption(mock_client, sample_item, mock_groq_response):
    mock_client.return_value.chat.completions.create.return_value = mock_groq_response(
        "Thrifted this butterfly tee off Depop for $18 and I'm never taking it off."
    )
    result = create_fit_card("Pair with baggy jeans and sneakers.", sample_item)
    assert isinstance(result, str)
    assert len(result) > 0


def test_create_fit_card_empty_outfit_string(sample_item):
    # Failure mode: empty outfit → error message string, no exception
    result = create_fit_card("", sample_item)
    assert isinstance(result, str)
    assert len(result) > 0


def test_create_fit_card_whitespace_outfit(sample_item):
    # Whitespace-only outfit should also be caught
    result = create_fit_card("   ", sample_item)
    assert isinstance(result, str)
    assert len(result) > 0
