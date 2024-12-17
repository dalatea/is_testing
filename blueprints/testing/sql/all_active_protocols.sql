SELECT
    tp.tp_id,
    tp.eu_id,
    un.name,
    t.type_name,
    pr_counts.test_count
FROM
    (SELECT
        tp_id,
        COUNT(*) AS test_count
     FROM
        `equipment`.protocol_test
     GROUP BY
        tp_id) AS pr_counts
JOIN
    `equipment`.testing_protocol AS tp ON pr_counts.tp_id = tp.tp_id
JOIN
    `equipment`.unit AS un ON tp.eu_id = un.eu_id
JOIN
    `equipment`.type AS t ON t.et_id = un.et_id
WHERE
    tp.w_id = 555
    AND tp.eq_status IS NULL;