import sqlite3

class Database(object):

    def __init__(self, db_path):
        self.db_conn = sqlite3.connect(db_path)
        self.c = self.db_conn.cursor()
        
    def __del__(self): 
        self.c.close() 
        self.db_conn.close()
        print("Connection to DB closed")
        
    def create_table(self):
        try:
            self.c.execute("""CREATE TABLE IF NOT EXISTS  Users (
            UserID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            First TEXT NOT NULL,
            Last TEXT NOT NULL,
            Path TEXT NOT NULL,
            Status TEXT NOT NULL
            );""")
        except sqlite3.Error as e:
            print(e)
            
    def insert_data(self,first, last, path, status="Unknown"):
        try:
            self.create_table()
            self.c.execute("""INSERT INTO Users (First, Last, Path, Status) VALUES (?,?,?,?)""", (first, last, path, status))
            self.db_conn.commit()
            print("User {} {} added into database".format(first, last)) 
        except sqlite3.Error as e:
            print(e)
            
    def get_name(self, userid):
        try:
            cursor = self.c.execute("""SELECT First, Last FROM Users WHERE UserID=?;""", (userid))
            profile = None
            for row in cursor:
                profile = row
            #user = self.c.fetchall()
            return profile
        except sqlite3.Error as e:
            print(e)
       
    def get_id(self, first, last):
        try:
            cursor = self.c.execute("""SELECT UserID FROM Users WHERE First=? AND Last=?;""", (first, last)) 
            profile = None
            for row in cursor:
                profile = row
            return profile
        except sqlite3.Error as e:
            print(e)    