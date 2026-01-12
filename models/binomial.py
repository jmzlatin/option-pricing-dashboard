import numpy as np

class BinomialModel:
    def __init__(self, time_to_maturity, strike, current_price, volatility, interest_rate, steps=50):
        self.T = time_to_maturity
        self.K = strike
        self.S = current_price
        self.sigma = volatility
        self.r = interest_rate
        self.N = int(steps)

    def calculate_prices(self):
        """
        Calculates American Call and Put prices using a Binomial Tree (CRR Method).
        """
        dt = self.T / self.N
        u = np.exp(self.sigma * np.sqrt(dt))  # Up factor
        d = 1 / u                             # Down factor
        p = (np.exp(self.r * dt) - d) / (u - d) # Risk-neutral probability

        # 1. Initialize asset prices at maturity
        # Vectorized calculation for speed
        asset_prices = self.S * (u ** np.arange(self.N, -1, -1)) * (d ** np.arange(0, self.N + 1, 1))

        # 2. Initialize option values at maturity (Payoff)
        call_values = np.maximum(asset_prices - self.K, 0)
        put_values = np.maximum(self.K - asset_prices, 0)

        # 3. Backward Induction
        discount_factor = np.exp(-self.r * dt)
        
        for i in range(self.N - 1, -1, -1):
            # Calculate continuation value
            call_values = discount_factor * (p * call_values[:-1] + (1 - p) * call_values[1:])
            put_values = discount_factor * (p * put_values[:-1] + (1 - p) * put_values[1:])
            
            # Recalculate asset prices for this step
            asset_prices = self.S * (u ** np.arange(i, -1, -1)) * (d ** np.arange(0, i + 1, 1))

            # Check for Early Exercise (American Option feature)
            call_values = np.maximum(asset_prices - self.K, call_values)
            put_values = np.maximum(self.K - asset_prices, put_values)

        return call_values[0], put_values[0]