import os
import json
import random
import string
import requests
import time
from datetime import datetime

import traceback
from flask import Flask, request, jsonify, render_template, Response


# Crear el server Flask
app = Flask(__name__)


gui_data = {
    "collide_level": {"top": 0, "left":0, "right":0},
    "frecuencia": 10
}

controller_data = {
    "moveleft": 0,
    "moveright": 0,
}


# ------------ Views ----------------- #
@app.route('/')
def login():
    return render_template('index.html', frecuencia=gui_data["frecuencia"])


# ---------------- API ------------------------
@app.route('/gui', methods=['POST'])
def gui():
    global gui_data
    global controller_data
    try:
        content_type = request.headers.get('Content-Type')
        if 'application/json' not in content_type:
            return Response(status=415)

        collide_level = request.json['collide_level']

        gui_data["collide_level"] = collide_level

        return jsonify(controller_data)

    except Exception as e:
        print(e)
        print(jsonify({'trace': traceback.format_exc()}))
        return Response(status=401)


@app.route('/controller', methods=['POST'])
def controller():
    global gui_data
    global controller_data
    try:
        content_type = request.headers.get('Content-Type')
        if 'application/json' not in content_type:
            return Response(status=415)

        moveleft = request.json['moveleft']
        moveright = request.json['moveright']

        controller_data["moveleft"] = moveleft
        controller_data["moveright"] = moveright

        return jsonify(gui_data)

    except Exception as e:
        print(e)
        print(jsonify({'trace': traceback.format_exc()}))
        return Response(status=401)

if __name__ == '__main__':
    print('Inove@Server start!')

    # Lanzar server
    app.run(host="127.0.0.1", port=5000)
