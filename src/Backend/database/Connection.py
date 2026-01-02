"""
Connecting program to existing database 
"""
import psycopg2                                  #contains connection object
import os 
from dotenv import load_dotenv
load_dotenv()


class Connection:

                                                #to connect to the db, we need the host, port, user, password, and 
                                                # DB && the value's must come from .env file ALWAYS 
    def __init__(self):                         #because we are getting the data from .env file we dont need to include the objects within the constructor's signature
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")

                                                # function that acctually gets the connection to the db 
    def get_connection(self):
        try:
            connection = psycopg2.connect(     
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                database = self.database
                    )
            return connection
        except psycopg2.Error as e:
            raise Exception (f"Connection to DB Failed: {e}")
                ...

    



            
