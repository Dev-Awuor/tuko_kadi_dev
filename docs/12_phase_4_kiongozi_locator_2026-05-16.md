---
title: "Phase 4 — Kiongozi Polling Station Locator"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Phase 4 — Kiongozi: Polling Station Locator

**Document ID:** SYM-IMPL-P4  
**Created:** 2026-05-16T10:40:00+03:00  
**Last Modified:** 2026-05-16T10:40:00+03:00  
**Phase Status:** ☐ Pending

---

## Phase Objective

Build the polling station CSV database, implement geo-lookup tools that search by county/constituency/ward, and upgrade Kiongozi from a stub to a fully functional polling station locator agent — all without requiring users to share personal identification.

---

## Dependencies & Blockers

| Dependency | Type | Resolution |
|-----------|------|-----------|
| Phase 2 complete | **BLOCKER** | Msaidizi must route polling queries to Kiongozi |
| IEBC polling station data | **BLOCKER** | Must obtain or create representative station dataset |

---

## Action Items

### Step 4.1 — Polling Station Seed Data

Kenya has 47 counties, 290 constituencies, and ~46,000+ polling stations. For the hackathon we create a representative sample dataset covering major counties. This can be expanded post-hackathon with full IEBC data.

```
[Artifact Type: Data File] | [File Name: data/polling_stations.csv] | [Timestamp: 2026-05-16 10:41 EAT]
```

```csv
county,constituency,ward,station_name,address
Nairobi,Westlands,Kangemi,Kangemi Primary School,"Kangemi Road, off Waiyaki Way"
Nairobi,Westlands,Kitisuru,Kitisuru Primary School,"Peponi Road, Kitisuru"
Nairobi,Westlands,Mountain View,Mountain View Primary School,"Mountain View Estate"
Nairobi,Dagoretti North,Kilimani,Kilimani Primary School,"Argwings Kodhek Road"
Nairobi,Dagoretti North,Kawangware,Kawangware Primary School,"Naivasha Road, Kawangware"
Nairobi,Langata,Karen,Karen C Primary School,"Karen Road, Karen"
Nairobi,Langata,Mugumo-ini,Mugumo-ini Primary School,"Langata South Road"
Nairobi,Starehe,Nairobi Central,Jamhuri Primary School,"Haile Selassie Avenue"
Nairobi,Kasarani,Roysambu,Roysambu Primary School,"Thika Road, Roysambu"
Nairobi,Kasarani,Zimmerman,Zimmerman Primary School,"Zimmerman Estate"
Nairobi,Embakasi East,Utawala,Utawala Primary School,"Kangundo Road, Utawala"
Nairobi,Embakasi Central,Kayole South,Kayole South Primary School,"Kayole Estate"
Mombasa,Mvita,Majengo,Majengo Primary School,"Majengo Road, Mombasa"
Mombasa,Mvita,Tudor,Tudor Day Secondary School,"Tudor Estate"
Mombasa,Kisauni,Mjambere,Mjambere Primary School,"Kisauni Road"
Mombasa,Likoni,Likoni,Likoni Primary School,"Likoni Ferry Road"
Kisumu,Kisumu Central,Railways,Railways Primary School,"Oginga Odinga Road"
Kisumu,Kisumu Central,Kondele,Kondele Primary School,"Kondele Market Area"
Kisumu,Kisumu East,Kolwa Central,Kolwa Primary School,"Kolwa East Road"
Nakuru,Nakuru Town East,Biashara,Menengai Primary School,"Kenyatta Avenue, Nakuru"
Nakuru,Nakuru Town West,Kaptembwo,Kaptembwo Primary School,"Kaptembwo Estate"
Nakuru,Naivasha,Hells Gate,Naivasha Primary School,"Moi South Lake Road"
Kiambu,Thika Town,Kamenu,Kamenu Primary School,"Thika Town Centre"
Kiambu,Ruiru,Gitothua,Gitothua Primary School,"Thika Superhighway"
Kiambu,Juja,Juja,Juja Primary School,"Juja Town"
Uasin Gishu,Ainabkoi,Ainabkoi,Ainabkoi Primary School,"Ainabkoi Road, Eldoret"
Uasin Gishu,Kapseret,Langas,Langas Primary School,"Langas Estate, Eldoret"
Kakamega,Lurambi,Butsotso Central,Butsotso Primary School,"Kakamega Town"
Machakos,Machakos Town,Machakos Central,Machakos Primary School,"Machakos CBD"
Nyeri,Nyeri Town,Rware,Rware Primary School,"Nyeri Town Centre"
Kilifi,Kilifi North,Tezo,Tezo Primary School,"Kilifi-Malindi Road"
Garissa,Garissa Township,Galbet,Galbet Primary School,"Garissa Town Centre"
Bungoma,Kanduyi,Khalaba,Khalaba Primary School,"Bungoma-Webuye Road"
Meru,Imenti Central,Abothuguchi Central,Nkubu Primary School,"Nkubu Town"
Kajiado,Kajiado North,Ongata Rongai,Ongata Rongai Primary School,"Magadi Road"
```

