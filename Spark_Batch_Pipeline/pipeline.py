import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.functions import monotonically_increasing_id,lit,array_contains,when,col
from pyspark.sql.types import *
credentials_location = './docker/mage/google-cred.json'

conf = SparkConf() \
    .setMaster('local[*]') \
    .setAppName('test') \
    .set("spark.jars", "./data/gcs-connector-hadoop3-2.2.5.jar") \
    .set("spark.hadoop.google.cloud.auth.service.account.enable", "true") \
    .set("spark.hadoop.google.cloud.auth.service.account.json.keyfile", credentials_location)
sc = SparkContext(conf=conf)

hadoop_conf = sc._jsc.hadoopConfiguration()

hadoop_conf.set("fs.AbstractFileSystem.gs.impl",  "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFS")
hadoop_conf.set("fs.gs.impl", "com.google.cloud.hadoop.fs.gcs.GoogleHadoopFileSystem")
hadoop_conf.set("fs.gs.auth.service.account.json.keyfile", credentials_location)
hadoop_conf.set("fs.gs.auth.service.account.enable", "true")


spark = SparkSession.builder \
    .config(conf=sc.getConf()) \
    .getOrCreate()

gcs_bucket_path='gs://shekhar-iq-bucket/'

df_scores = spark.read.parquet(gcs_bucket_path+'data/scores.parquet')
df_time_spent = spark.read.parquet(gcs_bucket_path+'data/time_spent.parquet')

                                                                                
df_scores.printSchema()


df_user = df_time_spent.withColumn("user_id", monotonically_increasing_id()).\
                        withColumn("user_type", lit("student")).\
                        select('user_id','email','user_type')

# Add user_type column with default value 'student'
# df_user.show()

# Filter emails for instructor user type
instructor_emails = ["Ankush_Khanna", "Victoria_Perez_Mola", "Alexey_Grigorev", "Matt_Palmer", "Luis_Oliveira", "Michael_Shoemaker", "Irem_Erturk","Adrian_Brudaru","RisingWave","CL_Kao","Self"]

# Extract email domains and create list of tuples with negative loop index as user_id
instructor_data = [(-i, email, "instructor") for i, email in enumerate(instructor_emails, start=1)]
print(instructor_data)

# Create DataFrame for instructor emails
df_instructor_emails = spark.createDataFrame(instructor_data, ["user_id", "email", "user_type"])

# Union the instructor emails DataFrame with the original DataFrame
df_user = df_user.union(df_instructor_emails)

instructor_df = df_user.filter(df_user.user_type == "instructor")

# instructor_df.show()

module_names=["Containerization and Infrastructure as Code","Workflow Orchestration","Data Warehouse","Analytics Engineering","Batch processing","Streaming","Data Ingestion","Stream Processing with SQL","Piperider","Project"]
module_id=["m1","m2","m3","m4","m5","m6","w1","w2","w3","p"]


# Create DataFrame for modules
df_module = spark.createDataFrame(zip(module_id, module_names), schema=["module_id", "module_name"])


# Define the mapping of module IDs to instructor user IDs
module_instructor_mapping = {'m1': [-6, -5, -3],'m2': [-4],'w1': [-8],'m3': [-1],'m4': [-2],'m5': [-3],'m6': [-1, -7],'w2': [-9],'p': [-10],'w3': [-10]}

# Create DataFrame for module names and IDs
df_module = spark.createDataFrame(zip(module_id, module_names), schema=["module_id", "module_name"])

# Create DataFrame for module instructor mapping
module_instructor_df = spark.createDataFrame(module_instructor_mapping.items(), schema=["module_id", "instructor_ids"])

# Join df_module with module_instructor_df to add instructor_id column
df_module_with_instructor_id = df_module.join(module_instructor_df, on="module_id", how="left")


# Show the modified df_module DataFrame
# df_module_with_instructor_id.show()


# df_time_spent.printSchema()

time_schema = StructType([
    StructField("email", StringType(), True),
    StructField("homework_m1", DoubleType(), True),
    StructField("lectures_m1", DoubleType(), True),
    StructField("homework_m2", DoubleType(), True),
    StructField("lectures_m2", DoubleType(), True),
    StructField("homework_m3", DoubleType(), True),
    StructField("lectures_m3", DoubleType(), True),
    StructField("homework_m4", DoubleType(), True),
    StructField("lectures_m4", DoubleType(), True),
    StructField("homework_m5", DoubleType(), True),
    StructField("lectures_m5", DoubleType(), True),
    StructField("homework_m6", DoubleType(), True),
    StructField("lectures_m6", DoubleType(), True),
    StructField("homework_w3", DoubleType(), True),
    StructField("p_eval_time", DoubleType(), True),
    StructField("p_sub_time", DoubleType(), True),
 
])

df_time_spent = df_time_spent.fillna(0).select(
    col('email'),
    (col('time_homework')+col('time_homework_homework-01b')).alias('homework_m1'),
    (col('time_lectures')+col('time_lectures_homework-01b')).alias('lectures_m1'),
    col('time_homework_homework-02').alias('homework_m2'),
    col('time_lectures_homework-02').alias('lectures_m2'),
    col('time_homework_homework-03').alias('homework_m3'),
    col('time_lectures_homework-03').alias('lectures_m3'),
    col('time_homework_homework-04').alias('homework_m4'),
    col('time_lectures_homework-04').alias('lectures_m4'),
    col('time_homework_homework-05').alias('homework_m5'),
    col('time_lectures_homework-05').alias('lectures_m5'),
    col('time_homework_homework-06').alias('homework_m6'),
    col('time_lectures_homework-06').alias('lectures_m6'),
    col('time_homework_homework-piperider').alias('homework_w3'),
    (col('time_evaluate')+col('time_evaluate_project-02-eval')).alias('p_eval_time'),
    (col('time_project')+col('time_project_project-02-submissions')).alias('p_sub_time')
).select([col(c).cast(time_schema[c].dataType) for c in time_schema.fieldNames()])

