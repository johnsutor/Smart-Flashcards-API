import numpy as np 

# Create global variables for rewards and penalties
CORRECT_REWARD = 1
INCORRECT_PENALTY = -2

# Define the explore / exploit parameter
EPSILON = 0.8

# Function for creating a new q table
def create_q_table(num_cards):
  # Only use one row 
  return np.random.rand(1, num_cards)

# Function for updating the user's q table
def iterate_table(step, previous_action, num_cards, correct=False, q_table=None, num_steps=10):
  # Generate a new table if none exist
  if q_table is None:
    q_table = create_q_table(num_cards)
  
  # Block to execute if this is the first iteration of the episode
  if step == 0:
    if np.random.random() > epsilon:
      # Greedily choose an action that hasn't been previously chosen
      action = np.argmax()
