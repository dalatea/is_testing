SELECT t1.eu_id AS equipment_cipher,
 t1.name AS equipment_name,
SUBSTRING_INDEX(t2.name, ' ', 1) AS  worker_name,
t3.eq_status AS equipment_status
FROM unit AS t1
	JOIN testing_protocol AS t3 USING (eu_id)
    JOIN worker AS t2 USING(w_id)
		WHERE MONTH(t_date) = $month AND YEAR(t_date) = $year;
