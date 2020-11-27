#!/usr/bin/env python3

import os
import re
import socket
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template, request
from flask_socketio import SocketIO, emit
from werkzeug.utils import secure_filename

app = Flask(__name__)
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def data_test():
    print(request.json)
    socketio.emit("message", request.json, namespace="/main")
    return jsonify({"result": "ok"})


def intify(value):
    p = re.compile(r"0x[0-9]+")
    value = str(inferred(value).values[0])
    if re.match(p, value):
        return int(value, 0)
    else:
        return int(value)


def normalize(value, max, min):
    divisor = max - min
    if divisor == 0:
        divisor = 1
    return (value - min) / divisor


def inferred(x):
    if not isinstance(x, pd.Series):
        try:
            x = pd.Series(x)
        except BaseException:
            return x
    try:
        y = x.astype("Int64")
    except (TypeError, ValueError):
        try:
            y = x.astype("float")
        except BaseException:
            y = x.astype("object").infer_objects()
    return y


viz_types = set(["matrix", "line", "bar"])


@app.route("/csv", methods=["POST"])
def data_csv():
    t = request.args.get("type", default="matrix", type=str)
    if t not in viz_types:
        return jsonify({"result": "error", "message": "invalid type"})

    f = request.files["file"]
    lines = f.readlines()
    if f:
        try:
            data = np.genfromtxt(lines, delimiter=",", names=True)
        except:
            data = np.genfromtxt(
                lines, delimiter=",", names=None, dtype=None, autostrip=True
            )
        len_names = 0
        try:
            len_names = len(data.dtype.names)
        except:
            pass
        if len_names < 1:
            a = inferred(data)
        else:
            a = inferred(data[data.dtype.names[0]])
        # when y column is not present, default to linear scale
        if len_names < 2:
            b = [i for i in range(len(a))]
        else:
            b = inferred(data[data.dtype.names[1]])
        # when value column is not present, default to constant
        if len_names < 3:
            c = [1] * len(a)
        else:
            c = inferred(data[data.dtype.names[2]])
        a_max = 0
        a_min = float("inf")
        b_max = 0
        b_min = float("inf")
        c_max = 0
        c_min = float("inf")
        for i in range(len(a)):
            a_i = intify(a[i])
            b_i = intify(b[i])
            c_i = intify(c[i])
            if a_i > a_max:
                a_max = a_i
            if a_i < a_min:
                a_min = a_i
            if b_i > b_max:
                b_max = b_i
            if b_i < b_min:
                b_min = b_i
            if c_i > c_max:
                c_max = c_i
            if c_i < c_min:
                c_min = c_i
        parsed_data = []
        parsed_labels = []
        for i in range(len(a)):
            parsed_data.append(
                [
                    intify(a[i]),
                    intify(b[i]),
                    intify(c[i]),
                    normalize(intify(c[i]), c_max, c_min),
                ]
            )
            parsed_labels.append([str(a[i]), str(b[i]), str(c[i])])
        message = {
            "type": t,
            "max": [a_max, b_max, c_max],
            "min": [a_min, b_min, c_min],
            "values": parsed_data,
        }
        socketio.emit("csv", message, namespace="/main")
    return jsonify({"result": "ok"})


@app.after_request
def apply_cors(response):
    hostname = socket.gethostname()
    response.headers["Access-Control-Allow-Headers"] = "content-type"
    response.headers["Access-Control-Allow-Methods"] = "GET,HEAD,PUT,POST,DELETE,PATCH"
    response.headers["Access-Control-Allow-Origin"] = f"http://{hostname}"
    return response


@socketio.on("connect")
def test_connect():
    print("socketio client connected")


if __name__ == "__main__":
    socketio.run(app, host="127.0.0.1", port=os.environ.get("PORT", 3100), debug=False)
