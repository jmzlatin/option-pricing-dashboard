def build_bull_call_spread(spot, params):
    """Buy ATM Call + Sell OTM Call"""
    width = params.get('width', 5.0)
    return [
        {'strike': spot, 'premium': params.get('premium_long', 0), 'type': 'Call', 'position': 'Long'},
        {'strike': spot + width, 'premium': params.get('premium_short', 0), 'type': 'Call', 'position': 'Short'}
    ]

def build_bear_put_spread(spot, params):
    """Buy ATM Put + Sell OTM Put"""
    width = params.get('width', 5.0)
    return [
        {'strike': spot, 'premium': params.get('premium_long', 0), 'type': 'Put', 'position': 'Long'},
        {'strike': spot - width, 'premium': params.get('premium_short', 0), 'type': 'Put', 'position': 'Short'}
    ]
