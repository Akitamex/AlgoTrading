import psycopg2
from psycopg2 import pool
import json
import os
import datetime
import pytz

DB_HOST = '127.0.0.1'
DB_PORT = '5432'
DB_NAME = 'cryptonaire'
DB_USER = 'postgres'
DB_PASSWORD = '1112'


class Database:

    @staticmethod
    def insert_cardless_dict(data: list, is_international=False):        
        connection_pool = psycopg2.pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )        
        connection = connection_pool.getconn()
        try:
            cursor = connection.cursor()
            if is_international:                           
                cursor.execute("delete from cardless_intercardless;")
                cursor.execute("SELECT setval(pg_get_serial_sequence('\"cardless_intercardless\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cardless_intercardless\";") 
            else:
                cursor.execute("delete from cardless_intracardless;")
                cursor.execute("SELECT setval(pg_get_serial_sequence('\"cardless_intracardless\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cardless_intracardless\";")                
            
            for item in data:
                with connection.cursor() as cursor:                  
                    time_now = datetime.datetime.now(pytz.timezone('Etc/GMT-6'))
                    query = ''
                    if is_international:                           
                        query = f"INSERT INTO cardless_intercardless (created_at, data) VALUES (%s, %s);"
                    else:
                        query = f"INSERT INTO cardless_intracardless (created_at, data) VALUES (%s, %s);"
                    cursor.execute(query,(time_now, json.dumps(item),))            
            connection.commit()  # Commit changes at the end of the loop
        except Exception as e:
            connection.rollback()  # Rollback if there's an error
            print(f"Error occurred: {e}")
        finally:
            connection_pool.putconn(connection)
                        
      
    @staticmethod
    def insert_exchange(data: str):
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()
                        
            query = f"INSERT INTO cardless_exchange (name) VALUES (%s);"
            
            cursor.execute(query,(data,))
            connection.commit()
            
            cursor.close()
            connection.close()
            
        except (Exception, psycopg2.Error) as error:
            print(f"Error inserting data: {data}", error)
    
        
            
    @staticmethod
    def exchange_to_db(data: list):
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()
                       
            cursor.execute("delete from cardless_exchange;")
            cursor.execute("SELECT setval(pg_get_serial_sequence('\"cardless_exchange\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cardless_exchange\";")
                        
            connection.commit()
            
            cursor.close()
            connection.close()
            print("Exchanges cleared")
            
        except (Exception, psycopg2.Error) as error:
            print(f"Error deleting data: {data}", error)
       
        for d in data:
            Database.insert_exchange(d)
            
    @staticmethod        
    def symbols_from_db():
        symbols = []
        order_sizes = {}
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()
                       
            cursor.execute("select * from cardless_symbol;")
            
            results = cursor.fetchall()
            
            for row in results:
                symbols.append(row[1])
                order_sizes[row[1]] = float(row[2])
            
            cursor.close()
            connection.close()
            
            result = {}
            result['symbols'] = symbols
            result['order_sizes'] = order_sizes
            
            return result
            
        except (Exception, psycopg2.Error) as error:
            print(f"Error retrieving data:", error)
