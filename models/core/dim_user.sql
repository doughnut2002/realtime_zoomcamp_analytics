-- dim_user.sql

-- Use the `source` block to define the source table from the Spark DataFrame
-- It is assumed that you have a source YAML file (e.g., profiles.yml) with the Spark connection details

{{ config(
    materialized='table',
    unique_key='user_id'
) }}

WITH user_data AS (
    SELECT 
        monotonically_increasing_id() as user_id,
        email,
        'student' as user_type
    FROM {{ ref('time_spent') }}
    
    UNION ALL
    
    SELECT 
        -1 as user_id, 'Ankush_Khanna' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -2 as user_id, 'Victoria_Perez_Mola' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -3 as user_id, 'Alexey_Grigorev' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -4 as user_id, 'Matt_Palmer' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -5 as user_id, 'Luis_Oliveira' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -6 as user_id, 'Michael_Shoemaker' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -7 as user_id, 'Irem_Erturk' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -8 as user_id, 'Adrian_Brudaru' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -9 as user_id, 'RisingWave' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -10 as user_id, 'CL_Kao' as email, 'instructor' as user_type
    UNION ALL
    SELECT 
        -11 as user_id, 'Self' as email, 'instructor' as user_type
)

-- Use the `SELECT` block to create the final user dimension table
SELECT 
    user_id,
    email,
    user_type
FROM user_data;
