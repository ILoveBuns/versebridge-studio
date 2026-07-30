"""Biometric moment detection and official verse-mapping selection."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


OFFICIAL_MAPPING = (
    Path(__file__).parent
    / "data"
    / "official"
    / "extracted"
    / "verse movement mapping.csv"
)


@dataclass(frozen=True)
class BiometricSnapshot:
    heart_rate: int
    hr_zone: int
    activity_type: str
    effort_pct: float
    recovery_score: int
    stress_index: float
    session_minute: int


FALLBACK_MAPPINGS = [
    {
        "moment_type": "peak_effort",
        "verse_reference": "ISA.40.31",
        "verse_text_preview": "Those who hope in the LORD will renew their strength",
        "translation": "NIV",
        "theme_tag": "endurance",
        "delivery_format": "haptic_pulse + display",
        "hr_zone_trigger": "5",
        "effort_pct_trigger": "0.85",
        "activity_context": "running/cycling",
    },
    {
        "moment_type": "breakthrough_wall",
        "verse_reference": "PHI.4.13",
        "verse_text_preview": "I can do all this through him who gives me strength",
        "translation": "NIV",
        "theme_tag": "strength",
        "delivery_format": "haptic_pulse + audio",
        "hr_zone_trigger": "4",
        "effort_pct_trigger": "0.75",
        "activity_context": "running",
    },
    {
        "moment_type": "recovery",
        "verse_reference": "PSA.46.10",
        "verse_text_preview": "Be still, and know that I am God",
        "translation": "NIV",
        "theme_tag": "rest",
        "delivery_format": "display_only",
        "hr_zone_trigger": "1",
        "effort_pct_trigger": "0.20",
        "activity_context": "all",
    },
]


def load_mappings(path: Path = OFFICIAL_MAPPING) -> list[dict[str, str]]:
    if not path.is_file():
        return FALLBACK_MAPPINGS
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def detect_moment(snapshot: BiometricSnapshot) -> str:
    if snapshot.hr_zone >= 5 or snapshot.effort_pct >= 0.88:
        return "peak_effort"
    if snapshot.activity_type == "weightlifting" and snapshot.effort_pct >= 0.80:
        return "final_rep"
    if snapshot.hr_zone >= 4 and snapshot.effort_pct >= 0.75:
        return "breakthrough_wall"
    if snapshot.session_minute >= 20 and snapshot.effort_pct >= 0.70:
        return "finishing_strong"
    if snapshot.hr_zone <= 1 and snapshot.effort_pct <= 0.25:
        return "recovery"
    return "steady_state"


def select_delivery(
    snapshot: BiometricSnapshot, mappings: list[dict[str, str]] | None = None
) -> dict[str, str]:
    moment = detect_moment(snapshot)
    candidates = [
        row for row in (mappings or load_mappings()) if row["moment_type"] == moment
    ]
    if not candidates:
        candidates = [
            row
            for row in (mappings or load_mappings())
            if row["moment_type"] in {"steady_state", "recovery"}
        ]
    if not candidates:
        candidates = FALLBACK_MAPPINGS

    def score(row: dict[str, str]) -> tuple[int, float]:
        contexts = row["activity_context"].split("/")
        context_match = snapshot.activity_type in contexts or "all" in contexts
        trigger_distance = abs(
            snapshot.effort_pct - float(row.get("effort_pct_trigger") or 0)
        )
        return (1 if context_match else 0, -trigger_distance)

    selected = max(candidates, key=score)
    return {
        **selected,
        "detected_moment": moment,
        "live_heart_rate": str(snapshot.heart_rate),
        "live_effort_pct": f"{snapshot.effort_pct:.2f}",
    }
