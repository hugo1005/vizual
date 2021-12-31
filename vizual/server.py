import json
from flask import Flask, jsonify, request
import logging

# Server Side
debug_log = {}
MAIN_TASK = {'task_name':'Main', 'progress':0, 'total_iters': 1}
tasks = []

app = Flask(__name__)
# Disable flask printing
log = logging.getLogger('werkzeug')
log.disabled = True

@app.route("/", methods=['GET'])
def index():
    return app.send_static_file("index.html")

@app.route("/css/<name>", methods=['GET'])
def stylesheets(name):
    return app.send_static_file("./css/%s" % name)

@app.route("/assets/<name>", methods=['GET'])
def assets(name):
    return app.send_static_file("./assets/%s" % name)


@app.route('/channels', methods=['GET'])
@app.route('/channels/<name>', methods=['GET', 'POST'])
def channels(name=None):
    if request.method == 'GET':
        if type(name) == type(None):
            return jsonify(list(debug_log.keys()))
        else:
            return jsonify(debug_log[name] if name in debug_log else [])
    if request.method == 'POST':
        msg = request.json
        
        if name not in debug_log:
            debug_log[name] = []
        
        if type(msg) != type(None):
            debug_log[name].append(msg)

        return 'Debug Log Updated'

@app.route('/reset/<name>', methods=['POST'])
def reset(name):
    global debug_log

    if name.lower() == 'channels':
        debug_log = {channel: [] for channel in debug_log}

    return 'Reset Completed'

@app.route('/task', methods=['GET'])
@app.route('/task/<msgtype>', methods=['POST'])
def task(msgtype=None):
    global tasks

    if request.method == 'GET':
        return jsonify(tasks[0] if len(tasks) > 0 else MAIN_TASK)
    if request.method == 'POST':
        msg = request.json

        if msgtype.lower() == 'new':
            tasks.append({
                'task_name': msg['task_name'],
                'progress': 0, 
                'total_iters': float(msg['total_iters'])
            })

            return 'Task Added'

        if msgtype.lower() == 'update':
            tasks[0]['progress'] += float(msg['increment'])

            if tasks[0]['progress'] >= tasks[0]['total_iters']:
                tasks.pop(0)

            return 'Task Progressed'
        
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=8080)