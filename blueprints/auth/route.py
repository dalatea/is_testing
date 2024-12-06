import os
import json
from flask import Blueprint, session, redirect, request, render_template, current_app
from db.sql_provider import SQLProvider
from .model import search_user, create_basic_auth_token, save_in_session_and_redirect
import requests

auth_blueprint = Blueprint(
    'auth_bp',
    __name__,
    template_folder='templates',
    static_folder='static')

sql_provider = SQLProvider(
    os.path.join(
    os.path.dirname(__file__), #file - абсолютный путь до этого файла
        'sql'
    )
)

@auth_blueprint.route('/', methods=['GET', 'POST'])
def start_auth_handler():
    with open("./data/dbconfiguser.json") as f:
        current_app.config['db_config'] = json.load(f)

    if request.method == 'GET':
        return render_template('auth/input_login.html', message='')
    else:
        login = request.form['login']
        password = request.form['password']
        is_internal = True if request.form.get('is_internal') == 'on' else False

        if not login or not password:
            return render_template('auth/input_login.html', message='Повторите вход.')

        if not is_internal:
            response = requests.get(
                f'http://127.0.0.1:5002/find-user',
                headers={'Authorization': create_basic_auth_token(login, password)}
            )
            print('response=', response)
            resp_json = response.json()
            print('resp_json', resp_json)

            if resp_json['status'] == 200:
                return save_in_session_and_redirect(resp_json['user'])
        else:
            user = search_user(current_app.config['db_config'], sql_provider, login, password)

            if user.status == False:
                return render_template('auth/input_login.html', message=user.error_message)

            return save_in_session_and_redirect(user.result)