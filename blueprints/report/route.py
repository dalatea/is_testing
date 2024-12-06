import os

from flask import Blueprint, render_template, current_app, request
from access import group_required
from db.sql_provider import SQLProvider
from .model import get_years, model_route, model_route2

report_blueprint = Blueprint(
    'report_bp',
    __name__,
    template_folder='templates', static_folder='static')

provider = SQLProvider(
    os.path.join(
        os.path.dirname(__file__),
        'sql')
)

report_list = [
    {
        'rep_id': '0',
        'rep_name': 'Количество созданных протоколов тестирования',
        'sql': 'worker_report.sql',
        'see_sql': 'see_worker_report.sql',
        'see_html': 'see_worker_report.html'},
    {
        'rep_id': '1',
        'rep_name': 'Состояние оборудований',
        'sql': 'testing_report.sql',
        'see_sql': 'see_testing_report.sql',
        'see_html': 'see_testing_report.html'}
]
@report_blueprint.route('/')
@group_required
def start_report_handler():
    return render_template('report.html')

@report_blueprint.route('/create_report', methods=['GET'])
@group_required
def create_report_choose():
    years = get_years(current_app.config['db_config'], provider)
    months = list(range(1, 13))

    return render_template("create_report_choose.html", months=months, years=years, reports=report_list)

@report_blueprint.route('/create_report', methods=['POST'])
@group_required
def create_report_show():
    user_data = request.form
    sql_file = report_list[int(user_data['reports'])]['sql']
    res_info = model_route(current_app.config['db_config'], user_data, provider, sql_file)
    if res_info.status:
        return render_template("create_info.html", result=res_info.message)

@report_blueprint.route('/see_report', methods=['GET'])
@group_required
def see_report_choose():
    years = get_years(current_app.config['db_config'], provider)
    months = list(range(1, 13))
    return render_template("see_report_choose.html", months=months, years=years, reports=report_list)

@report_blueprint.route('/see_report', methods=['POST'])
@group_required
def see_report():
    user_data = request.form
    sql_file = report_list[int(user_data['reports'])]['see_sql']
    see_html = report_list[int(user_data['reports'])]['see_html']

    res_info = model_route2(current_app.config['db_config'], user_data, provider, sql_file)

    if res_info.status:
        return render_template(see_html, month=user_data['months'], year=user_data['years'], strs=res_info.result)
    else:
        return render_template("create_info.html", result='Такого отчёта не существует')