```
[Artifact Type: Data File] | [File Name: data/constituencies.json] | [Timestamp: 2026-05-16 10:42 EAT]
```

```json
{
  "Nairobi": ["Westlands", "Dagoretti North", "Dagoretti South", "Langata", "Kibra", "Roysambu", "Kasarani", "Starehe", "Mathare", "Embakasi South", "Embakasi North", "Embakasi Central", "Embakasi East", "Embakasi West", "Makadara", "Kamukunji", "Ruaraka"],
  "Mombasa": ["Mvita", "Kisauni", "Likoni", "Nyali", "Jomvu", "Changamwe"],
  "Kisumu": ["Kisumu Central", "Kisumu East", "Kisumu West", "Muhoroni", "Nyando", "Nyakach", "Seme"],
  "Nakuru": ["Nakuru Town East", "Nakuru Town West", "Naivasha", "Gilgil", "Subukia", "Molo", "Njoro", "Kuresoi North", "Kuresoi South", "Bahati", "Rongai"],
  "Kiambu": ["Thika Town", "Ruiru", "Juja", "Gatundu South", "Gatundu North", "Githunguri", "Kiambu", "Kiambaa", "Kabete", "Lari", "Limuru", "Kikuyu"],
  "Uasin Gishu": ["Ainabkoi", "Kapseret", "Kesses", "Soy", "Turbo", "Moiben"],
  "Kakamega": ["Lurambi", "Navakholo", "Mumias East", "Mumias West", "Matungu", "Butere", "Khwisero", "Shinyalu", "Ikolomani", "Malava", "Lugari", "Likuyani"],
  "Machakos": ["Machakos Town", "Masinga", "Yatta", "Kangundo", "Matungulu", "Kathiani", "Mavoko", "Mwala"],
  "Nyeri": ["Nyeri Town", "Kieni", "Mathira", "Othaya", "Mukurweini", "Tetu"],
  "Kilifi": ["Kilifi North", "Kilifi South", "Ganze", "Malindi", "Magarini", "Rabai", "Kaloleni"],
  "Garissa": ["Garissa Township", "Balambala", "Lagdera", "Dadaab", "Fafi", "Ijara"],
  "Bungoma": ["Kanduyi", "Bumula", "Kabuchai", "Sirisia", "Webuye East", "Webuye West", "Kimilili", "Tongaren", "Mt. Elgon"],
  "Meru": ["Imenti Central", "Imenti North", "Imenti South", "Tigania West", "Tigania East", "Igembe North", "Igembe Central", "Igembe South", "Buuri"],
  "Kajiado": ["Kajiado North", "Kajiado Central", "Kajiado East", "Kajiado West", "Kajiado South"]
}
```

### Step 4.2 — Polling Station Lookup Tools

```
[Artifact Type: Source Code] | [File Name: src/tools/polling_stations.py] | [Timestamp: 2026-05-16 10:43 EAT]
```

