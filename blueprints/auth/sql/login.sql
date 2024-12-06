SELECT user_id,
    user_group,
    password
FROM internal_user
WHERE 1=1
    AND login='$login'