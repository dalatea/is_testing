SELECT
    eq_cipher,
    eq_name,
    eq_tests,
    eq_errors
FROM
    `equipment`.testing_report_str t1
JOIN
    (SELECT
		report_id,
		month,
        year
	FROM
		`equipment`.reports
    WHERE
		report_type = 2) t2 ON t1.report_id = t2.report_id
WHERE
    month = $month AND year = $year;