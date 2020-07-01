import flask
from flask import request, jsonify, abort, make_response


app = flask.Flask(__name__)
app.config["DEBUG"] = True


config_entries = [
    {
        "name": "a",
        "data": {}
    }
]


@app.route('/', methods=['GET'])
def home():
    return "config-server"


@app.route('/configs', methods=['GET'])
def config_list():
    return jsonify(config_entries)


@app.route('/configs/<string:config_name>', methods=['GET'])
def config_get(config_name):
    for config in config_entries:
        if config['name'] == config_name:
            return jsonify(config)

    abort(404)


@app.route('/configs', methods=['POST'])
def config_create():
    if not request.json or 'name' not in request.json or 'data' not in request.json:
        abort(400)

    config_name = request.json['name']
    config_data = request.json['data']

    config = [e for e in config_entries if e['name'] == config_name]

    if len(config) != 0:
        abort(409)

    config = {
        'name': config_name,
        'data': config_data
    }
    config_entries.append(config)
    return jsonify(config), 201


@app.route('/configs/<string:config_name>', methods=['PUT'])
def update_task(config_name):
    config = [e for e in config_entries if e['name'] == config_name]

    if len(config) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        abort(400)
    if 'data' not in request.json:
        abort(400)
    return jsonify({'task': config[0]})


@app.route('/configs/<string:config_name>', methods=['DELETE'])
def delete_task(config_name):
    config = [e for e in config_entries if e['name'] == config_name]

    if len(config) == 0:
        abort(404)

    config_entries.remove(config[0])
    return jsonify({'result': True})


@app.errorhandler(404)
def http_404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(409)
def http_409(error):
    return make_response(jsonify({'error': 'Already exists'}), 409)


if __name__ == "__main__":
    app.run()
