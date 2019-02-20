import json, os
from stem.control import Controller
from flask import Flask, render_template, request

key_path = os.path.expanduser(os.path.dirname(os.path.realpath(__file__)) + '/rsa_saved.key')
PASS = 'aVerySecurePassword'
app = Flask(__name__)


@app.route('/')
@app.route('/fuck/')
def index():
    items = []
    with open('data.json', 'r') as f:
        items = json.loads(f.read())
    print(request.url_rule)
    fuck = False
    if str(request.url_rule).find('/fuck/') != -1:
        fuck = {
            'ip': request.remote_addr,
            'headers': [{'k': k, 'v': v} for k, v in request.headers.items()]
        }
    return render_template('main.html', items=items, fuck=fuck)

"""
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
"""

with Controller.from_port() as controller:
    controller.authenticate(password = PASS)

    if not os.path.exists(key_path):
        service = controller.create_ephemeral_hidden_service({80: 5000}, await_publication = True)
        print('Started a new hidden service with the address of %s.onion' % service.service_id)

        with open(key_path, 'w') as key_file:
            key_file.write('%s:%s' % (service.private_key_type, service.private_key))
    else:
        with open(key_path) as key_file:
            key_type, key_content = key_file.read().split(':', 1)

        service = controller.create_ephemeral_hidden_service({80: 5000}, key_type = key_type, key_content = key_content, await_publication = True)
        print('Resumed %s.onion' % service.service_id)

    try:
        # By default:  port 5000, only localhost allowed
        app.run()
    finally:
        print(" * Shutting down our hidden service")
        # controller.remove_hidden_service(hidden_service_dir)
        controller.remove_ephemeral_hidden_service(service.service_id)

app.run()