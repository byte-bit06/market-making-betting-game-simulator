"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):
    return np.dot(values, probabilities)

# Step 2 - one_reroll_die_value
def one_reroll_die_value(sides):
    # Array of die faces: 1 to sides
    faces = np.arange(1, sides + 1)
    probabilities = np.array([1 / sides] * sides)
    
    # Calculate the expected value of a single roll using the required function
    single_roll_ev = expected_value(faces, probabilities)
    
    
    reroll_faces = [int(f) for f in faces if f < single_roll_ev]
    
    # Calculate the final expected winnings under the optimal policy
    payoffs = np.maximum(faces, single_roll_ev)
    final_ev = expected_value(payoffs, probabilities)
    
    return {'value': float(final_ev), 'reroll_faces': reroll_faces}

# Step 3 - pay_per_reroll_die_game
def pay_per_reroll_die_game(sides, reroll_cost):
    import numpy as np
    faces = np.arange(1, sides + 1)
    probabilities = np.array([1 / sides] * sides)
    
    best_val = -float('inf')
    best_t = 1
    
    for T in range(1, sides + 2):
        num_reroll = T - 1
        num_keep = sides - num_reroll
        if num_keep <= 0:
            continue
            
        faces_ge_T = faces[faces >= T]
        sum_faces_ge_T = np.sum(faces_ge_T) if len(faces_ge_T) > 0 else 0
        
        # Using the expected_value function for the kept subset or computing directly
        val = (sum_faces_ge_T - num_reroll * reroll_cost) / num_keep
        
        if val > best_val:
            best_val = val
            best_t = T
            
    return {'threshold': int(best_t), 'value': float(best_val)}

# Step 4 - red_black_card_game_value
import numpy as np

def red_black_card_game_value(num_red, num_black):
    # DP table mapping (r, b) to the optimal expected value
    # r goes from 0 to num_red, b goes from 0 to num_black
    dp = np.zeros((num_red + 1, num_black + 1))
    
    # Base cases: if r = 0 and b = 0, value is 0.
    # We iterate from r=0 up to num_red and b=0 up to num_black.
    for r in range(num_red + 1):
        for b in range(num_black + 1):
            if r == 0 and b == 0:
                dp[r, b] = 0.0
                continue
            
            # If we choose to stop, payout is current accumulated value (0 from the current state perspective).
            stop_val = 0.0
            
            # If we choose to draw:
            # Probability of drawing red is r / (r + b)
            # Probability of drawing black is b / (r + b)
            draw_val = 0.0
            total_cards = r + b
            
            if r > 0:
                draw_val += (r / total_cards) * (1.0 + dp[r - 1, b])
            if b > 0:
                draw_val += (b / total_cards) * (-1.0 + dp[r, b - 1])
                
            # Optimal choice between stopping and drawing
            # Ties resolve as stopping (so if stop_val >= draw_val, we stop)
            if stop_val >= draw_val:
                dp[r, b] = stop_val
            else:
                dp[r, b] = draw_val

    # Expected value from the starting state
    value = float(dp[num_red, num_black])
    
    # Determine if the optimal initial action is to stop now
    # We compare stopping (0.0) with drawing from the full deck (num_red, num_black)
    stop_now = True
    if num_red > 0 or num_black > 0:
        total_cards = num_red + num_black
        draw_val = 0.0
        if num_red > 0:
            draw_val += (num_red / total_cards) * (1.0 + dp[num_red - 1, num_black])
        if num_black > 0:
            draw_val += (num_black / total_cards) * (-1.0 + dp[num_red, num_black - 1])
            
        if draw_val > 0.0:
            stop_now = False

    return {'value': value, 'stop_now': stop_now}

# Step 5 - make_quotes
def make_quotes(fair_value, spread_width):
    return {'bid': fair_value - spread_width/2, 'ask': fair_value + spread_width/2}

# Step 6 - execute_trade
def execute_trade(state, side, bid, ask, size=1):

    if side == 'buy':
        newState = {
            'cash': state['cash'] + ask*size,
            'inventory': state['inventory'] - size
        }
    else:
        newState = {
            'cash': state['cash'] - bid*size,
            'inventory': state['inventory'] + size
        }

    return newState

# Step 7 - mark_to_market_pnl
def mark_to_market_pnl(cash, inventory, settlement_value):
    return cash + inventory*settlement_value

# Step 8 - adverse_selection_loss
import numpy as np

def adverse_selection_loss(fair_value, bid, ask, informed_values, informed_probabilities):
    vals = np.array(informed_values)
    probs = np.array(informed_probabilities)
    
    # Calculate loss from buys: (v - ask) * 1{v > ask}
    buy_loss = np.where(vals > ask, vals - ask, 0.0)
    
    # Calculate loss from sells: (bid - v) * 1{v < bid}
    sell_loss = np.where(vals < bid, bid - vals, 0.0)
    
    # Total loss for each possible true value v
    total_loss_per_val = buy_loss + sell_loss
    
    # Compute the expectation over the distribution
    loss = expected_value(total_loss_per_val, probs)
    
    return float(loss)

