import json
from pyspark.sql import SparkSession

from pyspark.sql import functions as F

builder = SparkSession.builder \
    .appName("MySQL connection") \
    .config("spark.jars", "/app/mysql-connector-j-9.3.0.jar" )

spark = builder.getOrCreate()
spark.sparkContext.setLogLevel('ERROR')

category_df = spark.read \
    .format ("jdbc") \
    .option ( "url", "jdbc:mysql://db_shop:3306/Shop" ) \
    .option ( "dbtable" , "categories") \
    .option ( "user", "user" ) \
    .option ( "password", "user" ) \
    .load ( )

product_df =  spark.read \
    .format ("jdbc") \
    .option ( "url", "jdbc:mysql://db_shop:3306/Shop" ) \
    .option ( "dbtable" , "products") \
    .option ( "user", "user" ) \
    .option ( "password", "user" ) \
    .load ( )

product_category_df = spark.read \
    .format ("jdbc") \
    .option ( "url", "jdbc:mysql://db_shop:3306/Shop" ) \
    .option ( "dbtable" , "product_category") \
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


result = category_df.join(product_category_df, product_category_df['category_id'] == category_df["id"]) \
    .join(product_df, product_category_df['product_id'] == product_df['id']) \
    .join(order_product_df, order_product_df['product_id'] == product_df['id']) \
    .join(order_df, order_product_df['order_id'] == order_df['id']) \
    .filter(order_df['status'] == "COMPLETED") \
    .groupBy(category_df['name']) \
    .agg(F.sum('quantity').alias('sold')).sort('sold',category_df['name'],ascending=[False,True]).collect()

print(result)

result_json = {
    "statistics": [
        {
            "name": category.name,
            "sold": category.sold
        }for category in result
    ] 
}

with open("/app/result2.json","w") as f:
    json.dump(result_json,f)

    

spark.stop()
