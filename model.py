"""
Market-Making & Betting-Game Simulator

Assembled from your step-by-step solutions.
"""

import numpy as np

# Step 1 - expected_value
def expected_value(values, probabilities):

    mean = 0

    for i in range(len(values)):
        mean += values[i]*probabilities[i]

    return mean

# Step 2 - one_reroll_die_value
import numpy as np

def expected_value(values, probabilities):
    return np.dot(values, probabilities)

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

# Step 3 - pay_per_reroll_die_game (not yet solved)
# TODO: implement

# Step 4 - red_black_card_game_value (not yet solved)
# TODO: implement

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

