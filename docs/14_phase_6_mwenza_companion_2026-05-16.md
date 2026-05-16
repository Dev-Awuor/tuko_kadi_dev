---
title: "Phase 6 — Mwenza Election Day Companion"
author: "TukoKadi Development Team"
date: "2026-05-16"
version: "1.0"
---

# Phase 6 — Mwenza: Election Day Companion (USSD-Optimized)

**Document ID:** SYM-IMPL-P6  
**Created:** 2026-05-16T10:53:00+03:00  
**Last Modified:** 2026-05-16T10:53:00+03:00  
**Phase Status:** ☐ Pending

---

## Phase Objective

Build the election day step-by-step content database, implement channel-aware tools that respect USSD/SMS character limits, create a voter-rights-at-station troubleshooting tool, and upgrade Mwenza from a stub to a fully functional election day companion optimized for feature phone users.

---

## Dependencies & Blockers

| Dependency | Type | Resolution |
|-----------|------|-----------|
| Phase 2 complete | **BLOCKER** | Msaidizi must route election day queries to Mwenza |
| Channel formatting (Phase 1) | Required | `formatter.py` must handle USSD CON/END and SMS limits |

---

## Action Items

### Step 6.1 — Election Day Content Database

```
[Artifact Type: Data File] | [File Name: data/election_day_steps.json] | [Timestamp: 2026-05-16 10:54 EAT]
```

