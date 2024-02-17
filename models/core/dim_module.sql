-- dimension_module.sql

-- Use the `source` block to define the source table from the Spark DataFrame
-- It is assumed that you have a source YAML file (e.g., profiles.yml) with the Spark connection details

{{ config(
    materialized='table',
    unique_key='module_id'
) }}

-- Create a temporary table for the module data
WITH module_data AS (
    SELECT 
        module_id,
        module_name
    FROM (VALUES 
        ('m1', 'Containerization and Infrastructure as Code'),
        ('m2', 'Workflow Orchestration'),
        ('m3', 'Data Warehouse'),
        ('m4', 'Analytics Engineering'),
        ('m5', 'Batch processing'),
        ('m6', 'Streaming'),
        ('w1', 'Data Ingestion'),
        ('w2', 'Stream Processing with SQL'),
        ('w3', 'Piperider'),
        ('p', 'Project')
    ) AS t (module_id, module_name)
)

-- Create a temporary table for the module-instructor mapping
, module_instructor_data AS (
    SELECT 
        module_id,
        explode(instructor_ids) as instructor_id
    FROM (VALUES 
        ('m1', array(-6, -5, -3)),
        ('m2', array(-4)),
        ('w1', array(-8)),
        ('m3', array(-1)),
        ('m4', array(-2)),
        ('m5', array(-3)),
        ('m6', array(-1, -7)),
        ('w2', array(-9)),
        ('p', array(-10)),
        ('w3', array(-10))
    ) AS t (module_id, instructor_ids)
)

-- Create the final module dimension table
SELECT 
    m.module_id,
    m.module_name,
    i.instructor_id
FROM module_data m
LEFT JOIN module_instructor_data i
ON m.module_id = i.module_id;
