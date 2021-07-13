import mysql.connector
from shashank.notes.spark_submit import run_spark
s=run_spark()


def db_conn(self, app_id, ):
    db = mysql.connector.connect(host='172.36.4.160', port=3317, database='unravel_mysql_prod', user='unravel',
                                 passwd='unraveldata')

    # initiate the cursor
    mycursor = db.cursor()

    # execute the query
    query = mycursor.execute(f"SELECT * FROM {app_id}")

    # fetch results
    result = mycursor.fetchone()
    print(result)