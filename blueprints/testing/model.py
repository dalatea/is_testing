from dataclasses import dataclass
from datetime import date

from flask import session

from db.selector import select_list, select_dict
from db.connection import DBContextManager

@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool

@dataclass
class ProductInfoResponse2:
    result: str
    error_message: str
    status: bool

def get_all_eq(db_config, sql_provider):
    session['eu_id'] = None
    _sql = sql_provider.get('all_equipment.sql')
    print("sql=", _sql)
    result, schema = select_list(db_config, _sql)
    print("result", result, "\n")
    print("schema", schema, "\n")
    if len(result) == 0:
        return ProductInfoRespronse(result, error_message='Оборудования не нуждаются в тестировании', status=False)
    return ProductInfoRespronse(result, error_message='OK', status=True)

def get_all_types(db_config):
    result = select_dict(db_config, f"SELECT type_name FROM equipment.type;")
    type_list = [f"{list(item.values())[0]}" for item in result]
    print(type_list)
    return type_list

def get_filtered_eq(db_config, sql_provider, equipment_type):
    session['eu_id'] = None
    _sql = sql_provider.get('filter_eq.sql', type=equipment_type)
    result, schema = select_list(db_config, _sql)
    return ProductInfoRespronse(result, error_message='OK', status=True)

def get_all_tests(db_config, sql_provider, equipment_type):
    _sql = sql_provider.get('all_eq_tests.sql', type=equipment_type)
    result, schema = select_list(db_config, _sql)
    return ProductInfoRespronse(result, error_message='OK', status=True)

def equipment_tests_model(db_config, sql_provider, model_info):
    equipment_id = model_info[0]
    equipment_type = model_info[1]
    result = ()

    if equipment_type:
        if 'basket' in session:
            if equipment_id in session['basket']:
                return ProductInfoRespronse(result, error_message='Это оборудование уже добавлено в план тестирования', status=False)
        session['eu_id'] = equipment_id
        res_info = get_all_tests(db_config, sql_provider, equipment_type)
        result = res_info.result
        print(res_info)
        return ProductInfoRespronse(result, error_message='OK', status=True)
    else:
        return ProductInfoRespronse(result, error_message='Не выбрано оборудование для тестирования', status=False)

def get_active_protocols(db_config, sql_provider, user_id):
    _sql = sql_provider.get('all_active_protocols.sql', e_user_id=user_id)
    result, schema = select_list(db_config, _sql)
    return ProductInfoRespronse(result, error_message='', status=True)

def get_active_tests(db_config, sql_provider, protocol_id):
    _sql = sql_provider.get('all_active_tp_tests.sql', e_protocol_id=protocol_id)
    result, schema = select_list(db_config, _sql)
    return ProductInfoRespronse(result, error_message='', status=True)

def transaction(db_config : dict, sql_provider, basket : dict, user_id: int):
    prod_info_response = ProductInfoResponse2(0, error_message='Протокол тестирования не был создан', status=False)
    protocol_id_list = []
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            ddate = date.today()

            for key, value in basket.items():
                _sql = sql_provider.get('create_protocol.sql',
                                        e_order_date=ddate,
                                        e_user_id=int(user_id),
                                        e_eq_id=int(key))
                print(_sql)
                cursor.execute(_sql)
                protocol_id = cursor.lastrowid
                print(protocol_id)
                for test in value:
                    _sql = sql_provider.get('insert_test_in_protocol.sql',
                                            e_protocol_id=protocol_id,
                                            e_test_id=int(test))
                    print(_sql)
                    cursor.execute(_sql)
                protocol_id_list.append(protocol_id)
            prot_info = ''
            for i in range (len(protocol_id_list)):
                if i == len(protocol_id_list) - 1:
                    prot_info += str(protocol_id_list[i])
                else:
                    prot_info += str(protocol_id_list[i]) + ', '
            if len(protocol_id_list) == 1:
                prot_info = 'Создан протокол тестирования номер ' + prot_info
            else:
                prot_info = 'Созданы протоколы тестирования номер ' + prot_info
            prod_info_response = ProductInfoResponse2(protocol_id, error_message=prot_info, status=True)

    return prod_info_response


def form_basket(current_basket : dict, provider, current_app):
    basket = []
    for k,v in current_basket.items():
        tests = []
        _sql = provider.get('one_eq.sql', unit_id=k)
        print(k,v)
        equipment = select_dict(current_app.config['db_config'], _sql)[0]
        for i in v:
            _sql = provider.get('tests_name.sql', test_id=int(i))
            test = select_dict(current_app.config['db_config'], _sql)[0]
            tests.append(test['name'])
            print(tests)
        equipment['tests'] = tests
        basket.append(equipment)
    return basket