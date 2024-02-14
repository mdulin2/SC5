import sqlite3
from abstract_database_connection import AbstractDatabaseConnection

def create_table():
    # Holds the state of all the phone calls
    con = sqlite3.connect("search.db") 
    cur = con.cursor()
    cur.execute(
        "DROP TABLE IF EXISTS search; "
    )
    cur.execute(
        "DROP TABLE IF EXISTS flag;"
    )
    
    cur.execute(
        """
        CREATE TABLE search(
            letter VARCHAR(36), -- UUID of the call
            info TEXT, 
            PRIMARY KEY (letter)
        );
        """
    )

    cur.execute(
        """
        CREATE TABLE flag(
            id INT, 
            flag TEXT,
            PRIMARY KEY (id)
        );
        """
    )

# Add testing data
def addData():

    con = sqlite3.connect("search.db") 
    cur = con.cursor()

    flagfile = open("/flags/flag4.txt", 'r')
    flag = flagfile.read()
    cur.execute(
        "INSERT INTO flag(id, flag) VALUES(1,?)", [flag]
	)

    con.commit()

# Go through the database
def searchDb(query):
    
    with AbstractDatabaseConnection('search.db') as con:
        cur = con.cursor()
        try:
            cur.execute(
                query
            )
            rows = cur.fetchall()
                    
        except Exception as err:
            return 'SQLite error: %s' % str(err) 
        return rows

if __name__ == "__main__":
    create_table()