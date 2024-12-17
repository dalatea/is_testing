from base64 import b64encode
import json

from flask import session, redirect, url_for, current_app
from db.selector import select_list
from dataclasses import dataclass

@dataclass
class ProductInfoRespronse:
    result: dict
    error_message: str
    status: bool

config_path = {
    'director': "./data/dbconfig_director.json",
    'analyst': "./data/dbconfig_report.json",
    'manager': "./data/dbconfig_manager.json",
    None: "./data/dbconfig_testing.json"
}
def search_user(db_config, sql_provider, login, password):
    _sql = sql_provider.get('login.sql', login=login)
    result, schema = select_list(db_config, _sql)

    if len(result) == 0:
        return ProductInfoRespronse({}, "Такого пользователя не существует.", False)
    elif password != result[0][2]:
            return ProductInfoRespronse({}, "Неверный пароль. Попробуйте вновь.", False)

    return ProductInfoRespronse({
        'user_id': result[0][0],
        'user_group': result[0][1],
        'password': result[0][2]}, "Ошибок нет", True)

def create_basic_auth_token(login, password):
    credentials_b64 = b64encode(f'{login}:{password}'.encode('ascii')).decode('ascii')
    print('credential=', credentials_b64)
    token = f'Basic {credentials_b64}'
    print('token=', token)
    return token

def save_in_session_and_redirect(user):
    print(current_app.config['db_config'])
    group = user['user_group']
    with open(config_path[group]) as f:
        current_app.config['db_config'] = json.load(f)
    session['user_id'] = user['user_id']
    session['user_group'] = user['user_group']
    session.permanent = True
    print(current_app.config['db_config'])
    return redirect(url_for('menu_bp.start_menu_handler'))