```json
[
  {
    "step": 1,
    "title_en": "Prepare Before You Leave",
    "title_sw": "Jiandae Kabla ya Kuondoka",
    "details_en": "Carry your ORIGINAL National ID card or valid Kenyan passport. Photocopies, waiting cards, and police abstracts are NOT accepted. Dress comfortably and eat before you go.",
    "details_sw": "Beba kitambulisho chako cha ASILI au pasipoti halali ya Kenya. Nakala, kadi za kusubiri, na hati za polisi HAZIKUBALIKI. Vaa vizuri na kula kabla ya kwenda.",
    "ussd_en": "Bring original ID/passport. No photocopies accepted.",
    "ussd_sw": "Beba kitambulisho asili. Nakala hazikubaliki.",
    "legal_reference": "Elections Act 2011, Section 5(2)",
    "common_questions": ["Can I use a waiting card?", "What if I lost my ID?"]
  },
  {
    "step": 2,
    "title_en": "Arrive at Your Polling Station",
    "title_sw": "Fika Kituo Chako cha Kupigia Kura",
    "details_en": "Go to the specific polling station where you registered. You CANNOT vote at a different station. Stations open at 6:00 AM and close at 5:00 PM. Arrive early to avoid long queues.",
    "details_sw": "Nenda kituo mahususi ulichojiandikisha. HUWEZI kupiga kura kituo kingine. Vituo vinafunguka saa 12 asubuhi na kufunga saa 11 jioni. Fika mapema.",
    "ussd_en": "Go to YOUR station. Open 6AM-5PM. Arrive early.",
    "ussd_sw": "Nenda kituo CHAKO. Saa 12 asubuhi-11 jioni. Fika mapema.",
    "legal_reference": "Elections Act 2011, Section 6",
    "common_questions": ["What time should I arrive?", "What if I go to wrong station?"]
  },
  {
    "step": 3,
    "title_en": "Join the Queue",
    "title_sw": "Ingia Foleni",
    "details_en": "Join the queue in an orderly manner. Cutting the line is an offense. Priority is given to pregnant women, elderly, persons with disabilities, and nursing mothers. If you are in the queue by 5:00 PM, you WILL be allowed to vote.",
    "details_sw": "Ingia foleni kwa utaratibu. Kuruka foleni ni kosa. Kipaumbele kinatolewa kwa wajawazito, wazee, walemavu, na wanaonyonyesha. Ukiwa folenini saa 11 jioni, UTARUHUSIWA kupiga kura.",
    "ussd_en": "Queue orderly. Priority: pregnant, elderly, disabled. In queue by 5PM = you WILL vote.",
    "ussd_sw": "Foleni kwa utaratibu. Kipaumbele: wajawazito, wazee, walemavu. Folenini saa 11 = UTAPIGA kura.",
    "legal_reference": "IEBC Election Guidelines",
    "common_questions": ["What if I arrive at 4:55 PM?", "Can someone hold my place?"]
  },
  {
    "step": 4,
    "title_en": "Identification & Verification",
    "title_sw": "Utambulisho na Uthibitisho",
    "details_en": "Present your original ID to the presiding officer. Your fingerprint will be scanned using the KIEMS kit for biometric verification. Your name will be checked against the voter register.",
    "details_sw": "Onyesha kitambulisho chako asili kwa afisa msimamizi. Alama ya kidole itaskanwa kwa KIEMS. Jina lako litathibitishwa kwenye daftari la wapiga kura.",
    "ussd_en": "Show ID. Fingerprint scan on KIEMS kit. Name checked on register.",
    "ussd_sw": "Onyesha kitambulisho. Kidole kitaskanwa. Jina litathibitishwa.",
    "legal_reference": "Elections Act 2011, Section 44",
    "common_questions": ["What is KIEMS?", "What if my fingerprint doesn't match?"]
  },
  {
    "step": 5,
    "title_en": "Receive Your Ballot Papers",
    "title_sw": "Pokea Karatasi za Kura",
    "details_en": "You will receive up to 6 ballot papers in a general election: President, Governor, Senator, Women Representative, Member of National Assembly, and County Assembly Ward Representative. Each is a different color.",
    "details_sw": "Utapokea hadi karatasi 6 za kura: Rais, Gavana, Seneta, Mbunge wa Wanawake, Mbunge wa Bunge la Taifa, na Mbunge wa Wadi. Kila moja ina rangi tofauti.",
    "ussd_en": "You get 6 ballots: President, Governor, Senator, Women Rep, MP, Ward Rep. Each different color.",
    "ussd_sw": "Karatasi 6: Rais, Gavana, Seneta, Wanawake, Mbunge, Wadi. Rangi tofauti.",
    "legal_reference": "Constitution of Kenya 2010, Articles 97-101, 138, 180",
    "common_questions": ["Why 6 ballot papers?", "What if I don't get all 6?"]
  },
  {
    "step": 6,
    "title_en": "Mark Your Ballot",
    "title_sw": "Weka Alama Kwenye Kura",
    "details_en": "Go to the private voting booth. Use the stamp or pen provided to mark your chosen candidate on EACH ballot paper. Mark only ONE candidate per ballot. Do NOT write anything else on the ballot — it will be spoiled.",
    "details_sw": "Nenda kibandani cha faragha. Tumia muhuri au kalamu kupiga alama kwa mgombea uliyemchagua KILA karatasi. Chagua mgombea MMOJA tu kwa kila karatasi. USIANDIKE kitu kingine.",
    "ussd_en": "Go to booth. Stamp/mark ONE candidate per ballot. Don't write anything else.",
    "ussd_sw": "Nenda kibandani. Alama mgombea MMOJA kwa kila kura. Usiandike kingine.",
    "legal_reference": "Elections Act 2011, Section 16",
    "common_questions": ["What if I make a mistake?", "Can I take a photo of my ballot?"]
  },
  {
    "step": 7,
    "title_en": "Cast Your Ballot",
    "title_sw": "Tupa Kura Yako",
    "details_en": "Fold each ballot paper and deposit it in the CORRECT ballot box. Each box is labeled and color-coded to match the ballot. Make sure you put each ballot in the right box.",
    "details_sw": "Kunja kila karatasi na uitupe kwenye sanduku SAHIHI la kura. Kila sanduku lina lebo na rangi inayolingana na karatasi. Hakikisha kila kura inaingia sanduku sahihi.",
    "ussd_en": "Fold ballots. Put each in the CORRECT color-coded box.",
    "ussd_sw": "Kunja kura. Tupa kila moja sanduku SAHIHI la rangi yake.",
    "legal_reference": "Elections Act 2011, Section 16",
    "common_questions": ["What if I put ballot in wrong box?", "How many boxes are there?"]
  },
  {
    "step": 8,
    "title_en": "Ink Marking",
    "title_sw": "Kuwekwa Wino",
    "details_en": "After voting, your finger will be marked with indelible ink. This prevents double voting. The ink cannot be washed off for several days.",
    "details_sw": "Baada ya kupiga kura, kidole chako kitawekwa wino usiofutika. Hii inazuia kupiga kura mara mbili. Wino hauondoki kwa siku kadhaa.",
    "ussd_en": "Finger marked with permanent ink to prevent double voting.",
    "ussd_sw": "Kidole kitawekwa wino kudhibiti kupiga kura mara mbili.",
    "legal_reference": "Elections Act 2011, Section 44",
    "common_questions": ["Can I refuse the ink?", "Which finger is marked?"]
  },
  {
    "step": 9,
    "title_en": "Leave the Polling Station",
    "title_sw": "Ondoka Kituoni",
    "details_en": "After voting, leave the polling station area promptly. Do not loiter or attempt to influence other voters. Campaigning within 400 meters of a polling station is illegal on election day.",
    "details_sw": "Baada ya kupiga kura, ondoka eneo la kituo haraka. Usizurure au kujaribu kushawishi wapiga kura wengine. Kampeni ndani ya mita 400 za kituo ni kinyume cha sheria siku ya uchaguzi.",
    "ussd_en": "Leave after voting. No campaigning within 400m of station.",
    "ussd_sw": "Ondoka baada ya kupiga kura. Kampeni ndani ya mita 400 ni marufuku.",
    "legal_reference": "Elections Act 2011, Section 14",
    "common_questions": ["Can I stay to watch counting?", "When are results announced?"]
  }
]
```

