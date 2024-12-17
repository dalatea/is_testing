SELECT pt_id, tests.name
	FROM equipment.testing_protocol tp
    JOIN equipment.protocol_test pt ON tp.tp_id = pt.tp_id
    JOIN equipment.test tests ON pt.test_id = tests.test_id
	WHERE tp.tp_id = $e_protocol_id
    AND pt.exit_code IS NULL