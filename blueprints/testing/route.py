import os

from flask import Blueprint, render_template, request, session, redirect, url_for, current_app
from access import group_required
from .model import form_basket, get_all_eq, get_all_types, get_filtered_eq, equipment_tests_model, transaction, get_active_protocols, get_active_tests, get_all_tests
from db.sql_provider import SQLProvider

testing_blueprint = Blueprint(
    'testing_bp',
    __name__,
    template_folder='templates', static_folder='static')

provider = SQLProvider(
    os.path.join(
        os.path.dirname(__file__),
        'sql')
)

@testing_blueprint.route('/all_equipment', methods=['GET', 'POST'])
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
        return res_info.error_message

@testing_blueprint.route('/equipment_tests', methods=['POST'])
@group_required
def show_equipment_tests():
    equipment_type = request.form.get('type')
    equipment_id = request.form.get('eu_id')

    model_info = [equipment_id, equipment_type]
    res_info = equipment_tests_model(current_app.config['db_config'], provider, model_info)

    if res_info.status:
        eq_title = "Доступные тесты для данного оборудования"
        return render_template("equipment_tests.html", title=eq_title, tests=res_info.result)
    else:
        return render_template("basket_info.html", message=res_info.error_message)

@testing_blueprint.route('/active', methods=['GET'])
@group_required
def active_prots():
    user_id = session.get('user_id', "")
    res_info = get_active_protocols(current_app.config['db_config'], provider, user_id)
    if res_info.status:
        title = "Незавершённые протоколы тестирования"
        return render_template("active_protocols.html", title=title, protocols=res_info.result)
    else:
        return "No result"

@testing_blueprint.route('/active', methods=['POST'])
@group_required
def active_tests():
    tp_id = request.form.get('protocol')
    res_info = get_active_tests(current_app.config['db_config'], provider, tp_id)
    if res_info.status:
        title = f"Незавершённые тесты в протоколе {tp_id}"
        return render_template("active_tests.html", title=title, tests=res_info.result)
    else:
        return "No result"


@testing_blueprint.route('/basket', methods=['GET'])
@group_required
def basket_index():
    current_basket = session.get('basket', {})
    current_basket = form_basket(current_basket, provider, current_app)
    print(current_basket)
    return render_template('basket_dynamic.html', basket=current_basket)
    #return render_template('basket_dynamic.html', basket=current_basket)


@testing_blueprint.route('/basket', methods=['POST'])
@group_required
def basket_main():
    selected_tests = request.form.getlist('selected_tests')
    if selected_tests:
        eu_id = session.get('eu_id', None)
        if not 'basket' in session:
            session['basket'] = dict()
        session['basket'][str(eu_id)] = selected_tests
        session.modified = True
    else:
        session['eu_id'] = None
    if request.form.get('product_display_delete'):
        eu_id = request.form.get('eu_id')
        session['basket'].pop(eu_id)
        session.modified = True
    if request.form.get('product_display_change'):
        eu_id = request.form.get('eu_id')
        eq_type = request.form.get('type')
        session['eu_id'] = eu_id
        session['equipment_type'] = eq_type
        return redirect(url_for('testing_bp.change_tests'))
    print("BASKET=", session.get('basket', []))
    return redirect(url_for('testing_bp.basket_index'))


@testing_blueprint.route('/change_tests', methods=['GET', 'POST'])
@group_required
def change_tests():
    eu_id = session.get('eu_id')
    equipment_type = session.get('equipment_type')

    if request.method == 'GET':
        if eu_id and equipment_type:
            # Получите все тесты для данного оборудования
            res_info = get_all_tests(current_app.config['db_config'], provider, equipment_type)
            if res_info.status:
                eq_title = "Изменение тестов для оборудования"
                return render_template("equipment_tests.html", title=eq_title, tests=res_info.result, eu_id=eu_id)
        return "Не удается получить тесты для выбранного оборудования."

    # Обработка POST-запроса для сохранения измененных тестов
    selected_tests = request.form.getlist('selected_tests')
    if selected_tests:
        session['basket'][eu_id] = selected_tests
        session.modified = True
    session['eu_id'] = None
    session['type'] = None
    return redirect(url_for('testing_bp.basket_index'))

@testing_blueprint.route('/clear_basket')
@group_required
def clear_basket():
    if session.get('basket', {}):
        session.pop('basket')
    return redirect(url_for('testing_bp.basket_index'))


@testing_blueprint.route('/save_order')
@group_required
def create_protocols():
    if not session.get('basket', {}):
        return redirect(url_for('basket_bp.basket_index'))

    print("Order success")
    current_basket = session.get('basket', {})
    user_id = session.get('user_id', "")
    result = transaction(current_app.config['db_config'], provider, current_basket, user_id)
    print(current_basket)
    print(user_id)
    if result.status:
        clear_basket()
        return render_template("basket_info.html", message=result.error_message)
    else:
        return render_template("basket_info.html", message=result.error_message)