```python
"""Polling station lookup tools for the Kiongozi locator agent.

Uses a CSV-based dataset of IEBC polling stations with fuzzy matching
on county, constituency, and ward names.
"""

from __future__ import annotations

import csv
import json
import logging
import os
from pathlib import Path
from difflib import get_close_matches

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_stations_cache: list[dict] | None = None
_constituencies_cache: dict[str, list[str]] | None = None


def _load_stations() -> list[dict]:
    """Load and cache the polling stations CSV."""
    global _stations_cache
    if _stations_cache is not None:
        return _stations_cache

    csv_path = _DATA_DIR / "polling_stations.csv"
    if not csv_path.exists():
        logger.error("Polling stations CSV not found at %s", csv_path)
        _stations_cache = []
        return _stations_cache

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        _stations_cache = [row for row in reader]

    logger.info("Loaded %d polling stations", len(_stations_cache))
    return _stations_cache


def _load_constituencies() -> dict[str, list[str]]:
    """Load and cache the constituencies JSON."""
    global _constituencies_cache
    if _constituencies_cache is not None:
        return _constituencies_cache

    json_path = _DATA_DIR / "constituencies.json"
    if not json_path.exists():
        logger.error("Constituencies JSON not found at %s", json_path)
        _constituencies_cache = {}
        return _constituencies_cache

    with open(json_path, "r", encoding="utf-8") as f:
        _constituencies_cache = json.load(f)

    logger.info("Loaded constituencies for %d counties", len(_constituencies_cache))
    return _constituencies_cache


def _fuzzy_match(query: str, options: list[str], cutoff: float = 0.6) -> str | None:
    """Case-insensitive fuzzy match against a list of options."""
    query_lower = query.strip().lower()
    options_lower = {o.lower(): o for o in options}
    # Exact match first
    if query_lower in options_lower:
        return options_lower[query_lower]
    # Fuzzy match
    matches = get_close_matches(query_lower, options_lower.keys(), n=1, cutoff=cutoff)
    if matches:
        return options_lower[matches[0]]
    return None


def find_polling_station(
    county: str = "",
    constituency: str = "",
    ward: str = "",
) -> dict:
    """Search for polling stations in Kenya by administrative area.

    Provide at least one of county, constituency, or ward to search.
    More specific queries (e.g., constituency + ward) return more
    precise results. Names are fuzzy-matched so minor spelling
    differences are tolerated.

    Args:
        county: County name (e.g., "Nairobi", "Mombasa").
        constituency: Constituency name (e.g., "Westlands", "Mvita").
        ward: Ward name for more specific lookup (e.g., "Kangemi").

    Returns:
        dict with keys:
          - stations: list of dicts with name, county, constituency, ward, address
          - total_found: int
          - search_criteria: dict of the search parameters used
    """
    stations = _load_stations()
    all_counties = list({s["county"] for s in stations})
    all_constituencies = list({s["constituency"] for s in stations})
    all_wards = list({s["ward"] for s in stations})

    # Fuzzy-match the inputs
    matched_county = _fuzzy_match(county, all_counties) if county else None
    matched_constituency = _fuzzy_match(constituency, all_constituencies) if constituency else None
    matched_ward = _fuzzy_match(ward, all_wards) if ward else None

    # Filter stations
    results = stations
    if matched_county:
        results = [s for s in results if s["county"].lower() == matched_county.lower()]
    if matched_constituency:
        results = [s for s in results if s["constituency"].lower() == matched_constituency.lower()]
    if matched_ward:
        results = [s for s in results if s["ward"].lower() == matched_ward.lower()]

    formatted = [
        {
            "name": s["station_name"],
            "county": s["county"],
            "constituency": s["constituency"],
            "ward": s["ward"],
            "address": s.get("address", "Address not available"),
        }
        for s in results
    ]

    logger.info(
        "Station search | county=%s constituency=%s ward=%s found=%d",
        matched_county, matched_constituency, matched_ward, len(formatted),
    )

    return {
        "stations": formatted[:10],  # Limit to 10 results
        "total_found": len(formatted),
        "search_criteria": {
            "county": matched_county or county or "(not specified)",
            "constituency": matched_constituency or constituency or "(not specified)",
            "ward": matched_ward or ward or "(not specified)",
        },
    }


def list_constituencies(county: str) -> dict:
    """List all constituencies within a given county.

    Use this tool when a user provides only a county name. Show them
    the available constituencies so they can narrow their search.

    Args:
        county: The county name (e.g., "Nairobi", "Mombasa").

    Returns:
        dict with keys:
          - county: str (matched county name)
          - constituencies: list of str
          - found: bool
    """
    all_data = _load_constituencies()
    all_counties = list(all_data.keys())

    matched = _fuzzy_match(county, all_counties)

    if matched:
        return {
            "county": matched,
            "constituencies": all_data[matched],
            "found": True,
        }

    return {
        "county": county,
        "constituencies": [],
        "found": False,
        "suggestion": (
            f"County '{county}' not found. Available counties include: "
            + ", ".join(sorted(all_counties)[:10]) + "..."
        ),
    }
```

