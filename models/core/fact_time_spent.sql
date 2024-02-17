-- fact_time_spent.sql

-- Use the `source` block to define the source table from the Spark DataFrame
-- It is assumed that you have a source YAML file (e.g., profiles.yml) with the Spark connection details

{{ config(
    materialized='table',
    unique_key='email'
) }}

-- Create a temporary table for the time_spent data
WITH time_spent_data AS (
    SELECT 
        email,
        COALESCE(time_homework + time_homework_homework-01b, 0) as homework_m1,
        COALESCE(time_lectures + time_lectures_homework-01b, 0) as lectures_m1,
        COALESCE(time_homework_homework-02, 0) as homework_m2,
        COALESCE(time_lectures_homework-02, 0) as lectures_m2,
        COALESCE(time_homework_homework-03, 0) as homework_m3,
        COALESCE(time_lectures_homework-03, 0) as lectures_m3,
        COALESCE(time_homework_homework-04, 0) as homework_m4,
        COALESCE(time_lectures_homework-04, 0) as lectures_m4,
        COALESCE(time_homework_homework-05, 0) as homework_m5,
        COALESCE(time_lectures_homework-05, 0) as lectures_m5,
        COALESCE(time_homework_homework-06, 0) as homework_m6,
        COALESCE(time_lectures_homework-06, 0) as lectures_m6,
        COALESCE(time_homework_homework-piperider, 0) as homework_w3,
        COALESCE(time_evaluate + time_evaluate_project-02-eval, 0) as p_eval_time,
        COALESCE(time_project + time_project_project-02-submissions, 0) as p_sub_time
    FROM {{ ref('time_spent') }}
)

-- Use the `SELECT` block to create the final fact_time_spent table
SELECT 
    email,
    homework_m1,
    lectures_m1,
    homework_m2,
    lectures_m2,
    homework_m3,
    lectures_m3,
    homework_m4,
    lectures_m4,
    homework_m5,
    lectures_m5,
    homework_m6,
    lectures_m6,
    homework_w3,
    p_eval_time,
    p_sub_time
FROM time_spent_data;

-- Create the fact_time table
WITH fact_time_data AS (
    SELECT 
        email,
        stack(9, 'm1', homework_m1 , lectures_m1,'m2', homework_m2 , lectures_m2,'m3', homework_m3 , lectures_m3,'m4', homework_m4 , lectures_m4,'m5', homework_m5 , lectures_m5,'m6', homework_m6 , lectures_m6,'w3',homework_w3,NULL,'p_eval',p_eval_time,NULL,'p_sub',p_sub_time,NULL) as (module_id,time_homework,time_lectures)
    FROM time_spent_data
)

-- Filter out null module names
SELECT 
    email,
    module_id,
    time_homework,
    time_lectures
FROM fact_time_data
WHERE module_id IS NOT NULL;
