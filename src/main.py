import flask
from flask import request, jsonify, abort, make_response

from werkzeug.middleware.dispatcher import DispatcherMiddleware
from prometheus_client import make_wsgi_app, Counter


app = flask.Flask(__name__)
app.config["DEBUG"] = True


# Add prometheus wsgi middleware to route /metrics requests
REQUEST_COUNT = Counter('request_count', 'Number of requests', ['method', 'status'])
app_dispatch = DispatcherMiddleware(app, {
    '/metrics': make_wsgi_app()
})


version = "unknown"
try:
    with open("version.txt", "r") as f:
        version = f.readline().strip()
except Exception:
    pass


config_entries = [
    {
        "name": "a",
        "data": {}
    }
]


@app.route('/', methods=['GET'])
def home():
    REQUEST_COUNT.labels('get', '200').inc()
    return jsonify(dict(
        app="config-service",
        version=version
    ))


@app.route('/configs', methods=['GET'])
def config_list():
    return jsonify(config_entries)


@app.route('/configs/<string:config_name>', methods=['GET'])
def config_get(config_name):
    for config in config_entries:
        if config['name'] == config_name:
            REQUEST_COUNT.labels('get', '200').inc()
            return jsonify(config)

    REQUEST_COUNT.labels('get', '404').inc()
    abort(404)


@app.route('/configs', methods=['POST'])
def config_create():
    if not request.json or 'name' not in request.json or 'data' not in request.json:
        REQUEST_COUNT.labels('post', '400').inc()
        abort(400)

    config_name = request.json['name']
    config_data = request.json['data']

    config = [e for e in config_entries if e['name'] == config_name]

    if len(config) != 0:
        REQUEST_COUNT.labels('post', '409').inc()
        abort(409)

    config = {
        'name': config_name,
        'data': config_data
    }
    config_entries.append(config)
    REQUEST_COUNT.labels('post', '201').inc()
    return jsonify(config), 201


@app.route('/configs/<string:config_name>', methods=['PUT', 'PATCH'])
def update_task(config_name):
    config = [e for e in config_entries if e['name'] == config_name]

    if len(config) == 0:
        REQUEST_COUNT.labels('put', '404').inc()
        abort(404)
    if not request.json:
        REQUEST_COUNT.labels('put', '400').inc()
        abort(400)
    if 'name' not in request.json:
        REQUEST_COUNT.labels('put', '400').inc()
        abort(400)
    if 'data' not in request.json:
        REQUEST_COUNT.labels('put', '400').inc()
        abort(400)

    REQUEST_COUNT.labels('put', '200').inc()
    return jsonify({'task': config[0]})


@app.route('/configs/<string:config_name>', methods=['DELETE'])
def delete_task(config_name):
    config = [e for e in config_entries if e['name'] == config_name]

    if len(config) == 0:
        REQUEST_COUNT.labels('delete', '404').inc()
        abort(404)

    config_entries.remove(config[0])
    REQUEST_COUNT.labels('delete', '200').inc()
    return jsonify({'result': True})


@app.errorhandler(404)
def http_404(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(409)
def http_409(error):
    return make_response(jsonify({'error': 'Already exists'}), 409)


if __name__ == "__main__":
    app.run()
