import numpy as np

class BinomialModel:
    def __init__(self, S, K, T, r, sigma, steps=100):
        self.S = S              # Spot Price
        self.K = K              # Strike Price
        self.T = T              # Time to Maturity
        self.r = r              # Risk-free Rate
        self.sigma = sigma      # Volatility
        self.steps = steps      # Number of steps in the tree

    def calculate_price(self, option_type='call', american=True):
        dt = self.T / self.steps
        u = np.exp(self.sigma * np.sqrt(dt))  # Up factor
        d = 1 / u                             # Down factor
        p = (np.exp(self.r * dt) - d) / (u - d)  # Risk-neutral probability

        # Initialize asset prices at maturity (the end of the tree)
        # We compute the bottom-most node to the top-most node
        asset_prices = self.S * (d ** np.arange(self.steps, -1, -1)) * (u ** np.arange(0, self.steps + 1, 1))

        # Initialize option values at maturity
        if option_type == 'call':
            option_values = np.maximum(0, asset_prices - self.K)
        else:
            option_values = np.maximum(0, self.K - asset_prices)

        # Backward induction: Step back from maturity to t=0
        for i in range(self.steps - 1, -1, -1):
            # Calculate "continuation value" (holding the option)
            continuation_value = np.exp(-self.r * dt) * (p * option_values[1:] + (1 - p) * option_values[:-1])
            
            # Recalculate asset prices for this earlier time step
            asset_prices = self.S * (d ** np.arange(i, -1, -1)) * (u ** np.arange(0, i + 1, 1))

            if american:
                # Check for early exercise (Intrinsic Value vs Continuation Value)
                if option_type == 'call':
                    exercise_value = np.maximum(0, asset_prices - self.K)
                else:
                    exercise_value = np.maximum(0, self.K - asset_prices)
                option_values = np.maximum(continuation_value, exercise_value)
            else:
                # European style (no early exercise)
                option_values = continuation_value

        return option_values[0]