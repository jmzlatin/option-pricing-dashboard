from modules.strategy_page.logic.strategies.straddle import build_straddle
from modules.strategy_page.logic.strategies.iron_condor import build_iron_condor
from modules.strategy_page.logic.strategies.spreads import build_bull_call_spread, build_bear_put_spread
from modules.strategy_page.logic.strategies.strangle import build_long_strangle

def build_strategy_legs(strategy_type, spot, params):
    """
    Dispatcher function: Routes the request to the correct specific strategy file.
    """
    strategies = {
        "Straddle": build_straddle,
        "Iron Condor": build_iron_condor,
        "Bull Call Spread": build_bull_call_spread,
        "Bear Put Spread": build_bear_put_spread,
        "Long Strangle": build_long_strangle
    }
    
    builder_func = strategies.get(strategy_type)
    
    if builder_func:
        return builder_func(spot, params)
    else:
        return []