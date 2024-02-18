import pyspark.sql.types as T

BOOTSTRAP_SERVERS = 'localhost:9092'
TOPIC = 'shekhar-iq-form-submissions'
STREAM_SCHEMA = T.StructType(
    [T.StructField("module_id", T.IntegerType()),
     T.StructField('module_name', T.StringType()),
     T.StructField("email", T.StringType()),
     T.StructField('time_homework', T.FloatType()),
     T.StructField("time_lectures", T.FloatType()),
     T.StructField("score", T.FloatType())
     ])

