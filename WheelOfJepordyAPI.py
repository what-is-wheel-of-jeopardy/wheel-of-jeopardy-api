from flask import Flask, request, jsonify
import json 

application=Flask(__name__)

@application.route('/', methods=['GET'])
def helloWorld():
    return jsonify("Hello World")


@application.route('/', methods=['POST'])
def helloName():
    data = request.get_data()
    data = json.loads(data)
    return jsonify("Hello " + data["name"])