# df_time_spent.printSchema()

df_scores=df_scores.fillna(0).select(
    col('email'),
    (col('hw-01a')+col('hw-01b')).alias('hw_m1'),
    col('hw-02').alias('hw_m2'),
    col('hw-03').alias('hw_m3'),
    col('hw-04').alias('hw_m4'),
    col('hw-05').alias('hw_m5'),
    col('hw-06').alias('hw_m6'),
    col('hw-piperider').alias('hw_w3'),
    (col('project-01')+col('project-02')).alias('p')
)

# df_scores.printSchema()


# Create Scores Fact Table

fact_scores = df_scores.selectExpr("email", "stack(8, 'm1', hw_m1, 'm2', hw_m2, 'm3', hw_m3, 'm4', hw_m4, 'm5', hw_m5, 'm6', hw_m6, 'w3', hw_w3, 'p_sub', p) as (module_id, score)").\
                        filter(df_scores.email.isNotNull())

# fact_scores.show()


fact_time =df_time_spent.selectExpr(
    'email',
    "stack(9, 'm1', homework_m1 , lectures_m1,'m2', homework_m2 , lectures_m2,'m3', homework_m3 , lectures_m3,'m4', homework_m4 , lectures_m4,'m5', homework_m5 , lectures_m5,'m6', homework_m6 , lectures_m6,'w3',homework_w3,NULL,'p_eval',p_eval_time,NULL,'p_sub',p_sub_time,NULL) as (module_id,time_homework,time_lectures)"
)

# Filter out null module names
fact_time = fact_time.filter(col("module_id").isNotNull())
# Show output DataFrame
# fact_time.show()

# # Add user_id column and make it primary_key
# df_user = df_time_spent.withColumn("user_id", monotonically_increasing_id()).\
#                         withColumn("user_type", lit("student")).\
#                         select('user_id','email','user_type')

# # Add user_type column with default value 'student'
# # df_user.show()

# # Filter emails for instructor user type
# instructor_emails = ["@Ankush_Khanna.com", "@Victoria_Perez_Mola.com", "@Alexey_Grigorev.com", "@Matt_Palmer.com", "@Luis_Oliveira.com", "@Michael_Shoemaker.com", "@Irem_Erturk.com", "@Adrian_Brudaru.com", "To_be_named" ,"@CL_Kao.com", "Self"]

# # Extract email domains and create list of tuples with negative loop index as user_id
# instructor_data = [(-i, email, "instructor") for i, email in enumerate(instructor_emails, start=1)]

# # Create DataFrame for instructor emails
# df_instructor_emails = spark.createDataFrame(instructor_data, ["user_id", "email", "user_type"])

# # Union the instructor emails DataFrame with the original DataFrame
# df_user = df_user.union(df_instructor_emails)

# instructor_df = df_user.filter(df_user.user_type == "instructor")

# # instructor_df.show()

# # Define module names and IDs
# module_names = ['Containerization and Infrastructure as Code','Workflow Orchestration','Data Ingestion', 'Data Warehouse','Analytics Engineering','Batch processing' ,'Streaming' ,'Stream Processing with SQL', 'Project_Evaluation' , 'Project_Submission', 'Piperider']
# module_id = ['m1','m2','w1','m3','m4','m5','m6','w2','p_eval','p_sub','w3']

# # Create DataFrame for modules
# df_module = spark.createDataFrame(zip(module_id, module_names), schema=["module_id", "module_name"])


# # Define the mapping of module IDs to instructor user IDs
# module_instructor_mapping = {'m1': [-6, -5, -3],'m2': [-4],'w1': [-8],'m3': [-1],'m4': [-2],'m5': [-3],'m6': [-1, -7],'w2': [-9],'p_eval': [-11],'p_sub': [-11],'w3': [-10]}

# # Create DataFrame for module names and IDs
# df_module = spark.createDataFrame(zip(module_id, module_names), schema=["module_id", "module_name"])

# # Create DataFrame for module instructor mapping
# module_instructor_df = spark.createDataFrame(module_instructor_mapping.items(), schema=["module_id", "instructor_ids"])

# # Join df_module with module_instructor_df to add instructor_id column
# df_module = df_module.join(module_instructor_df, on="module_id", how="left")


# Show the modified df_module DataFrame
# df_module.show()

# Show dataframes
df_user.show()
df_module.show()
fact_scores.show()
fact_time.show()



# Write df_module to GCS as Parquet
df_module.write.parquet(gcs_bucket_path + "transformed_data/df_module.parquet", mode="overwrite")

# Write df_user to GCS as Parquet
df_user.write.parquet(gcs_bucket_path + "transformed_data/df_user.parquet", mode="overwrite")

# Write fact_time to GCS as Parquet
fact_time.write.parquet(gcs_bucket_path + "transformed_data/fact_time.parquet", mode="overwrite")

# Write fact_scores to GCS as Parquet
fact_scores.write.parquet(gcs_bucket_path + "transformed_data/fact_scores.parquet", mode="overwrite")
