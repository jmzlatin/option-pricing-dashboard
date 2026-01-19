def build_straddle(spot, params):
    """Buy ATM Call + Buy ATM Put"""
    return [
        {'strike': spot, 'premium': params.get('premium_c', 0), 'type': 'Call', 'position': 'Long'},
        {'strike': spot, 'premium': params.get('premium_p', 0), 'type': 'Put', 'position': 'Long'}
    ]
