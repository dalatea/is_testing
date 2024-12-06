from functools import wraps
from flask import session, redirect, request, current_app, render_template

def login_required(func): #декоратор, принимает функцию и возвращает модифицированное поведение этой функции
    @wraps(func)
    def wrapper(*args, **kwargs): #передавать любые аргументы, какие хочешь
        if 'db_config' not in current_app.config:
            session.clear()
            return redirect('/auth')
        if 'user_id' in session:
            return func(*args, **kwargs)
        return redirect('/auth')
    return wrapper

def group_required(func): #декоратор, принимает функцию и возвращает модифицированное поведение этой функции
    @wraps(func)
    def wrapper(*args, **kwargs): #передавать любые аргументы, какие хочешь
        if 'db_config' not in current_app.config:
            session.clear()
            return redirect('/auth')
        if 'user_id' in session:
            user_group = session.get('user_group')
            if user_group == None:
                user_group = 'ext_user'
            access_config = current_app.config['db_access']
            if user_group in access_config:
                blueprint_name = request.endpoint.split('.')[0]
                url_name = request.endpoint
                if blueprint_name in access_config[user_group] or url_name in access_config[user_group]:
                    return func(*args, **kwargs)
                else:
                    return render_template("access_denied.html")
        return redirect('/auth')
    return wrapper