### Step 6.2 — Voter Rights at Station Database

```
[Artifact Type: Data File] | [File Name: data/voter_rights_scenarios.json] | [Timestamp: 2026-05-16 10:55 EAT]
```

```json
[
  {
    "scenario": "name not on register",
    "keywords": ["not on register", "name missing", "jina halipo", "can't find my name"],
    "right_en": "Ask the presiding officer to check the supplementary register. If your name is confirmed in the supplementary register, you will be allowed to vote.",
    "right_sw": "Mwambie afisa msimamizi akague daftari la nyongeza. Jina lako likithibitishwa, utaruhusiwa kupiga kura.",
    "action_en": "Speak to the presiding officer calmly. If unresolved, file a complaint with the IEBC.",
    "action_sw": "Zungumza na afisa msimamizi kwa utulivu. Isipomalizika, wasilisha malalamiko kwa IEBC.",
    "legal_basis": "Elections Act 2011, Section 44"
  },
  {
    "scenario": "voter intimidation",
    "keywords": ["intimidation", "threatened", "intimidate", "vitisho", "threatened"],
    "right_en": "Voter intimidation is a criminal offense. You have the right to vote freely without pressure from anyone.",
    "right_sw": "Kutisha wapiga kura ni kosa la jinai. Una haki ya kupiga kura kwa uhuru bila shinikizo kutoka kwa mtu yeyote.",
    "action_en": "Report immediately to the presiding officer, police officers at the station, or call the IEBC hotline.",
    "action_sw": "Ripoti mara moja kwa afisa msimamizi, polisi kituoni, au piga simu IEBC.",
    "legal_basis": "Elections Act 2011, Section 12A"
  },
  {
    "scenario": "station not open",
    "keywords": ["station closed", "not open", "haijafunguliwa", "closed"],
    "right_en": "Polling stations must open at 6:00 AM. If a station has not opened, the presiding officer must explain the delay. Voting may be extended to compensate for lost time.",
    "right_sw": "Vituo lazima vifunguke saa 12 asubuhi. Kama kituo hakijafunguka, afisa msimamizi lazima aeleze sababu. Muda wa kupiga kura unaweza kuongezwa.",
    "action_en": "Wait at the station and ask the presiding officer for an explanation. Contact the IEBC constituency office.",
    "action_sw": "Subiri kituoni na uliza afisa msimamizi. Wasiliana na ofisi ya IEBC ya eneo bunge.",
    "legal_basis": "IEBC Election Guidelines"
  },
  {
    "scenario": "long queue",
    "keywords": ["long queue", "waiting long", "foleni ndefu", "too many people"],
    "right_en": "If you are in the queue when the station closes at 5:00 PM, you have the legal right to vote. No one can turn you away.",
    "right_sw": "Ukiwa folenini kituo kinapofungwa saa 11 jioni, una haki ya kisheria kupiga kura. Hakuna mtu anayeweza kukukataa.",
    "action_en": "Stay in the queue. The presiding officer must allow everyone in the queue at 5:00 PM to vote.",
    "action_sw": "Kaa folenini. Afisa msimamizi lazima aruhusu kila mtu aliye folenini saa 11 jioni kupiga kura.",
    "legal_basis": "Elections Act 2011, Section 6"
  },
  {
    "scenario": "ballot paper mistake",
    "keywords": ["mistake on ballot", "wrong mark", "spoiled ballot", "nimekosea"],
    "right_en": "If you make a mistake on your ballot BEFORE putting it in the box, you can request a replacement from the presiding officer. The spoiled ballot will be cancelled.",
    "right_sw": "Ukikosea kura yako KABLA ya kuitupa sandukuni, unaweza kuomba karatasi mpya kutoka kwa afisa msimamizi. Kura iliyoharibika itafutwa.",
    "action_en": "Immediately inform the presiding officer before depositing the ballot. Do not put a spoiled ballot in the box.",
    "action_sw": "Mwambie afisa msimamizi mara moja kabla ya kutupa kura. Usitupe kura iliyoharibika sandukuni.",
    "legal_basis": "Elections Act 2011, Section 16"
  },
  {
    "scenario": "disability assistance",
    "keywords": ["disability", "blind", "wheelchair", "ulemavu", "kipofu", "msaada"],
    "right_en": "Voters with disabilities have the right to be assisted by a person of their choice or by the presiding officer. Accessible facilities should be provided.",
    "right_sw": "Wapiga kura wenye ulemavu wana haki ya kusaidiwa na mtu wanayemchagua au afisa msimamizi. Vifaa vinavyofikika vinapaswa kutolewa.",
    "action_en": "Inform the presiding officer of your needs. You may bring one assistant of your choice into the booth.",
    "action_sw": "Mjulishe afisa msimamizi mahitaji yako. Unaweza kuleta msaidizi mmoja unayemchagua kibandani.",
    "legal_basis": "Elections Act 2011, Section 8"
  }
]
```