### Step 4.3 — Upgrade Kiongozi Agent

```
[Artifact Type: Source Code] | [File Name: src/agents/kiongozi.py (REPLACE)] | [Timestamp: 2026-05-16 10:44 EAT]
```

```python
"""Kiongozi (Guide) — Polling Station Locator Agent.

Helps citizens find their designated polling station by
county, constituency, or ward — without requiring personal IDs.
"""

from google.adk.agents import LlmAgent
from src.agents.safety import SAFETY_PREAMBLE
from src.tools.polling_stations import find_polling_station, list_constituencies

KIONGOZI_INSTRUCTION = f"""
{SAFETY_PREAMBLE}

## YOUR ROLE
You are Kiongozi (Guide), a polling station locator for Kenyan citizens.
You help citizens find their designated voting location.

## INTERACTION FLOW
1. If the user provides a county only:
   - Call `list_constituencies` to show available constituencies.
   - Ask: "Which constituency are you in?"

2. If the user provides a constituency (with or without county):
   - Call `find_polling_station` with the constituency.
   - Present matching stations in a clean list.

3. If the user provides a ward:
   - Call `find_polling_station` with the ward for the most specific result.

4. If multiple stations are found:
   - Present a numbered list (max 5).
   - Include station name, ward, and address for each.

5. If NO stations are found:
   - Respond: "Samahani, sikupata kituo cha kupigia kura kwa eneo hilo.
     Tafadhali tembelea ofisi ya IEBC iliyo karibu nawe au angalia tovuti ya IEBC."
     ("Sorry, I couldn't find a polling station for that area. Please visit
     your nearest IEBC office or check the IEBC website.")

## RESPONSE FORMAT
When stations are found, respond like this:

"Polling stations in [Constituency], [County]:

1. [Station Name]
   Ward: [Ward]
   Address: [Address]

2. [Station Name]
   ..."

For USSD (short format):
"[Station Name], [Ward] - [Address]"

## PRIVACY RULES — CRITICAL
- NEVER ask for the user's national ID number.
- NEVER ask for the user's voter registration number.
- ONLY use geographic identifiers (county, constituency, ward) for lookup.
- If a user volunteers their ID number, respond: "Sihitaji nambari yako ya
  kitambulisho. Niambie tu kaunti, eneo bunge, au wadi yako."
  ("I don't need your ID number. Just tell me your county, constituency, or ward.")

## ABSOLUTE CONSTRAINTS
- Do NOT provide information about candidates assigned to any station.
- Do NOT express opinions about any political entity.
- Do NOT suggest which station a user "should" go to — only show what's available.

Respond in the same language the user wrote in.
""".strip()

kiongozi = LlmAgent(
    name="kiongozi",
    model="gemini-2.0-flash",
    description=(
        "Polling station locator. Helps citizens find their designated "
        "voting location based on county, constituency, or ward information."
    ),
    instruction=KIONGOZI_INSTRUCTION,
    tools=[find_polling_station, list_constituencies],
    output_key="location_response",
)
```

