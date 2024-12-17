SELECT eu_id, t1.name, type_name, eq_status, test_date, test_period
FROM `equipment`.unit t1
JOIN `equipment`.type t2 ON t1.et_id = t2.et_id
WHERE DATE_ADD(test_date, INTERVAL test_period MONTH) <= CURDATE()
AND NOT EXISTS (
    SELECT 1
    FROM `equipment`.testing_protocol tp
    WHERE tp.eu_id = t1.eu_id
    AND tp.eq_status IS NULL
)
ORDER BY DATEDIFF(CURDATE(), DATE_ADD(test_date, INTERVAL test_period MONTH)) DESC;