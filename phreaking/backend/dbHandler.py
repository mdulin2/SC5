import sqlite3
import uuid
import time


def create_table():
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    cur.execute(
        "DROP TABLE IF EXISTS inProgressCall; "
    )
    cur.execute(
        "DROP TABLE IF EXISTS phoneBook;"
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
        CREATE TABLE phoneBook(
            number VARCHAR(36), -- phone number call
            name VARCHAR(100),
            international INT, -- whether this is an international card 
            link TEXT, -- link to get the user information from
            visible INT, 
            PRIMARY KEY (number)
        );
        """
    )

    con.commit()

def add_cash_amount(call_id, amount):
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    print("call id before update:", call_id)
    cur.execute(
        """
        UPDATE inProgressCall SET cash = ? WHERE id = ?
        """, [amount, call_id]
    )
    
    con.commit()

# Update the current frame and last updated frame
def add_frame_data(call_id, curRecordings, lastUpdate):
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    cur.execute(
        """
        UPDATE inProgressCall SET curRecording = ?, lastUpdate = ? WHERE id = ?
        """, [curRecordings,lastUpdate, call_id]
    )
    
    con.commit()

def add_char_to_call(call_id, char):
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    cur.execute(
        """
        UPDATE inProgressCall SET characters = ? WHERE id = ?
        """, [char, call_id]
    )
    
    con.commit()

def add_state_to_call(call_id, state): 
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    cur.execute(
        """
        UPDATE inProgressCall SET state = ? WHERE id = ?
        """, [state, call_id]
    )
    
    con.commit()   
def add_operator_code_to_call(call_id, operatorCode):
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    cur.execute(
        """
        UPDATE inProgressCall SET operatorCode = ? WHERE id = ?
        """, [operatorCode, call_id]
    )
    
    con.commit()

def get_call_info(call_id):
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
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
def add_all_to_phone_book():
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    f = open("./address_list.txt")
    
    data = f.read()
    lines = data.split("\n")

    for line in lines: 
        # section break 
        if("---" in line):
            continue
        
        entries = line.split(",")
        # Add the data
        cur.execute(
            """
            INSERT INTO phoneBook(number, name, international, link, visible)
            VALUES(?, ?, ?, ?, ?)
            """, [entries[0], entries[1], entries[2], entries[3], entries[4]]
        )   
    con.commit()

'''
Get the phone information. 
Removes all special numbers for the challenges.
'''
def get_phone_book_info():
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()
    cur.execute(
        """
        SELECT number, name, international FROM phoneBook WHERE visible = true
        """,[]
    )
    rows = cur.fetchall()
    if(len(rows) == 0):
        return False 
    
    return rows

def get_phone_number_info(number):
    
    # Holds the state of all the phone calls
    con = sqlite3.connect("calls.db") 
    cur = con.cursor()

    cur.execute(
        """
        SELECT number, name, international, link FROM phoneBook WHERE number = ?
        """,[number]
    )
    rows = cur.fetchall()
    if(len(rows) == 0):
        return False 
    
    # Should only be a single match for the primary key
    return rows[0]

'''
This is for the calling card challenge.
Hackers will need to brute force the card information with sounds!
The magic is having a seven digit card that is divisible by 37. 
Large amount of cards to be valid!
'''
def isValidCard(cardNumber):
    
    try:
        numberInt = int(cardNumber)
        if(numberInt % 37 == 0 and len(cardNumber) >= 7 and cardNumber.startswith("789")):
            return True 
        else: 
            return False 
    except ValueError: # Integer conversion failed
        return False 

def initializeInformation():
    create_table()
    add_all_to_phone_book()  

if __name__ == "__main__":
    create_table()
    add_all_to_phone_book()
    print(get_phone_book_info())
    print(get_phone_number_info("9"))

