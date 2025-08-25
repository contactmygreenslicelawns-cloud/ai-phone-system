from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello Railway! Flask app is running."

@app.route('/voice', methods=['POST'])
def voice():
    return '<?xml version="1.0" encoding="UTF-8"?><Response><Say>Hello from Green Slice AI Phone System</Say></Response>', 200, {'Content-Type': 'text/xml'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
