from flask import Flask
app = Flask(__name__)

@app.route("/test", methods=['POST'])
def hello():
    return "Hello World!"


app.run(debug=True)
