import os

from flask import Blueprint, render_template, current_app, request
from access import login_required, group_required
from db.sql_provider import SQLProvider
from .model import get_all_eq, get_all_types, get_filtered_eq, get_all_tests

query_blueprint = Blueprint(
    'query_bp',
    __name__,
    template_folder='templates', static_folder='static')

provider = SQLProvider(
    os.path.join(
        os.path.dirname(__file__),
        'sql')
)

@query_blueprint.route('/all_equipment', methods=['GET', 'POST'])
@group_required
def show_equipment():
    types = get_all_types(current_app.config['db_config'])
    if request.method == 'POST':
        equipment_type = request.form.get('type')
    else:
        equipment_type = None

    if equipment_type:
        # Логика фильтрации по выбранному типу
        res_info = get_filtered_eq(current_app.config['db_config'], provider, equipment_type)
    else:
        # Получаем все оборудование, если нет фильтра
        res_info = get_all_eq(current_app.config['db_config'], provider)

    print(res_info)
    if res_info.status:
        eq_title = "Оборудования в базе данных"
        return render_template("equipment.html", eq_title=eq_title, equipments=res_info.result, types=types)
    else:
        return "No result"

@query_blueprint.route('/equipment_tests', methods=['POST'])
@group_required
def show_equipment_tests():
    equipment_type = request.form.get('type')
    if equipment_type:
        res_info = get_all_tests(current_app.config['db_config'], provider, equipment_type)
        print(res_info)
    else:
        return "Не выбрано оборудование для тестирования"
    if res_info.status:
        eq_title = "Доступные тесты для данного оборудования"
        return render_template("equipment_tests.html", title=eq_title, tests=res_info.result)
    else:
        return "No result"

'''
@query_blueprint.route('/eq_category', methods=['GET'])
@group_required
def get_client_eq_type():
    types = get_all_types(current_app.config['db_config'])
    return render_template("input_type.html", types=types)
'''