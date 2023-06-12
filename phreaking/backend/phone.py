from toneParser import * 
from dbHandler import * 
import time

'''
Based on the previous state and the information being dialed, handle the state changes
TODO: Prior to this, the following should happen: 
- Transfer '.wav' file here via websocket
- Save it to the file system 
- Call this function to update state
- Delete the file 
- Continue on :) 
'''
def handleDial(f, call_id):
    print("Call Id:", call_id)
    callInfo = get_call_info(
        call_id
    )

    print(callInfo)
    lastUpdate = callInfo[7]
    currentRecording = callInfo[6]  
    state = callInfo[3]  

    # Place holder
    # types: data, flag, link, op
    # TODO: Set the 'state' to the previous one as the default
    response_data = {"data" : "", "type" : "", "state" : "" }

    # Too quick of an update. Let's just ignore this.
    if(currentRecording != 0 and currentRecording == lastUpdate):
        add_frame_data(call_id, currentRecording+1, lastUpdate)
        return False

    d, op = findTones(f)
    if DEBUG == True: print("Parsed Frequencies Raw:", d, op)

    # No data found update the frame and exit now. 
    if(d == False): 
        add_frame_data(call_id,currentRecording+1, lastUpdate)
        return False
    
    ## TODO: Coin sound without real coin - mirror packet check 
    
    # Just dialing a number. Add the number then move on.
    if(op == False):
        previousChars = callInfo[1]
        add_char_to_call(call_id, previousChars + d)
        add_frame_data(call_id,currentRecording+1, currentRecording+1)

        # TODO: Return an array instead of dict to support MULTIPLE updates
        if(d == "A" or d == "B" or d == "C" or d == "D"):
            response_data["data"] = "SC5{Military_Ph0nes_Used_T0_Support_Th3se!}"
            response_data["type"] = "flag"         
        else:
            response_data["data"] = d
            response_data["type"] = "msg"
        return response_data

    # Add a quarter to the system
    elif(d == "COIN"):
        add_cash_amount(call_id, 25 + callInfo[4]) 
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        return response_data
    
    # Add a quarter to the system
    elif(d == "QUARTER"):
        add_cash_amount(call_id, 25 + callInfo[4]) 
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        return response_data 

    # Add a nickel to the system
    elif(d == "NICKEL"):
        add_cash_amount(call_id, 5 + callInfo[4]) 
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        return response_data
    
    elif(d == "DIAL"):
        
        # IF we were in the DISCONNECT state before
        if(state == 2): 
            # TODO: Check if this is an international phone call before sending this back
            response_data["data"] = "SC5{Blue_B0x_1s_Phreaking_Me_0uT!}"
            response_data["type"] = "flag"
            return response_data
        
        # 1 is the 'CALL' state
        add_state_to_call(call_id, 1)

        # Return a 'recording' or a flag
        # TODO Call people by going to address book and finding data
        link = "http://localhost:3000/audio_files/gettysburg10.wav"
        response_data["data"] = link
        response_data["type"] = "link"
        return response_data
    
    # Add a nickel to the system
    elif(d == "EMERGENCY"):
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        return response_data
    
    elif("SC5{" in d):
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "flag"    
        return response_data

    # 2600 Hz tone
    elif("DISCONNECT" in d):

        print("State: ", state, state == 1)
        time.sleep(3) 

        # Check if the state is 'IN CALL'. That's super important for this attack to work
        if(state == 1): # Ready for another call
            add_frame_data(call_id,currentRecording+1, currentRecording+1)
            # 2 is the 'DISCONNECT' state
            add_state_to_call(call_id, 2)
            response_data["data"] = d
            response_data["type"] = "op"   
            response_data["state"] = "DIALING"  

        elif(state == 0): # State is something else...
            # 3 is the 'END' state
            add_state_to_call(call_id, 3)
            response_data["data"] = d
            response_data["type"] = "op"   
            response_data["state"] = "END"            
        
        # Ignore other stray calls to this 

        return response_data

    # Nothing no update at all. Need to advance the frames ahead though.
    else: 
        add_frame_data(call_id,currentRecording+1, lastUpdate)

    # TODO Response to the user. Either a tone to be played or a .wav file
    # Should have 'default' phone numbers and fun ones as well

if __name__ == "__main__":
    '''
    Mimicing the phone call setup via websocket calls
    '''
    call_id = add_call()


    handleDial("./audio_files/DialB.wav", call_id)
    handleDial("./audio_files/DialNine.wav", call_id)
    handleDial("./audio_files/DialOne.wav", call_id)
    handleDial("./audio_files/Coin.wav", call_id)
    handleDial("./audio_files/DialTone.wav", call_id)
    handleDial("./audio_files/2800.wav", call_id)
    handleDial("./audio_files/nothing.wav", call_id)
    handleDial("./test.wav", call_id)
    handleDial("./audio_files/quarter.wav", call_id)

    print(get_call_info(call_id)) 
