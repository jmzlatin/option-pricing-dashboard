import pytest
from modules.strategy_page.logic.builder import build_strategy_legs

SPOT_PRICE = 100.0
PARAMS = {
    'width': 10.0,
    'premium_long': 2.0,
    'premium_short': 1.0,
    'premium_c': 3.0,
    'premium_p': 3.0,
    'distance': 5.0,
    'premium': 1.5
}

def test_build_straddle():
    legs = build_strategy_legs("Straddle", SPOT_PRICE, PARAMS)
    assert len(legs) == 2
    assert legs[0]['type'] == 'Call'

def test_build_iron_condor():
    legs = build_strategy_legs("Iron Condor", SPOT_PRICE, PARAMS)
    assert len(legs) == 4
    # Check that we have both calls and puts
    types = [l['type'] for l in legs]
    assert 'Call' in types
    assert 'Put' in types

def test_build_bull_call_spread():
    legs = build_strategy_legs("Bull Call Spread", SPOT_PRICE, PARAMS)
    assert len(legs) == 2
    # Should be Long (Buy) and Short (Sell)
    positions = [l['position'] for l in legs]
    assert 'Long' in positions
    assert 'Short' in positions

def test_build_unknown_strategy():
    legs = build_strategy_legs("Unknown Strategy", SPOT_PRICE, PARAMS)
    assert legs == []
