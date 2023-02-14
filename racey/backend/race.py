from flask import Flask, jsonify
from flask import request
import database
import sqlite3
from abstract_database_connection import AbstractDatabaseConnection
import uuid
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

@app.route("/submit", methods=["POST"])
def submit():
	body = request.get_json()

	print(body) 
	# Body is missing the flag
	if("press" not in body or 'button' not in body):
		return build_result("Missing parameter 'flag' or 'button'", 400)

	button = get_button(body['button']) # Ensure this exists...
	# button DNE	
	if(button == []):
		return build_result("Button does not exist", 400)

	button_id = button[0][0]
	score = button[0][1]

	# button has already been solved
	if(score != 0):
		return build_result("Already Pressed", 400)

	print(body['press'])
	if(body['press'] != 'true' and body['press'] != True):
		return build_result("Press not True", 400) 

	# Add the points for the button
	with AbstractDatabaseConnection('button.db') as conn:
		cursor = conn.cursor()

		# Add previous button score + 100
		cursor.execute("UPDATE buttons set score = score + ? WHERE button_id=?", (100, button_id))
		conn.commit()

	return build_result("Success!", 200)

# Remove the value
@app.route("/<button_id>", methods = ["DELETE"])
def remove(button_id):

	with AbstractDatabaseConnection('button.db') as conn:
		cursor = conn.cursor()
		cursor.execute("UPDATE buttons set score = 0 WHERE button_id=?", (button_id,))
		conn.commit()
	
	return build_result(button_id, 200)

# Add a new button to test
@app.route("/add_button", methods=["POST"])
def add_button():
	button_id = str(uuid.uuid4())
	with AbstractDatabaseConnection('button.db') as conn:
		cursor = conn.cursor()
		cursor.execute("INSERT INTO buttons VALUES(?, ?)", (button_id, 0))
		conn.commit()
		#result = cursor.fetchall()
	
	return build_result(button_id, 200)

# Did the score get larger than 100?
@app.route("/points/<button_id>", methods = ["GET"])
def send_points(button_id):
	button_info = get_button(button_id)

	# button DNE	
	if(button_info == []):
		return build_result("button does not exist", 400)	

	score = button_info[0][1]
	return build_result(score, 200)

# Did the score get larger than 100?
@app.route("/winner/<button_id>", methods = ["GET"])
def did_win(button_id):
	button_info = get_button(button_id)

	# button DNE	
	if(button_info == []):
		return build_result("button does not exist", 400)	

	score = button_info[0][1]
	if(score > 100):
		return build_result(get_flag(), 200)
	
	else: 
		return build_result("No dice :(", 403)

def build_result(content, http_status):
    """
    Build API response.
    Args:
        content: message content.
        http_status: HTTP status code.
    Returns:
        API response with message and HTTP code.
    """
    success = True if (http_status == 200) else False
    if (success):
        return jsonify({
            "success": 'true',
            "response": content,
            "code": http_status
        })
    else:
        return jsonify({
            "success": 'false',
            "error": {
                "code": http_status,
                "message": "Error: {}".format(content)
            }
        })

# Get the button from the database
def get_button(button_id):
	with AbstractDatabaseConnection('button.db') as conn:
		cursor = conn.cursor()
		cursor.execute("SELECT button_id, score FROM buttons WHERE button_id = ?", (button_id,))
		result = cursor.fetchall()
	
	return result

# Get the flag
def get_flag(): 
	with open('../flag.txt') as f:
		contents = f.read()
		return contents	

if __name__ == '__main__':
    # TODO: Turn off debugging on production.
    app.run(debug=True, port=8081, host="0.0.0.0")