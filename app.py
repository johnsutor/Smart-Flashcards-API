from flask import Flask, jsonify, make_response, abort, request

# Initialize the app
app = Flask(__name__)

#Handle request errors
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
  return make_response(jsonify({'error': 'Bad request'}))


# Updates the Q table provided by the user
# or creates a new q table
@app.route('/flashcards/api/v1.0', methods=['POST'])
def calculate_q_value():
    if not request.json or not 'title' in request.json:
      abort(400)
    return jsonify({'tasks': tasks})

    # Receive the q table object from the user
    q_table_object = {
      'q_table': request.json['q_table']

    }

    # TODO: Call the q-learning function

if(__name__ == '__main__'):
  app.run(debug=True)