from flask import Blueprint, session, render_template, current_app
from access import login_required

menu_blueprint = Blueprint(
    'menu_bp',
    __name__,
    template_folder='templates', static_folder='static')

@menu_blueprint.route('/')
@login_required
def start_menu_handler():
    if session.get('user_group') == 'director':
        return render_template('director_menu.html')
    elif session.get('user_group') == 'analyst':
        return render_template('analyst_menu.html')
    else:
        return render_template('external_menu.html')