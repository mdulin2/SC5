import sqlite3
import uuid

# Holds the state of all the phone calls
con = sqlite3.connect("calls.db") 
cur = con.cursor()

def create_table():
    cur.execute(
        "DROP TABLE IF EXISTS inProgressCall; "
    )
    cur.execute(
        """
        CREATE TABLE inProgressCall(
            id VARCHAR(36), -- UUID of the call
            characters VARCHAR(256), -- The characters that had previously been entered that are valid
            operatorCodes VARCHAR(512),
            state int, -- The state of the phone call
            cash int, 
            callContinued bool,
            PRIMARY KEY (id)
        );
        """
    )

    con.commit()

def add_cash_amount(call_id, amount):
    print("call id before update:", call_id)
    cur.execute(
        """
        UPDATE inProgressCall SET cash = ? WHERE id = ?
        """, [amount, call_id]
    )
    
    con.commit()

def add_char_to_call(call_id, char):
    print("call id before update:", call_id)
    cur.execute(
        """
        UPDATE inProgressCall SET characters = ? WHERE id = ?
        """, [char, call_id]
    )
    
    con.commit()

def add_operator_code_to_call(call_id, operatorCode):
    cur.execute(
        """
        UPDATE inProgressCall SET operatorCode = ? WHERE id = ?
        """, [operatorCode, call_id]
    )
    
    con.commit()

def get_call_info(call_id):
    cur.execute(
        """
        SELECT * FROM inProgressCall WHERE id = ?
        """, [call_id]
    )
    rows = cur.fetchall()
    if(len(rows) == 0):
        return False 
    
    return rows[0]

def add_call():
    
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    caller_id = str(uuid.uuid4())
    cur.execute(
        """
        INSERT INTO inProgressCall(id, characters, operatorCodes, state, cash, callContinued)
        VALUES(?, ?,?, ?, ?, ?)
        """, [caller_id, "", "", 0, 0, True]
    )   

    con.commit()

    return caller_id



create_table()
'''
call_id = add_call()
print(call_id) 
print(get_call_info(call_id))
'''
