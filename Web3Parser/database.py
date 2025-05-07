import psycopg2
#from dotenv import load_dotenv
import json
import os
import datetime
import pytz

#load_dotenv()


DB_HOST = '127.0.0.1'
DB_PORT = '5432'
DB_NAME = 'cryptonaire'
DB_USER = 'postgres'
DB_PASSWORD = '1112'


class Database:

    @staticmethod
    def insert_cryptop2p_dict(data_dict: dict):
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cursor = connection.cursor()

            cursor.execute("delete from cryptop2p_cryptop2p;")
            cursor.execute("SELECT setval(pg_get_serial_sequence('\"cryptop2p_cryptop2p\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cryptop2p_cryptop2p\";")

            cursor.execute("delete from cryptop2p_allcryptop2p;")
            cursor.execute("SELECT setval(pg_get_serial_sequence('\"cryptop2p_allcryptop2p\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cryptop2p_allcryptop2p\";")

            
            is_international = False
            
            for (k, v) in data_dict.items():
                for data in v:
                    try:
                        is_international = str(data['Type']).lower().__contains__('international')
                    except Exception:
                        pass          
                        
                    time_now = datetime.datetime.now(pytz.timezone('Etc/GMT-6'))
                    
                    query = f"INSERT INTO cryptop2p_allcryptop2p (created_at, data, is_international) VALUES (%s, %s, %s);"
            
                    cursor.execute(query,(time_now, json.dumps(data), is_international,))

                    if data['Profit Percentage'][0] != "-":
                        print(data['Profit Percentage'])
                        query = f"INSERT INTO cryptop2p_cryptop2p (created_at, data, is_international) VALUES (%s, %s, %s);"            
                        cursor.execute(query,(time_now, json.dumps(data), is_international,))
                    
            connection.commit()
            
            cursor.close()
            connection.close()
            
        except (Exception, psycopg2.Error) as error:
            print("Error executing queries:", error)


    @staticmethod
    def insert_other(data_list: list, type: str):
        try:
            connection = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            query = ''
            cursor = connection.cursor()

            if type == 'exchange':                    
                cursor.execute("delete from cryptop2p_exchange;")
                cursor.execute("SELECT setval(pg_get_serial_sequence('\"cryptop2p_exchange\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cryptop2p_exchange\";")                
            elif type == 'fiat':
                cursor.execute("delete from cryptop2p_fiat;")
                cursor.execute("SELECT setval(pg_get_serial_sequence('\"cryptop2p_fiat\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cryptop2p_fiat\";")                
            elif type == 'bank':
                cursor.execute("delete from cryptop2p_bank;")
                cursor.execute("SELECT setval(pg_get_serial_sequence('\"cryptop2p_bank\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cryptop2p_bank\";")
            elif type == 'asset':
                cursor.execute("delete from cryptop2p_asset;")
                cursor.execute("SELECT setval(pg_get_serial_sequence('\"cryptop2p_asset\"','id'), coalesce(max(\"id\"), 1), max(\"id\") IS NOT null) FROM \"cryptop2p_asset\";")                
        
            for data in data_list:
                time_now = datetime.datetime.now(pytz.timezone('Etc/GMT-6'))
                 
                if type == 'exchange':                    
                    query = f"INSERT INTO cryptop2p_exchange (created_at, name) VALUES (%s, %s);"                    
                elif type == 'fiat':
                    query = f"INSERT INTO cryptop2p_fiat (created_at, name) VALUES (%s, %s);"                    
                elif type == 'bank':
                    query = f"INSERT INTO cryptop2p_bank (created_at, name) VALUES (%s, %s);"                    
                elif type == 'asset':
                    query = f"INSERT INTO cryptop2p_asset (created_at, name) VALUES (%s, %s);"
                    
                cursor.execute(query,(time_now, data,))

            connection.commit()
                        
            cursor.close()
            connection.close()
            
        except (Exception, psycopg2.Error) as error:
            print("Error executing queries:", error)
                
                
        
       
