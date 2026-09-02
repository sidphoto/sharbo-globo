"""Fail-closed validation for a persisted multilingual publication bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .contracts import REQUIRED_SIGNAL_FIELDS, STRUCTURED_LOCALES, SUPPORTED_LOCALES


class ValidationError(ValueError):
    """Raised when a bundle is not safe to publish."""


def _require_nonempty_text(value: Any, path: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{path} must be non-empty text")


def _require_unique_text_ids(values: Any, path: str) -> list[str]:
    if not isinstance(values, list) or not values:
        raise ValidationError(f"{path} must be a non-empty list")
    if not all(isinstance(value, str) and value.strip() for value in values):
        raise ValidationError(f"{path} must contain non-empty text IDs")
    if len(values) != len(set(values)):
        raise ValidationError(f"{path} must not contain duplicate IDs")
    return values


def validate_bundle(bundle: Any) -> None:
    """Validate the complete persisted state or raise ValidationError.

    The validator intentionally accepts no partial-success mode. Callers may
    write a READY marker only after this function returns successfully.
    """

    if not isinstance(bundle, dict):
        raise ValidationError("bundle must be an object")

    canonical = bundle.get("canonical")
    if not isinstance(canonical, dict):
        raise ValidationError("canonical must be an object")
    canonical_ids = _require_unique_text_ids(
        canonical.get("signal_ids"), "canonical.signal_ids"
    )

    localizations = bundle.get("localizations")
    if not isinstance(localizations, dict):
        raise ValidationError("localizations must be an object")

    for locale in SUPPORTED_LOCALES:
        localized = localizations.get(locale)
        if not isinstance(localized, dict):
            raise ValidationError(f"localizations.{locale} must be an object")
        _require_nonempty_text(
            localized.get("world_summary"),
            f"localizations.{locale}.world_summary",
        )

        signals = localized.get("signals")
        if not isinstance(signals, list):
            raise ValidationError(f"localizations.{locale}.signals must be a list")
        signal_ids = [signal.get("id") for signal in signals if isinstance(signal, dict)]
        if len(signal_ids) != len(signals) or signal_ids != canonical_ids:
            raise ValidationError(
                f"localizations.{locale}.signals must match canonical IDs and order"
            )
        for index, signal in enumerate(signals):
            for field in REQUIRED_SIGNAL_FIELDS:
                _require_nonempty_text(
                    signal.get(field),
                    f"localizations.{locale}.signals[{index}].{field}",
                )

        radar = localized.get("taiwan_radar")
        if not isinstance(radar, list):
            raise ValidationError(
                f"localizations.{locale}.taiwan_radar must be a list"
            )
        radar_ids = [item.get("signal_id") for item in radar if isinstance(item, dict)]
        if len(radar_ids) != len(radar) or radar_ids != canonical_ids:
            raise ValidationError(
                f"localizations.{locale}.taiwan_radar must match canonical IDs and order"
            )
        for index, item in enumerate(radar):
            _require_nonempty_text(
                item.get("text"),
                f"localizations.{locale}.taiwan_radar[{index}].text",
            )

    structures = bundle.get("structures")
    if not isinstance(structures, dict):
        raise ValidationError("structures must be an object")
    canonical_emerging = _require_unique_text_ids(
        canonical.get("emerging_signal_ids"), "canonical.emerging_signal_ids"
    )
    canonical_chains = _require_unique_text_ids(
        canonical.get("impact_chain_ids"), "canonical.impact_chain_ids"
    )

    for locale in STRUCTURED_LOCALES:
        structure = structures.get(locale)
        if not isinstance(structure, dict):
            raise ValidationError(f"structures.{locale} must be an object")
        if structure.get("emerging_signal_ids") != canonical_emerging:
            raise ValidationError(
                f"structures.{locale}.emerging_signal_ids must match canonical IDs"
            )
        chains = structure.get("impact_chains")
        if not isinstance(chains, list):
            raise ValidationError(f"structures.{locale}.impact_chains must be a list")
        chain_ids = [chain.get("id") for chain in chains if isinstance(chain, dict)]
        if len(chain_ids) != len(chains) or chain_ids != canonical_chains:
            raise ValidationError(
                f"structures.{locale}.impact_chains must match canonical IDs and order"
            )
        for chain_index, chain in enumerate(chains):
            nodes = chain.get("nodes")
            if not isinstance(nodes, list) or not nodes:
                raise ValidationError(
                    f"structures.{locale}.impact_chains[{chain_index}].nodes must be non-empty"
                )
            for node_index, node in enumerate(nodes):
                if not isinstance(node, dict):
                    raise ValidationError(
                        f"structures.{locale}.impact_chains[{chain_index}].nodes[{node_index}] must be an object"
                    )
                _require_nonempty_text(
                    node.get("label"),
                    f"structures.{locale}.impact_chains[{chain_index}].nodes[{node_index}].label",
                )
        if structure.get("featured_chain_id") not in canonical_chains:
            raise ValidationError(
                f"structures.{locale}.featured_chain_id must reference an impact chain"
            )

    ready = bundle.get("ready")
    if not isinstance(ready, dict) or ready.get("status") != "ready":
        raise ValidationError("ready.status must equal 'ready'")


def load_and_validate(path: Path) -> None:
    with path.open("r", encoding="utf-8") as handle:
        validate_bundle(json.load(handle))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("bundle", type=Path)
    args = parser.parse_args()
    try:
        load_and_validate(args.bundle)
    except (OSError, json.JSONDecodeError, ValidationError) as error:
        print(f"FAIL: {error}")
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
