WITH ranked_users AS (

    SELECT
        CAST(ID AS INTEGER) AS id,
        CAST(NAME AS VARCHAR) AS name,
        CAST(AGE AS INTEGER) AS age,
        CAST(AGE_GROUP AS VARCHAR) AS age_group,
        LOAD_DATE,

        ROW_NUMBER() OVER (
            PARTITION BY ID
            ORDER BY LOAD_DATE DESC
        ) AS row_num

    FROM {{ source('raw', 'users_raw') }}

)

SELECT
    id,
    name,
    age,
    age_group,
    load_date
FROM ranked_users
WHERE row_num = 1