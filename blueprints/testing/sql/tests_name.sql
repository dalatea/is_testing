SELECT test_id, t1.name
    FROM equipment.test t1
		WHERE test_id = $test_id;