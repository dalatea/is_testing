SELECT
    protocol_test_count,
    worker_name,
    worker_last_name
FROM
    `equipment`.worker_report_str t1
JOIN
    (SELECT
		report_id,
		month,
        year
	FROM
		`equipment`.reports
    WHERE
		report_type = 1) t2 ON t1.report_id = t2.report_id
WHERE
    month = $month AND year = $year;