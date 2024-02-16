import pyspark
from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from pyspark.context import SparkContext
from pyspark.sql.functions import monotonically_increasing_id,lit,array_contains,when,col
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
df_scores = spark.read.parquet('gs://shekhar-iq-bucket/data/scores.parquet')
df_time_spent = spark.read.parquet('gs://shekhar-iq-bucket/data/time_spent.parquet')

                                                                                
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


# Creating df_assignment DataFrame with required transformations
df_assignment = df_scores.fillna(0).select(
    monotonically_increasing_id().alias("assignment_id"),
    col("email").alias("email"),
    (col("hw-01a") + col("hw-01b")).alias("hw_m1"),
    col("hw-02").alias("hw_m2"),
    col("hw-03").alias("hw_m3"),
    col("hw-04").alias("hw_m4"),
    col("hw-05").alias("hw_m5"),
    col("hw-06").alias("hw_m6"),
    lit(None).cast("double").alias("hw_w1"),  # Creating a column with NaN values
    lit(None).cast("double").alias("hw_w2"),  # Creating a column with NaN values
    col("hw-piperider").alias("hw_w3"),
    when(col("project-01").isNotNull(), col("project-01")).otherwise(col("project-02")).alias("hw_p")
)

# Show the resulting DataFrame
df_assignment.fillna(0).show()

