from dataclasses import dataclass
from db.selector import select_list, select_dict
from operations import ProductInfoRespronse as ProductInfoResponse2

@dataclass
class ProductInfoResponse:
    message: str
    status: bool


def get_years(db_config, provider):
    result = select_dict(db_config, f"SELECT DISTINCT YEAR(t_date) FROM testing_protocol ORDER BY YEAR(t_date) DESC;;")
    year_list = [f"{list(item.values())[0]}" for item in result]

    return year_list

def model_route(db_config, user_input_data, provider, sql_file):
    _sql = provider.get(sql_file, month=user_input_data['months'], year=user_input_data['years'])

    result, schema = select_list(db_config, _sql)
    if result or schema:
        return ProductInfoResponse(message=result[0][0], status=True)
    return ProductInfoResponse(message=result[0][0], status=False)

def model_route2(db_config, user_input_data, provider, sql_file):
    _sql = provider.get(sql_file, month=user_input_data['months'], year=user_input_data['years'], rep_id=user_input_data['reports'])

    print(_sql)
    result, schema = select_list(db_config, _sql)
    print(result)
    if result or schema and len(result) != 0:
        return ProductInfoResponse2(result, error_message='OK', status=True)
    return ProductInfoResponse2(result, error_message='No data', status=False)