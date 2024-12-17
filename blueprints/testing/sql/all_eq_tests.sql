SELECT test_id, t1.name
    FROM equipment.test t1
    JOIN equipment.type t2 ON t1.et_id = t2.et_id
        WHERE type_name = '$type';