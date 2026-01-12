import streamlit as st
import numpy as np
from models.strategies import plot_strategy

st.set_page_config(page_title="Options Strategy Builder", layout="wide")

st.title("🏗️ Options Strategy Builder")

# --- Sidebar: Strategy Setup ---
st.sidebar.header("Strategy Settings")
spot_price = st.sidebar.number_input("Current Spot Price", value=100.0, step=1.0)

# Strategy Selector
strategy_type = st.sidebar.selectbox(
    "Select Strategy", 
    ["Straddle", "Long Strangle", "Bull Call Spread", "Bear Put Spread", "Iron Condor", "Butterfly Spread", "Iron Butterfly", "Covered Call", "Protective Put", "Custom"]
)

legs = []

# Initialize session state for custom legs if it doesn't exist
if "custom_legs" not in st.session_state:
    st.session_state.custom_legs = []

# --- Logic for Pre-defined Strategies ---
if strategy_type == "Straddle":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Buy Call + Buy Put at the same strike.")
    
    strike = st.sidebar.number_input("Strike Price", value=spot_price)
    premium_c = st.sidebar.number_input("Call Premium", value=2.50)
    premium_p = st.sidebar.number_input("Put Premium", value=3.00)
    
    legs.append({'strike': strike, 'premium': premium_c, 'type': 'Call', 'position': 'Long'})
    legs.append({'strike': strike, 'premium': premium_p, 'type': 'Put', 'position': 'Long'})

elif strategy_type == "Iron Condor":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Sell Inner Strikes, Buy Outer Strikes (Wings).")
    
    center_strike = st.sidebar.number_input("Center Strike", value=spot_price)
    width = st.sidebar.number_input("Wing Width", value=5.0)
    
    # 1. Put Wing (Bearish side)
    # Buy Outer Put (Protection)
    legs.append({'strike': center_strike - (2*width), 'premium': 0.5, 'type': 'Put', 'position': 'Long'})
    # Sell Inner Put (Income)
    legs.append({'strike': center_strike - width, 'premium': 2.0, 'type': 'Put', 'position': 'Short'})
    
    # 2. Call Wing (Bullish side)
    # Sell Inner Call (Income)
    legs.append({'strike': center_strike + width, 'premium': 2.0, 'type': 'Call', 'position': 'Short'})
    # Buy Outer Call (Protection)
    legs.append({'strike': center_strike + (2*width), 'premium': 0.5, 'type': 'Call', 'position': 'Long'})
elif strategy_type == "Butterfly Spread":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Long ITM Call + Short 2 ATM Calls + Long OTM Call")
    
    # Inputs
    center_strike = st.sidebar.number_input("Center Strike (ATM)", spot_price)
    wing_width = st.sidebar.number_input("Wing Width", 5.0)
    
    # 1. Buy Lower Call (In-The-Money)
    legs.append({'strike': center_strike - wing_width, 'premium': 5.0, 'type': 'Call', 'position': 'Long'})
    
    # 2. Sell 2 Middle Calls (At-The-Money)
    # We add this leg twice, or you could modify your logic to support quantity. 
    # For now, adding it twice is the easiest way to visualize 2 contracts.
    legs.append({'strike': center_strike, 'premium': 2.5, 'type': 'Call', 'position': 'Short'})
    legs.append({'strike': center_strike, 'premium': 2.5, 'type': 'Call', 'position': 'Short'})
    
    # 3. Buy Upper Call (Out-of-The-Money)
    legs.append({'strike': center_strike + wing_width, 'premium': 0.5, 'type': 'Call', 'position': 'Long'})

elif strategy_type == "Iron Butterfly":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Sell ATM Straddle + Buy OTM Strangle (Protection)")
    
    center_strike = st.sidebar.number_input("Center Strike", spot_price)
    wing_width = st.sidebar.number_input("Wing Width", 5.0)
    
    # 1. The Short Straddle (Income)
    legs.append({'strike': center_strike, 'premium': 3.0, 'type': 'Call', 'position': 'Short'})
    legs.append({'strike': center_strike, 'premium': 3.0, 'type': 'Put', 'position': 'Short'})
    
    # 2. The Long Strangle (Wings/Protection)
    legs.append({'strike': center_strike + wing_width, 'premium': 0.5, 'type': 'Call', 'position': 'Long'})
    legs.append({'strike': center_strike - wing_width, 'premium': 0.5, 'type': 'Put', 'position': 'Long'})

