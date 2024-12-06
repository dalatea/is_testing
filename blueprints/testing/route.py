from flask import Blueprint, render_template, request
from access import group_required

testing_blueprint = Blueprint(
    'testing_bp',
    __name__,
    template_folder='templates', static_folder='static')

@testing_blueprint.route('/')
@group_required
def start_testing_handler():
    return render_template('testing.html')

@testing_blueprint.route('/begin', methods=['POST'])
@group_required
def begin_testing():
    selected_tests = request.form.getlist('selected_tests')
    return selected_tests
