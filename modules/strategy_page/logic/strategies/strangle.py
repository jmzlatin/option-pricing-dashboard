def build_long_strangle(spot, params):
    """Buy OTM Put + Buy OTM Call"""
    dist = params.get('distance', 5.0)
    return [
        {'strike': spot - dist, 'premium': params.get('premium', 0), 'type': 'Put', 'position': 'Long'},
        {'strike': spot + dist, 'premium': params.get('premium', 0), 'type': 'Call', 'position': 'Long'}
    ]