### Step 6.3 — Election Day Tools

```
[Artifact Type: Source Code] | [File Name: src/tools/election_day.py] | [Timestamp: 2026-05-16 10:56 EAT]
```

```python
"""Election day guidance tools for the Mwenza companion agent.

Provides step-by-step voting procedures and voter rights information,
with channel-aware content (full text vs USSD-condensed).
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

_DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
_steps_cache: list[dict] | None = None
_rights_cache: list[dict] | None = None


def _load_steps() -> list[dict]:
    global _steps_cache
    if _steps_cache is not None:
        return _steps_cache
    path = _DATA_DIR / "election_day_steps.json"
    if not path.exists():
        _steps_cache = []
        return _steps_cache
    with open(path, "r", encoding="utf-8") as f:
        _steps_cache = json.load(f)
    return _steps_cache


def _load_rights() -> list[dict]:
    global _rights_cache
    if _rights_cache is not None:
        return _rights_cache
    path = _DATA_DIR / "voter_rights_scenarios.json"
    if not path.exists():
        _rights_cache = []
        return _rights_cache
    with open(path, "r", encoding="utf-8") as f:
        _rights_cache = json.load(f)
    return _rights_cache


def get_election_day_step(step_number: int, language: str = "en") -> dict:
    """Get detailed information about a specific election day step.

    Use this tool to guide a voter through election day. There are 9
    steps from preparation to leaving the station.

    Args:
        step_number: Step number (1-9).
        language: Language code - "en" for English, "sw" for Swahili.

    Returns:
        dict with step details including full text and USSD-short version.
    """
    steps = _load_steps()

    if step_number < 1 or step_number > 9:
        return {
            "step_number": step_number,
            "found": False,
            "error": f"Step {step_number} does not exist. Valid steps are 1-9.",
            "total_steps": 9,
        }

    step = steps[step_number - 1]
    lang = "sw" if language.lower().startswith("sw") else "en"

    return {
        "step_number": step["step"],
        "found": True,
        "title": step[f"title_{lang}"],
        "details": step[f"details_{lang}"],
        "ussd_short": step[f"ussd_{lang}"],
        "legal_reference": step["legal_reference"],
        "common_questions": step["common_questions"],
        "total_steps": 9,
        "has_next": step_number < 9,
        "has_previous": step_number > 1,
    }


def get_voter_rights_at_station(scenario: str) -> dict:
    """Look up voter rights for a specific scenario at the polling station.

    Use this tool when a voter describes a problem they are experiencing
    or anticipating at the polling station.

    Args:
        scenario: Description of the situation. Examples:
                 "my name is not on the register"
                 "someone is intimidating voters"
                 "I made a mistake on my ballot"
                 "I have a disability and need help"

    Returns:
        dict with the voter's rights, recommended action, and legal basis.
    """
    rights = _load_rights()
    scenario_lower = scenario.lower()

    for right in rights:
        if any(kw in scenario_lower for kw in right["keywords"]):
            return {
                "scenario": right["scenario"],
                "found": True,
                "right_en": right["right_en"],
                "right_sw": right["right_sw"],
                "action_en": right["action_en"],
                "action_sw": right["action_sw"],
                "legal_basis": right["legal_basis"],
            }

    return {
        "scenario": scenario,
        "found": False,
        "message_en": (
            "I don't have specific guidance for that situation. "
            "Please speak to the presiding officer at your polling station "
            "or contact the IEBC hotline."
        ),
        "message_sw": (
            "Sina mwongozo mahususi kwa hali hiyo. Tafadhali zungumza na "
            "afisa msimamizi kituoni chako au piga simu IEBC."
        ),
    }
```

