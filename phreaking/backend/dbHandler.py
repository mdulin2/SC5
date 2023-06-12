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
        "DROP TABLE IF EXISTS PhoneBook;"
    )
    cur.execute(
        """
        CREATE TABLE inProgressCall(
            id VARCHAR(36), -- UUID of the call
            characters VARCHAR(256), -- The characters that had previously been entered that are valid
            operatorCodes VARCHAR(512),
            state INT, -- The state of the phone call
            cash INT, 
            callContinued BOOL,
            curRecording INT, -- Used for handling transition between recordings
            lastUpdate INT, -- Used for handling transition between recordings
            PRIMARY KEY (id)
        );
        """
    )
    cur.execute(
        """
        CREATE TABLE PhoneBook(
            number VARCHAR(36), -- phone number call
            name VARCHAR(100),
            international BOOL, -- whether this is an international card 
            isComputer BOOL,    -- Is this a computer - for war dialing
            link TEXT, -- link to get the user information from
            PRIMARY KEY (number)
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

# Update the current frame and last updated frame
def add_frame_data(call_id, curRecordings, lastUpdate):
    cur.execute(
        """
        UPDATE inProgressCall SET curRecording = ?, lastUpdate = ? WHERE id = ?
        """, [curRecordings,lastUpdate, call_id]
    )
    
    con.commit()

def add_char_to_call(call_id, char):
    cur.execute(
        """
        UPDATE inProgressCall SET characters = ? WHERE id = ?
        """, [char, call_id]
    )
    
    con.commit()

def add_state_to_call(call_id, state): 
    cur.execute(
        """
        UPDATE inProgressCall SET state = ? WHERE id = ?
        """, [state, call_id]
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
        INSERT INTO inProgressCall(id, characters, operatorCodes, state, cash, callContinued, curRecording,lastUpdate)
        VALUES(?, ?,?, ?, ?, ?, ?, ?)
        """, [caller_id, "", "", 0, 0, True, 0 ,0]
    )   

    con.commit()

    return caller_id


###
### Read the CSV file to add contents to the book
### Add recordings to the frontend to play
#def add_all_to_phone_book():
    

create_table()

