                                                                                     
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, DoubleType, StringType
from pyspark.sql.functions import col, udf
import h3
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, TimestampType

spark = SparkSession.builder.appName("RawRidesExample").config("hive.metastore.uris", "thrift://hive-metastore:9083").enableHiveSupport().getOrCreate()
spark.sql("SHOW DATABASES").show()

schema = StructType([
    StructField("trip_id", IntegerType(), True),
    StructField("start_lat", DoubleType(), True),
    StructField("start_lon", DoubleType(), True),
    StructField("end_lat", DoubleType(), True),
    StructField("end_lon", DoubleType(), True),
    StructField("start_time", TimestampType(), True),
    StructField("end_time", TimestampType(), True),
    StructField("distance", DoubleType(), True)
])

rides_df = spark.read.csv("hdfs://localhost:9000/staging_zone/uber_rides", schema=schema, inferSchema=True)

def latlng_to_h3(lat, lon):
    return h3.latlng_to_cell(lat, lon, 9)

latlng_to_h3_udf = udf(latlng_to_h3, StringType())
rides_df = rides_df.withColumn("start_geo_hash", latlng_to_h3_udf(rides_df["start_lat"], rides_df["start_lon"]))
rides_df = rides_df.withColumn("end_geo_hash", latlng_to_h3_udf(rides_df["end_lat"], rides_df["end_lon"]))

result = rides_df.select('trip_id', 'start_time', 'start_geo_hash','end_geo_hash', (col('end_time').cast('long') - col('start_time').cast('long')).alias('duration'))
result.write.mode("overwrite").saveAsTable("uber_db.Staging_Rides_Geo")