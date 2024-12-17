from db.connection import DBContextManager


def select_list(db_config: dict, _sql: str):
    with DBContextManager(db_config) as cursor:
        if cursor is None:
            raise ValueError("Cursor not created")
        else:
            print(_sql)
            cursor.execute(_sql)
            result = cursor.fetchall()
            print(result)

            schema = [item[0] for item in cursor.description]
            print(result)
            return result, schema

def select_dict(db_config: dict, _sql: str):
    result, schema = select_list(db_config, _sql)
    result_dict = []
    for item in result:
        result_dict.append(dict(zip(schema, item)))
    # print(result_dict)
    return result_dict