### Step 6.4 — Upgrade Mwenza Agent

```
[Artifact Type: Source Code] | [File Name: src/agents/mwenza.py (REPLACE)] | [Timestamp: 2026-05-16 10:57 EAT]
```

```python
"""Mwenza (Companion) — Election Day Companion Agent.

USSD-optimized election day guide. Provides step-by-step voting
guidance and troubleshooting for voter rights issues at the station.
"""

from google.adk.agents import LlmAgent
from src.agents.safety import SAFETY_PREAMBLE
from src.tools.election_day import get_election_day_step, get_voter_rights_at_station

MWENZA_INSTRUCTION = f"""
{SAFETY_PREAMBLE}

## YOUR ROLE
You are Mwenza (Companion), an election day guide for Kenyan voters.
You walk citizens through every step of voting day.

## CHANNEL-AWARE RESPONSES
Check the session state for the channel and adapt your response:

FOR USSD (channel == "ussd"):
- Use the "ussd_short" field from tool results (already condensed)
- Maximum 182 characters total including CON/END prefix
- Use numbered menu format for navigation
- Keep language extremely concise

FOR SMS (channel == "sms"):
- Maximum 160 characters
- One key instruction per message
- Plain text, no formatting

FOR WhatsApp (channel == "whatsapp"):
- Use full "details" field from tool results
- Use emoji step markers (1️⃣ 2️⃣ etc.)
- Include legal references
- Up to 1000 characters

## STEP-BY-STEP FLOW
When a user asks about election day generally:
1. Start with Step 1 (Preparation)
2. After each step, offer: "Next step?" / "Hatua inayofuata?"
3. If user says "next" or a number, show that step
4. Use `get_election_day_step` for each step

When a user describes a PROBLEM at the station:
1. Use `get_voter_rights_at_station` with their scenario
2. Explain their rights clearly
3. Tell them what action to take
4. Cite the legal basis

## LANGUAGE
- Detect user language and respond accordingly
- For `get_election_day_step`, pass language="sw" for Swahili users
- Provide both English and Swahili for critical rights information

## ABSOLUTE CONSTRAINTS
- NEVER suggest which candidate or party to vote for
- NEVER discuss results, predictions, or opinion polls
- All information must cite Elections Act 2011 or IEBC procedures
- If asked about something outside election day procedures, say:
  "Ninaweza kusaidia na mwongozo wa siku ya uchaguzi tu."
  ("I can only help with election day guidance.")
""".strip()

mwenza = LlmAgent(
    name="mwenza",
    model="gemini-2.0-flash",
    description=(
        "Election day companion. Provides step-by-step guidance for "
        "voting day procedures, optimized for USSD and SMS with strict "
        "character limits. Covers preparation, queuing, ballot marking, "
        "voter rights at the station, and troubleshooting."
    ),
    instruction=MWENZA_INSTRUCTION,
    tools=[get_election_day_step, get_voter_rights_at_station],
    output_key="election_day_response",
)
```

