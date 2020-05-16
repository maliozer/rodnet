import mysql.connector

#define host, root,passwd,database inline
def mysql_connector():
    db_con = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="test",
    )
    return db_con

def query_select(mysql_con, limit=100):
    sql_select_Query = "select * from usd_live_data where is_parsed = 0 ORDER BY timestamp_dt LIMIT " + str(limit)
    mycursor = mysql_con.cursor()
    mycursor.execute(sql_select_Query)
    records = mycursor.fetchall()
    result = "Total number of rows in usd_table is: " + str(mycursor.rowcount)
    return records

#insert one by one
def query_insert_live(mysql_con,usd_currency=str(6.14), dt_field = "2020-3-17 5:14:24"):
    date_str = "STR_TO_DATE('"+dt_field+"','%Y-%m-%d %H:%i:%s')"
    sql_insert_date_query = "INSERT INTO usd_live_data (currency_l, timestamp_dt) VALUES ("+usd_currency+", "+date_str+")"
    #INSERT INTO `usd_live_data`(`currency_l`, `timestamp_dt`) VALUES (7, STR_TO_DATE('24-3-2020 5:14:24','%d-%m-%Y %H:%i:%s'))
    mycursor = mysql_con.cursor()
    try:
        mycursor.execute(sql_insert_date_query)
        mysql_con.commit()
    except(RuntimeError, TypeError, NameError):
        print(RuntimeError)

#executemany insert
def query_insert_modeltable(mysql_con, data):
    sql_insert_modelpack = "INSERT INTO usd_5_min (currency_l, date) VALUES (%s, %s)"
    mycursor = mysql_con.cursor()
    try:
        mycursor.executemany(sql_insert_modelpack, data)
        mysql_con.commit()
    except(RuntimeError, TypeError, NameError):
        print(RuntimeError)
