SELECT
    age_group,
    COUNT(*) AS number_of_users,
    AVG(age) AS average_age
FROM {{ ref('dim_users') }}
GROUP BY age_group