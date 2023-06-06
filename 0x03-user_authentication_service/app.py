#!/usr/bin/env python3
"""flask app"""

from flask import jsonify, Flask

app = Flask(__name__)

app.route('/', methods=['GET'])


def basic_app():
    """returns a message"""
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