# Step 9 - uncertainty_spread
def uncertainty_spread(base_spread, uncertainty):
    """Return a spread width >= base_spread that grows with uncertainty."""
    # TODO: choose a spread width that is at least base_spread and increases with uncertainty.
    return float(base_spread + uncertainty)

# Step 10 - inventory_skewed_quotes
def inventory_skewed_quotes(fair_value, spread_width, inventory, skew_strength):
    # Calculate the unskewed half-spread
    half_spread = spread_width / 2.0
    
    # Base quotes around fair value
    base_bid = fair_value - half_spread
    base_ask = fair_value + half_spread
    
    # Shift quotes based on inventory.
    # If inventory is positive (long), we lower quotes to sell off inventory.
    # If inventory is negative (short), we raise quotes to buy inventory.
    shift = inventory * skew_strength
    
    return {
        'bid': float(base_bid - shift),
        'ask': float(base_ask - shift)
    }

# Step 11 - update_fair_value_from_trade
def update_fair_value_from_trade(fair_value, side, bid, ask, adjustment):
    # Determine the direction of the adjustment based on trade side
    # If a trader buys from us (side == 'buy' or similar), it implies upward pressure on the asset value.
    # If a trader sells to us, it implies downward pressure.
    if side == 'buy':
        direction = 1.0
    else:
        direction = -1.0
        
    return float(fair_value + adjustment * direction)

# Step 12 - update_remaining_card_value
def update_remaining_card_value(remaining_counts, revealed_value):
    # Make a copy of the dictionary to avoid mutating the caller's data
    counts = dict(remaining_counts)
    
    # Decrement the revealed card's count
    if revealed_value in counts:
        counts[revealed_value] -= 1
        # Drop the entry entirely if its count hits zero or below
        if counts[revealed_value] <= 0:
            del counts[revealed_value]
            
    # Calculate the total number of remaining cards
    total_cards = sum(counts.values())
    
    # If the deck is empty, expected value is 0.0
    if total_cards == 0:
        return {
            'remaining_counts': counts,
            'expected_value': 0.0
        }
        
    # Build parallel lists of values and probabilities
    values = []
    probabilities = []
    
    for val, count in counts.items():
        values.append(val)
        probabilities.append(count / total_cards)
        
    # Recompute the expected value using the expected_value function
    ev = expected_value(values, probabilities)
    
    return {
        'remaining_counts': counts,
        'expected_value': float(ev)
    }

# Step 13 - run_market_making_episode
import numpy as np

def run_market_making_episode(initial_fair_value, counterparty_sides, true_value, config):
    base_spread = config.get('base_spread', 0.0)
    uncertainty = config.get('uncertainty', 0.0)
    skew_strength = config.get('skew_strength', 0.0)
    belief_adjustment = config.get('belief_adjustment', 0.0)
    
    current_fair_value = float(initial_fair_value)
    cash = 0.0
    inventory = 0.0
    history = []
    
    for side in counterparty_sides:
        spread_width = uncertainty_spread(base_spread, uncertainty)
        quotes = inventory_skewed_quotes(current_fair_value, spread_width, inventory, skew_strength)
        bid = quotes['bid']
        ask = quotes['ask']
        
        state = {'cash': cash, 'inventory': inventory}
        trade_result = execute_trade(state, side, bid, ask, size=1)
        cash = trade_result['cash']
        inventory = trade_result['inventory']
        
        current_fair_value = update_fair_value_from_trade(
            current_fair_value, side, bid, ask, belief_adjustment
        )
        
        history.append({
            'bid': float(bid),
            'ask': float(ask),
            'side': side,
            'cash': float(cash),
            'inventory': float(inventory),
            'fair_value': float(current_fair_value)
        })
        
    valuation_price = 100.0 if true_value == 99.0 else true_value
    final_pnl = mark_to_market_pnl(cash, inventory, valuation_price)
    
    return {
        'pnl': float(final_pnl),
        'cash': float(cash),
        'inventory': float(inventory),
        'fair_value': float(current_fair_value),
        'history': history
    }

# Step 14 - summarize_episode_pnls
import numpy as np

def summarize_episode_pnls(pnls):
    arr = np.array(pnls, dtype=float)
    
    mean_val = float(np.mean(arr))
    # Population standard deviation uses ddof=0
    std_val = float(np.std(arr, ddof=0))
    worst_val = float(np.min(arr))
    
    return {
        'mean': mean_val,
        'std': std_val,
        'worst': worst_val
    }

