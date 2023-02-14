"""
Maxwell Dulin 
Super Secure scoreboard 
"""

import sqlite3
from abstract_database_connection import AbstractDatabaseConnection


create_statements = {
    # Create statement for album table.
    'buttons' : """CREATE TABLE IF NOT EXISTS buttons (
        button_id VARCHAR(256) PRIMARY KEY,
        score int
    );""",
	
}

def create_tables():
    """
    Creates all tables in the database.
    """
    with AbstractDatabaseConnection('button.db') as conn:
        cursor = conn.cursor()
        for cs in create_statements:
            cursor.execute(create_statements[cs])
        conn.commit()

def delete_tables():

	with AbstractDatabaseConnection('button.db') as conn:
		cursor = conn.cursor()
		cursor.execute("""DROP TABLE IF EXISTS buttons""")
		conn.commit()
	
def setup():
	"""
	Create and seed the database.
	"""
	delete_tables()
	create_tables()

if __name__ == '__main__':
    setup()