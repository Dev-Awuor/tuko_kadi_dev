"""Tests for Agent Hierarchy and Safety."""

import pytest
from src.agents.msaidizi import msaidizi
from src.agents.safety import IMMUTABLE_SAFETY_PREAMBLE

def test_msaidizi_definition():
    assert msaidizi.name == "msaidizi"
    assert len(msaidizi.sub_agents) == 4
    assert "Msaidizi" in msaidizi.instruction

def test_safety_preamble_presence():
    from src.agents.specialists import mwalimu
    assert IMMUTABLE_SAFETY_PREAMBLE in mwalimu.instruction

def test_specialist_names():
    from src.agents.specialists import mwalimu, kiongozi, ukweli, mwenza
    assert mwalimu.name == "mwalimu"
    assert kiongozi.name == "kiongozi"
    assert ukweli.name == "ukweli"
    assert mwenza.name == "mwenza"
