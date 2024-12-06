SELECT t1.name, type_name, manufacturer, eq_status, test_date
    FROM equipment.unit t1
    JOIN equipment.type t2 ON t1.et_id = t2.et_id;