### Step 6.5 — Election Day Tool Tests

```
[Artifact Type: Test Suite] | [File Name: tests/test_election_day.py] | [Timestamp: 2026-05-16 10:58 EAT]
```

```python
"""Tests for election day tools."""

import pytest
from src.tools.election_day import get_election_day_step, get_voter_rights_at_station


class TestElectionDaySteps:
    def test_step_1_exists(self):
        r = get_election_day_step(1)
        assert r["found"] is True
        assert r["step_number"] == 1

    def test_step_9_exists(self):
        r = get_election_day_step(9)
        assert r["found"] is True
        assert r["has_next"] is False

    def test_step_0_invalid(self):
        r = get_election_day_step(0)
        assert r["found"] is False

    def test_step_10_invalid(self):
        r = get_election_day_step(10)
        assert r["found"] is False

    def test_english_language(self):
        r = get_election_day_step(1, language="en")
        assert "ID" in r["details"] or "passport" in r["details"]

    def test_swahili_language(self):
        r = get_election_day_step(1, language="sw")
        assert "kitambulisho" in r["details"].lower()

    def test_ussd_short_exists(self):
        r = get_election_day_step(1)
        assert "ussd_short" in r
        assert len(r["ussd_short"]) < 160

    def test_has_legal_reference(self):
        r = get_election_day_step(1)
        assert r["legal_reference"], "Steps must cite legal basis"

    def test_step_5_mentions_6_ballots(self):
        r = get_election_day_step(5, language="en")
        assert "6" in r["details"]

    def test_navigation_flags(self):
        r1 = get_election_day_step(1)
        assert r1["has_previous"] is False
        assert r1["has_next"] is True
        r5 = get_election_day_step(5)
        assert r5["has_previous"] is True
        assert r5["has_next"] is True


class TestVoterRights:
    def test_name_not_on_register(self):
        r = get_voter_rights_at_station("my name is not on the register")
        assert r["found"] is True
        assert "supplementary" in r["right_en"].lower()

    def test_intimidation(self):
        r = get_voter_rights_at_station("someone is threatening voters")
        assert r["found"] is True
        assert "criminal" in r["right_en"].lower()

    def test_ballot_mistake(self):
        r = get_voter_rights_at_station("I made a mistake on my ballot")
        assert r["found"] is True

    def test_disability(self):
        r = get_voter_rights_at_station("I am blind and need help voting")
        assert r["found"] is True
        assert "assisted" in r["right_en"].lower()

    def test_unknown_scenario(self):
        r = get_voter_rights_at_station("aliens have landed at the station")
        assert r["found"] is False

    def test_swahili_keywords(self):
        r = get_voter_rights_at_station("jina halipo kwenye daftari")
        assert r["found"] is True
```

---

## Required Artifacts — Summary

| # | Artifact Type | File Name | Description |
|---|--------------|-----------|-------------|
| 1 | Data File | `data/election_day_steps.json` | 9 bilingual steps (EN/SW) with USSD-short variants |
| 2 | Data File | `data/voter_rights_scenarios.json` | 6 troubleshooting scenarios with rights and actions |
| 3 | Source Code | `src/tools/election_day.py` | `get_election_day_step` + `get_voter_rights_at_station` |
| 4 | Source Code | `src/agents/mwenza.py` (replace) | Full agent with channel-aware formatting rules |
| 5 | Test Suite | `tests/test_election_day.py` | 16 tests for steps, rights, languages, navigation |

---

## Exit Criteria

- [ ] `data/election_day_steps.json` contains 9 steps in English and Swahili with USSD-short variants
- [ ] `data/voter_rights_scenarios.json` contains 6 scenarios with bilingual content
- [ ] `get_election_day_step(1, "en")` returns English preparation instructions
- [ ] `get_election_day_step(1, "sw")` returns Swahili preparation instructions
- [ ] USSD-short text is under 160 chars for every step
- [ ] `get_voter_rights_at_station("name not on register")` returns supplementary register guidance
- [ ] Unknown scenarios return graceful fallback (not crash)
- [ ] `pytest tests/test_election_day.py -v` — all 16 tests pass
- [ ] End-to-end: SMS "What do I do on election day?" → Mwenza → Step 1 with legal reference
