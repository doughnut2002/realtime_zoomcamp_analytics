-- fact_scores.sql

-- Use the `source` block to define the source table from the PySpark DataFrame
-- It is assumed that you have a source YAML file (e.g., profiles.yml) with the PySpark connection details

{{ config(
    materialized='table',
    unique_key='email'
) }}

-- Create a temporary table for the scores data
WITH scores_data AS (
    SELECT 
        email,
        COALESCE(hw-01a + hw-01b, 0) as hw_m1,
        COALESCE(hw-02, 0) as hw_m2,
        COALESCE(hw-03, 0) as hw_m3,
        COALESCE(hw-04, 0) as hw_m4,
        COALESCE(hw-05, 0) as hw_m5,
        COALESCE(hw-06, 0) as hw_m6,
        COALESCE(hw-piperider, 0) as hw_w3,
        COALESCE(project-01 + project-02, 0) as p
    FROM {{ ref('df_scores') }}
)

-- Create the fact_scores table
WITH fact_scores_data AS (
    SELECT 
        email,
        stack(8, 'm1', hw_m1, 'm2', hw_m2, 'm3', hw_m3, 'm4', hw_m4, 'm5', hw_m5, 'm6', hw_m6, 'w3', hw_w3, 'p_sub', p) as (module_id, score)
    FROM scores_data
)

-- Filter out rows with null email
SELECT 
    email,
    module_id,
    score
FROM fact_scores_data
WHERE email IS NOT NULL;
