import numpy as np

class MonteCarloPricing:
    def __init__(self, S, K, T, r, sigma, simulations=10000, steps=252):
        """
        S: Spot Price
        K: Strike Price
        T: Time to Maturity (Years)
        r: Risk-free Rate
        sigma: Volatility
        simulations: Number of paths to simulate
        steps: Number of time steps (252 = daily for 1 year)
        """
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.simulations = simulations
        self.steps = steps
        self.dt = T / steps

    def simulate_paths(self):
        """
        Generates N random price paths using Geometric Brownian Motion.
        Formula: St = S0 * exp((r - 0.5*sigma^2)t + sigma*sqrt(t)*Z)
        """
        # Set random seed for reproducibility (optional)
        # np.random.seed(42)
        
        # 1. Generate random shocks (Z) for every step of every simulation
        Z = np.random.standard_normal((self.simulations, self.steps))
        
        # 2. Calculate the drift and diffusion components
        drift = (self.r - 0.5 * self.sigma**2) * self.dt
        diffusion = self.sigma * np.sqrt(self.dt) * Z
        
        # 3. Calculate daily returns (exponential)
        daily_returns = np.exp(drift + diffusion)
        
        # 4. Initialize price matrix
        price_paths = np.zeros((self.simulations, self.steps + 1))
        price_paths[:, 0] = self.S
        
        # 5. Accumulate returns to get prices
        for t in range(1, self.steps + 1):
            price_paths[:, t] = price_paths[:, t-1] * daily_returns[:, t-1]
            
        return price_paths

    def calculate_price(self, price_paths, option_type='Call'):
        """
        Calculates option price based on the average payoff at expiration.
        """
        # Get prices at the final step (expiration)
        terminal_prices = price_paths[:, -1]
        
        if option_type == 'Call':
            payoffs = np.maximum(terminal_prices - self.K, 0)
        else:
            payoffs = np.maximum(self.K - terminal_prices, 0)
            
        # Discount the average payoff back to today
        option_price = np.exp(-self.r * self.T) * np.mean(payoffs)
        
        return option_price