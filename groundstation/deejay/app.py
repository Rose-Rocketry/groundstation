from pathlib import Path
from flask import Flask, send_file

app = Flask(__name__)

data = Path("/data")


@app.route("/")
def list():
    json = dict()
    for rocket in data.iterdir():
        json[rocket.name] = [
            "/download/" + str(path.relative_to(data))
            for path in rocket.iterdir()
        ]
    return json


@app.route("/download/<path:path>")
def download(path):
    file = data / path
    return send_file(file)
