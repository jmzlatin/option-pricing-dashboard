import numpy as np
from scipy.stats import norm

class BlackScholes:
    def __init__(self, time_to_maturity, strike, current_price, volatility, interest_rate):
        self.T = time_to_maturity
        self.K = strike
        self.S = current_price
        self.sigma = volatility
        self.r = interest_rate

    def calculate_prices(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)

        call_price = self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        put_price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)

        return call_price, put_price

    def calculate_greeks(self):
        d1 = (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))
        d2 = d1 - self.sigma * np.sqrt(self.T)

        # Delta
        call_delta = norm.cdf(d1)
        put_delta = norm.cdf(d1) - 1

        # Gamma (Same for Call & Put)
        gamma = norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

        # Vega (Same for Call & Put)
        # Divided by 100 to represent value change per 1% change in volatility
        vega = self.S * norm.pdf(d1) * np.sqrt(self.T) / 100

        # Theta (Time Decay)
        # Divided by 365 to represent value change per 1 day passing
        theta_call = (- (self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T)) 
                      - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)) / 365
        
        theta_put = (- (self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T)) 
                     + self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)) / 365

        # Rho (Interest Rate Sensitivity)
        # Divided by 100 to represent value change per 1% change in rate
        rho_call = self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2) / 100
        rho_put = -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2) / 100

        return {
            "call": {"delta": call_delta, "gamma": gamma, "vega": vega, "theta": theta_call, "rho": rho_call},
            "put": {"delta": put_delta, "gamma": gamma, "vega": vega, "theta": theta_put, "rho": rho_put}
        }