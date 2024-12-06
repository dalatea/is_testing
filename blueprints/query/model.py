from dataclasses import dataclass
from db.selector import select_list

from db.selector import select_dict

@dataclass
class ProductInfoRespronse:
    result: tuple
    error_message: str
    status: bool

def get_all_eq(db_config, sql_provider):
    _sql = sql_provider.get('all_equipment.sql')
    print("sql=", _sql)
    result, schema = select_list(db_config, _sql)
    print("result", result, "\n")
    print("schema", schema, "\n")
    return ProductInfoRespronse(result, error_message='', status=True)

def get_all_types(db_config):
    result = select_dict(db_config, f"SELECT type_name FROM equipment.type;")
    type_list = [f"{list(item.values())[0]}" for item in result]
    print(type_list)
    return type_list

def get_all_names(db_config):
    result = select_dict(db_config, f"SELECT type_name FROM equipment.type;")
    name_list = [f"{list(item.values())[0]}" for item in result]
    print(name_list)
    return name_list

def get_filtered_eq(db_config, sql_provider, equipment_type):
    _sql = sql_provider.get('filter_eq.sql', type=equipment_type)
    result, schema = select_list(db_config, _sql)
    return ProductInfoRespronse(result, error_message='', status=True)

def get_all_tests(db_config, sql_provider, equipment_type):
    _sql = sql_provider.get('all_eq_tests.sql', type=equipment_type)
    result, schema = select_list(db_config, _sql)
    return ProductInfoRespronse(result, error_message='', status=True)
