from flask import Flask, jsonify, make_response, abort, request
from q_learning import initialize_learning_episode, step_learning_episode

# Initialize the app
app = Flask(__name__)

STEP_EPISODE_REQ = ['step', 'chosen_actions', 'arm_count', 'previous_action', 'num_cards', 'q_table', 'correct']


#Handle request errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'error': 'Bad request'}))


# Initializes the learning episode
@app.route('/api/v1.0/flashcards/initialize', methods=['POST'])
def initialize_episode():
    if not request.json or not "num_cards" in request.json:
      abort(400)

    # Call the episode function
    if "arm_count" in request.json and "q_table" in request.json:
      res = initialize_learning_episode(request.json["num_cards"], request.json['num_steps'], arm_count=request.json['arm_count'], q_table=request.json['q_table'])
      return jsonify(res)

    else:
      res = initialize_learning_episode(request.json["num_cards"], request.json['num_steps'])
      print(f"initial request {request.json} outgoing response {res}")
      return jsonify(res)

# Steps the learning episode
@app.route('/api/v1.0/flashcards/step', methods=['POST'])
def step_episode():
  if not request.json:
    abort(400)
  
  similarities = [param for param in STEP_EPISODE_REQ not in request.json]
  if len(similarities) > 0:
    abort(400)

  # Call the step function
  res = step_learning_episode()
  

if(__name__ == '__main__'):
  app.run(debug=True)