### Step 4.4 — Polling Station Tool Tests

```
[Artifact Type: Test Suite] | [File Name: tests/test_polling_stations.py] | [Timestamp: 2026-05-16 10:45 EAT]
```

```python
"""Tests for polling station lookup tools."""

import pytest
from src.tools.polling_stations import find_polling_station, list_constituencies


class TestFindPollingStation:
    def test_find_by_county(self):
        result = find_polling_station(county="Nairobi")
        assert result["total_found"] > 0
        assert all(s["county"] == "Nairobi" for s in result["stations"])

    def test_find_by_constituency(self):
        result = find_polling_station(constituency="Westlands")
        assert result["total_found"] > 0
        assert all(s["constituency"] == "Westlands" for s in result["stations"])

    def test_find_by_ward(self):
        result = find_polling_station(ward="Kangemi")
        assert result["total_found"] > 0
        assert result["stations"][0]["ward"] == "Kangemi"

    def test_find_by_county_and_constituency(self):
        result = find_polling_station(county="Nairobi", constituency="Westlands")
        assert result["total_found"] > 0

    def test_not_found(self):
        result = find_polling_station(county="Atlantis")
        assert result["total_found"] == 0

    def test_fuzzy_match_case_insensitive(self):
        result = find_polling_station(county="nairobi")
        assert result["total_found"] > 0

    def test_fuzzy_match_misspelling(self):
        result = find_polling_station(county="Nairob")
        assert result["total_found"] > 0

    def test_results_capped_at_10(self):
        result = find_polling_station(county="Nairobi")
        assert len(result["stations"]) <= 10

    def test_result_has_required_fields(self):
        result = find_polling_station(constituency="Westlands")
        if result["stations"]:
            station = result["stations"][0]
            assert "name" in station
            assert "county" in station
            assert "constituency" in station
            assert "ward" in station
            assert "address" in station


class TestListConstituencies:
    def test_list_nairobi(self):
        result = list_constituencies("Nairobi")
        assert result["found"] is True
        assert "Westlands" in result["constituencies"]

    def test_list_mombasa(self):
        result = list_constituencies("Mombasa")
        assert result["found"] is True
        assert len(result["constituencies"]) > 0

    def test_unknown_county(self):
        result = list_constituencies("Wakanda")
        assert result["found"] is False

    def test_fuzzy_match(self):
        result = list_constituencies("nairob")
        assert result["found"] is True
```

---

## Required Artifacts — Summary

| # | Artifact Type | File Name | Description |
|---|--------------|-----------|-------------|
| 1 | Data File | `data/polling_stations.csv` | 35 seed polling stations across 14 counties |
| 2 | Data File | `data/constituencies.json` | County → constituency mapping for 14 counties |
| 3 | Source Code | `src/tools/polling_stations.py` | `find_polling_station` + `list_constituencies` with fuzzy matching |
| 4 | Source Code | `src/agents/kiongozi.py` (replace) | Full Kiongozi agent with tools and privacy rules |
| 5 | Test Suite | `tests/test_polling_stations.py` | 13 tests for station lookup and constituency listing |

---

## Exit Criteria

- [ ] `data/polling_stations.csv` contains station data for 14+ counties
- [ ] `data/constituencies.json` maps counties to constituencies
- [ ] `find_polling_station(county="Nairobi")` returns stations with full details
- [ ] `find_polling_station(ward="Kangemi")` returns specific station
- [ ] Fuzzy matching works: "nairob" matches "Nairobi"
- [ ] Unknown locations return empty results gracefully (no crash)
- [ ] Kiongozi NEVER asks for national ID or voter registration number
- [ ] `pytest tests/test_polling_stations.py -v` — all 13 tests pass
- [ ] End-to-end: SMS "Where do I vote in Westlands?" → Kiongozi → station list
