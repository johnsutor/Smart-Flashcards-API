from flask import Flask, jsonify, make_response, abort, request
from q_learning import initialize_learning_episode, step_learning_episode
from flask_cors import CORS

# Initialize the app
app = Flask(__name__)
CORS(app)

STEP_EPISODE_REQ = ['chosen_actions', 'arm_count', 'previous_action', 'num_cards', 'q_table', 'correct', 'num_steps']


#Handle request errors
@app.errorhandler(404)
def not_found(error):
  return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'error': 'Bad request'}))

@app.route('/')
def index():
  return '<h1>Welcome to the Flashcard API home</h1>'

# Initializes the learning episode
@app.route('/api/v1.0/flashcards/initialize', methods=['POST'])
def initialize_episode():
  if not request.json or not "num_cards" in request.json or not "num_steps" in request.json:
    abort(400)
  
  req = request.json

  # Call the episode function
  if "arm_count" in req and "q_table" in req:
    res = initialize_learning_episode(req["num_cards"], req['num_steps'], arm_count=req['arm_count'], q_table=req['q_table'])
    return jsonify(res)

  else:
    res = initialize_learning_episode(req["num_cards"], req['num_steps'])
    return jsonify(res)

# Steps the learning episode
@app.route('/api/v1.0/flashcards/step', methods=['POST'])
def step_episode():
  if not request.json:
    abort(400)
  
  # Check that all values are present
  if set(request.json.keys()) != set(STEP_EPISODE_REQ):
    abort(400)

  req = request.json

  # Call the step function
  res = step_learning_episode( req['chosen_actions'], req['arm_count'], req['previous_action'], req['num_cards'], req['q_table'], req['correct'], req['num_steps'])
  return jsonify(res)

if(__name__ == '__main__'):
  app.run(debug=False)