elif strategy_type == "Butterfly Spread":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Long ITM Call, Short 2 ATM Calls, Long OTM Call")
    
    center_strike = st.sidebar.number_input("Center Strike (ATM)", spot_price)
    width = st.sidebar.number_input("Wing Width", 5.0)
    
    # 1. Buy Lower Call (ITM)
    legs.append({'strike': center_strike - width, 'premium': 6.0, 'type': 'Call', 'position': 'Long'})
    
    # 2. Sell 2 Middle Calls (ATM)
    legs.append({'strike': center_strike, 'premium': 3.0, 'type': 'Call', 'position': 'Short'})
    legs.append({'strike': center_strike, 'premium': 3.0, 'type': 'Call', 'position': 'Short'})
    
    # 3. Buy Upper Call (OTM)
    legs.append({'strike': center_strike + width, 'premium': 1.0, 'type': 'Call', 'position': 'Long'})
    # Button to clear
    if st.sidebar.button("Clear All Legs"):
        st.session_state.custom_legs = []
        st.rerun()
        
    legs = st.session_state.custom_legs

elif strategy_type == "Long Strangle":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Buy OTM Put + Buy OTM Call")
    
    # Inputs
    strike_distance = st.sidebar.number_input("Distance from Spot", 5.0)
    
    # 1. Buy OTM Put (Lower Strike)
    legs.append({'strike': spot_price - strike_distance, 'premium': 1.5, 'type': 'Put', 'position': 'Long'})
    
    # 2. Buy OTM Call (Higher Strike)
    legs.append({'strike': spot_price + strike_distance, 'premium': 1.5, 'type': 'Call', 'position': 'Long'})

elif strategy_type == "Bull Call Spread":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Buy Low Call + Sell High Call")
    
    spread_width = st.sidebar.number_input("Spread Width", 5.0)
    
    # 1. Buy ATM Call (The "Driver")
    legs.append({'strike': spot_price, 'premium': 4.0, 'type': 'Call', 'position': 'Long'})
    
    # 2. Sell OTM Call (To reduce cost)
    legs.append({'strike': spot_price + spread_width, 'premium': 1.5, 'type': 'Call', 'position': 'Short'})

elif strategy_type == "Covered Call":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Long Stock + Short OTM Call")
    
    # 1. Long Stock (The Asset)
    legs.append({'strike': spot_price, 'premium': 0, 'type': 'Stock', 'position': 'Long'})
    
    # 2. Short Call (The Income)
    strike_input = st.sidebar.number_input("Call Strike", spot_price * 1.05) # Default to 5% OTM
    premium_input = st.sidebar.number_input("Call Premium", 2.0)
    
    legs.append({'strike': strike_input, 'premium': premium_input, 'type': 'Call', 'position': 'Short'})

elif strategy_type == "Protective Put":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Long Stock + Long Put (Insurance)")
    
    # 1. Long Stock (The Asset)
    legs.append({'strike': spot_price, 'premium': 0, 'type': 'Stock', 'position': 'Long'})
    
    # 2. Long Put (The Insurance)
    strike_input = st.sidebar.number_input("Put Strike", spot_price * 0.95) # Default to 5% OTM
    premium_input = st.sidebar.number_input("Put Premium", 2.0)
    
    legs.append({'strike': strike_input, 'premium': premium_input, 'type': 'Put', 'position': 'Long'})
elif strategy_type == "Bear Put Spread":
    st.sidebar.markdown("---")
    st.sidebar.caption("Setup: Buy High Put + Sell Low Put")
    
    spread_width = st.sidebar.number_input("Spread Width", 5.0)
    
    # 1. Buy ATM Put (The "Driver")
    legs.append({'strike': spot_price, 'premium': 4.0, 'type': 'Put', 'position': 'Long'})
    
    # 2. Sell OTM Put (To reduce cost)
    legs.append({'strike': spot_price - spread_width, 'premium': 1.5, 'type': 'Put', 'position': 'Short'})

elif strategy_type == "Custom":
    st.sidebar.markdown("---")
    st.sidebar.write("### Build Your Own")
    
    with st.sidebar.form("add_leg_form"):
        leg_type = st.selectbox("Type", ["Call", "Put","Stock"])
        leg_pos = st.selectbox("Position", ["Long (Buy)", "Short (Sell)"])
        leg_strike = st.number_input("Strike", value=spot_price)
        leg_premium = st.number_input("Premium", value=1.0)
        
        submitted = st.form_submit_button("Add Leg")
        
        if submitted:
            st.session_state.custom_legs.append({
                'strike': leg_strike, 
                'premium': leg_premium, 
                'type': leg_type, 
                'position': leg_pos.split()[0] # Take just "Long" or "Short"
            })
# --- Main Visualization ---
if legs:
    st.subheader(f"Payoff Diagram: {strategy_type}")
    
    # Generate X-axis range dynamically based on the strikes
    # Find min and max strikes to set the chart width nicely
    strikes = [leg['strike'] for leg in legs]
    min_strike = min(strikes)
    max_strike = max(strikes)
    margin = (max_strike - min_strike) * 0.5 if max_strike != min_strike else spot_price * 0.2
    
    spot_range = np.linspace(min_strike - margin, max_strike + margin, 100)
    
    # Plot
    fig = plot_strategy(spot_range, strategy_type, legs)
    st.plotly_chart(fig, width="stretch")

    # Show the Legs Table
    st.write("### Strategy Composition")
    st.table(legs)