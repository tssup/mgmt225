from venv import create
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
import os
import numpy as np
import time

gcloudhostname = os.getenv("gcloudhostname")
gclouddb_name = os.getenv("gclouddb_name")
gcloudusername = os.getenv("gcloudusername")
gcloudpassword = os.getenv("gcloudpassword")


engine = create_engine("mysql+pymysql://{user}:{pw}@{host}/{db}"
                        .format(host=gcloudhostname, db=gclouddb_name, user=gcloudusername, pw=gcloudpassword))

try:
    engine.connect()
    print("success")
except SQLAlchemyError as err:
    print("error", err.__cause__)
connection = engine.connect()

def sql_data_frame(query, connection):
    
    sql_query = pd.read_sql_query(query, connection)
    df = pd.DataFrame(sql_query)
    return df


if __name__ == "__main__":
    
    while True:
        df = sql_data_frame("SELECT * FROM orders", connection)
        df['Order Date'] = pd.to_datetime(df['Order Date'])
        df['Shipped Date'] = pd.to_datetime(df['Shipped Date'])
        if df.size:
            delete_query = 'DELETE FROM orders'
            connection.execute(delete_query)

            csv_df = pd.read_csv("stream_orders.csv", encoding='cp1252')
            magic_val = np.random.randint(0, 367)
            magic_val_plus_one = magic_val + 1

            csv_df_row = csv_df[csv_df.columns].iloc[magic_val:magic_val_plus_one, :]
            csv_df_row['Order ID'] = np.random.randint(2000, 50000)
            csv_df_row['Quantity'] = np.random.randint(1, 100)
            csv_df_row['Revenue'] = csv_df['Quantity']*csv_df['Unit Price']
            csv_df_row['Shipping Fee'] = round(np.random.uniform(20, 200), 1)
            csv_df_row['Order Date']  = pd.to_date(csv_df_row['Order Date'])
            csv_df_row['Shipped Date']  = pd.to_date(csv_df_row['Shipped Date'])

            df.to_sql(con=connection, name='orders', if_exists='append', index=False)
            csv_df_row.to_sql(con=connection, name='orders', if_exists='append', index=False)
            
            print('inserting into the table orders ........ \n')
            time.sleep(1)
            print(csv_df_row)
            print('\n')
            time.sleep(2)