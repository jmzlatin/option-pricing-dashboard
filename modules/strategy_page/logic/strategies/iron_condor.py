def build_iron_condor(spot, params):
    """Sell Inner Strangle, Buy Outer Wings"""
    width = params.get('width', 5.0)
    return [
        # Put Wing (Bull Put Spread)
        {'strike': spot - width, 'premium': params.get('premium_short', 0), 'type': 'Put', 'position': 'Short'},
        {'strike': spot - (2*width), 'premium': params.get('premium_long', 0), 'type': 'Put', 'position': 'Long'},
        # Call Wing (Bear Call Spread)
        {'strike': spot + width, 'premium': params.get('premium_short', 0), 'type': 'Call', 'position': 'Short'},
        {'strike': spot + (2*width), 'premium': params.get('premium_long', 0), 'type': 'Call', 'position': 'Long'}
    ]
