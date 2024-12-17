SELECT w_id
	FROM `equipment`.testing_protocol
    WHERE eq_status IS NULL
    AND eu_id = $e_eu_id;