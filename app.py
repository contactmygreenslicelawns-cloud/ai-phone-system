from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello! Flask is working!"

@app.route('/test')
def test():
    return "Test endpoint works!"

@app.route('/voice', methods=['GET', 'POST'])
def voice():
    return "Voice endpoint reached!"

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
