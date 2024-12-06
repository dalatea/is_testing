import os
from base64 import b64decode
import json
from flask import Flask, request, current_app, jsonify

from db.sql_provider import SQLProvider
from db.selector import select_dict
#from blueprints.testing.route import testing_blueprint

app = Flask(__name__)

#app.register_blueprint(testing_blueprint, url_prefix='/testing')

with open('./data/dbconfiguser.json') as f:
    app.config['db_config'] = json.load(f)

app.secret_key = 'janfckjnjswJCFkjnkj'

provider = SQLProvider(os.path.join(os.path.dirname(__file__), 'sql'))

def valid_authorization_request(api_request):
    auth_header = api_request.headers.get('Authorization', '')
    print('auth_header=', auth_header)
    if not auth_header:
        return False
    pop = auth_header.startswith('Basic ')
    print('pop=', pop)
    if not auth_header.startswith('Basic '):
        return False
    if len(auth_header) <= len('Basic '):
        return False
    return True

def decode_basic_authorization(api_request):
    auth_header = api_request.headers.get('Authorization')
    print('auth_header=', auth_header)
    token = auth_header.split()[-1]
    print('token=', token)
    login_and_password = b64decode(token.encode('ascii')).decode('ascii').split(':')
    if len(login_and_password) != 2:
        raise ValueError('Invalid login and password format')
    login, password = login_and_password
    return login, password

@app.route('/find-user', methods=['GET'])
def find_user():
    if not valid_authorization_request(request):
        return jsonify({'status': 400, 'message': 'Bad request'})

    try:
        login, password = decode_basic_authorization(request)
    except Exception as e:
        return jsonify({'status': 400, 'message': f'Bad request. {str(e)}'})
    else:
        sql = provider.get('user.sql', login=login, password=password)
        user = select_dict(current_app.config['db_config'], sql)
        if not user:
            return jsonify({'status': 404, 'message': 'user not found'})

        return jsonify({'status': 200, 'message': 'OK', 'user': user[0]})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)