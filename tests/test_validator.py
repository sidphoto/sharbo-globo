import copy
import json
from pathlib import Path

import pytest

from sharbo_globo.validator import ValidationError, validate_bundle


@pytest.fixture
def valid_bundle():
    path = Path("examples/data/localization-bundle.json")
    return json.loads(path.read_text(encoding="utf-8"))


def test_complete_bundle_passes(valid_bundle):
    validate_bundle(valid_bundle)


def test_missing_locale_fails_closed(valid_bundle):
    invalid = copy.deepcopy(valid_bundle)
    del invalid["localizations"]["vi-VN"]
    with pytest.raises(ValidationError, match="vi-VN"):
        validate_bundle(invalid)


def test_empty_required_field_fails_closed(valid_bundle):
    invalid = copy.deepcopy(valid_bundle)
    invalid["localizations"]["en"]["signals"][0]["why_now"] = ""
    with pytest.raises(ValidationError, match="why_now"):
        validate_bundle(invalid)


def test_signal_order_must_match_canonical(valid_bundle):
    invalid = copy.deepcopy(valid_bundle)
    invalid["localizations"]["zh-TW"]["signals"][0]["id"] = "wrong-id"
    with pytest.raises(ValidationError, match="canonical IDs and order"):
        validate_bundle(invalid)


def test_ready_marker_is_required(valid_bundle):
    invalid = copy.deepcopy(valid_bundle)
    invalid["ready"]["status"] = "building"
    with pytest.raises(ValidationError, match="ready.status"):
        validate_bundle(invalid)
