from flask import Flask, request, render_template
import socket, json

app = Flask(__name__)
PORT = 5000
REGISTER_URL = "http://10.5.3.92:5000/register"


@app.route('/force')
def force():
    return render_template('force_layout.html')

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    # Load the file
    with open('data/musicians.json') as data_file:
        data = json.load(data_file)
    return json.dumps(data)

if __name__ == '__main__':

    # Start Flask app
    app.run(host='0.0.0.0', port=PORT, debug=True)
