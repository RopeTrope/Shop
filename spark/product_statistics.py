import json
from pyspark.sql import SparkSession

from pyspark.sql import functions as F

builder = SparkSession.builder \
    .appName("MySQL connection") \
    .config("spark.jars", "/app/mysql-connector-j-9.3.0.jar" )

spark = builder.getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

product_df = spark.read \
    .format ("jdbc") \
    .option ( "url", "jdbc:mysql://db_shop:3306/Shop" ) \
    .option ( "dbtable" , "products") \
    .option ( "user", "user" ) \
    .option ( "password", "user" ) \
    .load ( )


order_df = spark.read \
    .format ("jdbc") \
    .option ( "url", "jdbc:mysql://db_shop:3306/Shop" ) \
    .option ( "dbtable" , "orders") \
    .option ( "user", "user" ) \
    .option ( "password", "user" ) \
    .load ( )


order_product_df = spark.read \
    .format ("jdbc") \
    .option ( "url", "jdbc:mysql://db_shop:3306/Shop" ) \
    .option ( "dbtable" , "order_product") \
    .option ( "user", "user" ) \
    .option ( "password", "user" ) \
    .load ( )

df_sold = product_df.join(order_product_df,product_df["id"] == order_product_df["product_id"]) \
    .join(order_df, order_product_df["order_id"] == order_df["id"]) \
    .filter(order_df['status'] == "COMPLETED") \
    .groupBy(product_df['name'])\
    .agg(F.sum('quantity').alias('sold')).alias('sold')

df_waiting = product_df.join(order_product_df,product_df["id"] == order_product_df["product_id"]) \
    .join(order_df, order_product_df["order_id"] == order_df["id"]) \
    .filter(order_df['status'] != "COMPLETED") \
    .groupBy(product_df['name'])\
    .agg(F.sum('quantity').alias('waiting')).alias('waiting')


df_sold = df_sold.withColumnRenamed('name','sold_name')
df_waiting = df_waiting.withColumnRenamed('name','waiting_name')


result = df_sold.join(df_waiting, df_waiting['waiting_name'] == df_sold["sold_name"],'left') \
    .select(F.coalesce(df_sold['sold_name'], df_waiting['waiting_name']).alias('name'),
            (df_sold['sold']).alias('sold'),
            F.coalesce(df_waiting['waiting'], F.lit(0)).alias('waiting')).collect()


result_json = {
    "statistics": [
        {
            "name": product.name,
            "sold": product.sold,
            "waiting": product.waiting
        }for product in result
    ] 
}

with open("/app/result.json","w") as f:
    json.dump(result_json,f)


spark.stop()
