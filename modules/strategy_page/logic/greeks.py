from models.bs_model import BlackScholes

def calculate_net_greeks(legs, spot, T, r, sigma):
    """
    Calculates the aggregated Greeks for a multi-leg strategy.
    
    Args:
        legs (list): List of leg dictionaries.
        spot (float): Current underlying price.
        T (float): Time to maturity in years.
        r (float): Risk-free rate (decimal).
        sigma (float): Volatility (decimal).
        
    Returns:
        dict: Net Delta, Gamma, Theta, Vega, Rho.
    """
    net_greeks = {
        "delta": 0.0,
        "gamma": 0.0,
        "theta": 0.0,
        "vega": 0.0,
        "rho": 0.0
    }
    
    for leg in legs:
        # 1. Initialize BS Model for this leg
        # Note: 'Call' or 'Put' determines the price/greek calculation
        bs = BlackScholes(T, leg['strike'], spot, sigma, r)
        greeks = bs.calculate_greeks()
        
        # 2. Get the specific type (Call greeks or Put greeks)
        type_key = leg['type'].lower() # 'call' or 'put'
        leg_greeks = greeks.get(type_key)
        
        if not leg_greeks:
            continue # Skip if invalid type (e.g. Stock)

        # 3. Adjust for Position (Long = +, Short = -)
        multiplier = 1.0 if leg['position'] == 'Long' else -1.0
        
        net_greeks['delta'] += leg_greeks['delta'] * multiplier
        net_greeks['gamma'] += leg_greeks['gamma'] * multiplier
        net_greeks['theta'] += leg_greeks['theta'] * multiplier
        net_greeks['vega']  += leg_greeks['vega']  * multiplier
        net_greeks['rho']   += leg_greeks['rho']   * multiplier
        
    return net_greeks
