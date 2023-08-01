from flask import Flask, request, jsonify
from flask_cors import CORS
import random

app = Flask(__name__)
# OTP database to store generated OTPs and their status
otp_database = {}  # Format: {otp: {'verified': False}}
CORS(app)
# Endpoint to generate OTP
@app.route('/api/generate-otp', methods=['POST'])
def generate_otp():
    data = request.get_json()
    user_id = data.get('userId')

    if not user_id or not is_valid_user_id(user_id):
        return jsonify(error='Invalid user ID'), 400

    otp = generate_random_otp(6)
    otp_database[user_id] = {'otp': otp, 'verified': False}

    return jsonify(otp=otp), 200

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    user_id = data.get('userId')
    otp = data.get('otp')

    if not user_id or not otp:
        return jsonify(error='User ID and OTP are required'), 400

    stored_otp_info = otp_database.get(user_id)

    if not stored_otp_info:
        return jsonify(error='Invalid user ID'), 401

    if stored_otp_info['otp'] != otp:
        return jsonify(error='Invalid OTP'), 401

    if stored_otp_info['verified']:
        return jsonify(error='OTP already verified'), 401

    stored_otp_info['verified'] = True

    return jsonify(message='OTP verified successfully'), 200

def is_valid_user_id(user_id):
    # Implement your own user ID validation logic here.
    # This is just a basic example. You may want to use a proper validation mechanism.
    return isinstance(user_id, int) and user_id > 0

def generate_random_otp(length):
    return ''.join(str(random.randint(0, 9)) for _ in range(length))

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=10000)
