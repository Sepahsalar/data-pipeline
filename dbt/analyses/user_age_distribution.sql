SELECT
    age_group,
    COUNT(*) AS users,
    AVG(age) AS average_age,
    MIN(age) AS minimum_age,
    MAX(age) AS maximum_age
FROM {{ ref('dim_users') }}
GROUP BY age_group
ORDER BY age_group;