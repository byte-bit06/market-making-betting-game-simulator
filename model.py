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

# Step 5 - make_quotes (not yet solved)
# TODO: implement

# Step 6 - execute_trade (not yet solved)
# TODO: implement

# Step 7 - mark_to_market_pnl (not yet solved)
# TODO: implement

# Step 8 - adverse_selection_loss (not yet solved)
# TODO: implement

# Step 9 - uncertainty_spread (not yet solved)
# TODO: implement

# Step 10 - inventory_skewed_quotes (not yet solved)
# TODO: implement

# Step 11 - update_fair_value_from_trade (not yet solved)
# TODO: implement

# Step 12 - update_remaining_card_value (not yet solved)
# TODO: implement

# Step 13 - run_market_making_episode (not yet solved)
# TODO: implement

# Step 14 - summarize_episode_pnls (not yet solved)
# TODO: implement

