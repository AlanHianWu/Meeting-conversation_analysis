from flask import Flask
import os, sys

mod = os.path.join(os.getcwd(), "src\python_back\source")
sys.path.insert(1, mod)

# importing files from source
import speech_to_text, summarisation, dbp_spotlight

app = Flask(__name__)


@app.route("/members")
def members():
    return {"members": ["testing 1", "testing 2", "testing 3"]}

@app.route("/record")
def record():
    # reactjs record from browser
    return None

@app.route("/diarization")
def diarization():
    return None

@app.route("/speech_to_text")
def speech_to_text():
    return None

@app.route("/summarise")
def summarise():
    return None

@app.route("/dbp_spootlight")
def dbp_spootlight():
    return None


if __name__ == '__main__':
    app.run(debug=True)
