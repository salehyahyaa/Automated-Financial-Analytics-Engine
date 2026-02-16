import psycopg2                                  #contains connection object
import os 
from dotenv import load_dotenv
load_dotenv()
"""
Connecting program to existing database 
"""


class Connection:

                                                    #to connect to the db, we need the host, port, user, password, and database WHY:
                                                    # DB && the value's must come from .env file ALWAYS 
    def __init__(self):                             #because we are getting the data from .env file we dont need to include the objects within the constructor's signature
        self.host = os.getenv("DB_HOST")
        self.port = int(os.getenv("DB_PORT"))                        # Convert to int since .env values are strings
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
        self.connection = None                                       # Store connection as instance variable


    def get_connection(self):                                        # gets the connection to the db 
        if self.connection is None:                                  # If connection already exists and is open, reuse it.
            try:
            # Why: Local variables disappear after method ends. We need to keep connection alive for reuse.
                self.connection = psycopg2.connect(     
                    host = self.host,
                    port = self.port,
                    user = self.user,
                    password = self.password,
                    database = self.database
                )
            except psycopg2.Error as e:                              #raise's exception to let caller know connection failed silent failures are dangerous. Caller needs to know if connection didnt work.
                raise Exception(f"Connection to DB Failed: {e}")
        elif self.connection.closed:
            # Reconnect if connection was closed (e.g., by database timeout) # Why: Closed connections can't be used. We need to create a new one.
            try:
                self.connection = psycopg2.connect(     
                    host = self.host,
                    port = self.port,
                    user = self.user,
                    password = self.password,
                    database = self.database
                )
            except psycopg2.Error as e:
                raise Exception(f"Connection to DB Failed: {e}")
        #Method should return the connection object for convenience (even though it's also stored in self.connection)
        return self.connection


    def cursor(self):                                             # cursor is what you use to traverse through the db based on ur queries and fetch a response to you
        try:
            if self.connection is None or self.connection.closed: # WHY: If self.connection is None, calling .cursor() on None will crash with AttributeError
                self.get_connection()                             # We can't create a cursor without an active connection
            cursor = self.connection.cursor()
            return cursor
        except psycopg2.Error as e:
            raise Exception(f"Failed to create cursor: {e}")      # psycopg2.Error tells us it's a database problem, not a Python code problem
    
    
    def close_connection(self):
        if self.connection and not self.connection.closed:        # Check if connection exists and is not already closed
            self.connection.close()                         
        self.connection = None                                    # Set to None after closing






"""
you can also think of connection as requests to the database, 
if we dont close the connection at the end the connection will stay open 
and besides it taking up memeory once we reach 100 requested connections to the database, postgres will start to reject 
ecause each prev connection stays alive and within the database so we need to close the connection everytime we open it
"""
