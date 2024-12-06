from flask import Blueprint, render_template, request
from access import group_required

client_blueprint = Blueprint(
    'client_bp',
    __name__,
    template_folder='templates', static_folder='static')

@client_blueprint.route('/')
@group_required
def start_client_handler():
    return render_template('client.html')

@client_blueprint.route('/request', methods=['POST'])
@group_required
def client_request_handler():
    eq_type = request.form.get('eq_type')
    return eq_type