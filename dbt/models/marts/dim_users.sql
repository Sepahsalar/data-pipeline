SELECT
    id,
    name,
    age,
    age_group,

    CASE
        WHEN age >= 18 THEN TRUE
        ELSE FALSE
    END AS is_adult,

    load_date

FROM {{ ref('stg_users') }}