import numpy as np 

# Create global variables for rewards and penalties
CORRECT_PENALTY = -2
INCORRECT_REWARD = 1

# Define the explore / exploit parameter
EPSILON = 0.8

# Function for initializing an episode
def initialize_learning_episode(num_cards, num_steps=10, **kwargs):
  '''
  Provides an API-callable function to initialize reinforcement
  learning. It must be called with the following parameters:

  @param num_cards: the number of cards to present to the user
  @param num_steps: the number of steps in the Q learning process
  @param q_table: the q table to use within the 
  @returns: Updated values for the above parameters
  '''
  if kwargs is not None:
    q_table = np.frombuffer(kwargs['q_table'], dtype=float) 
    arm_count = np.frombuffer(kwargs['arm_count'], dtype=int)
  else:
    # Generate a Q table and an arm counter
    q_table = np.random.rand(1, num_cards)
    arm_count = [0] * num_cards

  # Choose an action to take
  if np.random.random() > EPSILON:
    action = np.argmax(q_table)
  else:
    action = np.random.randint(0, num_cards)

  # Convert arrays to a buffer
  q_table = q_table.tostring()
  arm_count = arm_count.tostring()
  
  return {
    'action': action,
    'q_table': q_table,
    'arm_count': arm_count
  }

# Function for updating the user's q table
def step_learning_episode(step, chosen_actions, arm_count, previous_action, num_cards, q_table, correct, num_steps=10):
  '''
  Provides an API-callable function to complete reinforcement
  learning. It must be called with the following parameters:

  @param step: The current step of the episode
  @param chosen_actions: an array containing previously chosen actions 
  @param arm_count: an array that tallies the number of times an action has been chosen
  @param previous_action: an integer that represents the previous chosen action
  @param num_cards: the number of cards to present to the user
  @param correct: if the previously chosen question was correct
  @param q_table: the q table to use within the 
  @returns: Updated values for the above parameters
  '''

  # Interpret the buffer to a one dimensional array
  q_table, arm_count, chosen_actions = np.frombuffer(q_table, dtype=float), np.frombuffer(arm_count, dtype=int), np.frombuffer(chosen_actions, dtype=int)
  
  # Create an array of the index of all max values
  available_action_array = []
  for a in range(len(q_table)):
    available_action_array.append(np.argmax(q_table))
    available_action_array = [action for action in available_action_array if action not in chosen_actions]

  # Choose an action to take
  if np.random.random() > EPSILON:
    action = available_action_array[0]
  else:
    action = available_action_array[np.random.randint(0, len(available_action_array))]
  chosen_actions.append(action)
  
  # Determine the reward
  if correct:
    reward = CORRECT_PENALTY
  else:
    reward = INCORRECT_REWARD

  # Recalculate the Q table based on if the user got the previous question right
  arm_count[previous_action] += 1
  q_table[previous_action] += (1 / arm_count[previous_action]) * (reward - q_table[previous_action])
  step += 1

  # Convert all arrays back to buffers
  q_table, arm_count, chosen_actions = q_table.tostring(), arm_count.tostring(), chosen_actions.tostring()

  # Return the updated values
  return {
    'action': action,
    'q_table': q_table,
    'arm_count': arm_count,
    'chosen_actions': chosen_actions
  }
