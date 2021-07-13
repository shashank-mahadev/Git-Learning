#  install mysql connector
# pip install mysql-connector

import pymysql
import mysql.connector
db = mysql.connector.connect(host='172.36.4.160', port=3317, database='unravel_mysql_prod', user='unravel', passwd='unraveldata')

# initiate the cursor
mycursor = db.cursor()

# execute the query
query=mycursor.execute(f"SELECT * FROM {'users'}")


# fetch results
result=mycursor.fetchone()
print(result)
# close the cursor
# mycursor.close()
# # close db connection
# db.close()


# print(dir(mysql))
# print(dir(pymysql))


# sql injection attack - this will mess up the database because proper escape dont happen. always good to add data using a tuple
# Examples:::::::
# query=mycursor.execute("INSERT INTO workflows VALUES (?, ?, ?)", ('employee1', 'employee2', 'employee3',))
# query=mycursor.execute("INSERT INTO workflows VALUES where NAME=%s", ("shashank",))

