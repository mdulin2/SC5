from toneParser import * 
from dbHandler import * 
import time
import copy 

'''
Based on the previous state and the information being dialed, handle the state changes
- Transfer '.wav' file here via websocket
- Save it to the file system 
- Call this function to update state
- Continue on :) 
'''
def handleDial(f, call_id):
    print("Call Id:", call_id)
    callInfo = get_call_info(
        call_id
    )

    print(callInfo)
    consecutive = callInfo[8]
    lastUpdate = callInfo[7]
    currentRecording = callInfo[6]  
    state = callInfo[3]  
    phoneNumber = callInfo[1]  
    userFunds = callInfo[4]  

    # Place holder
    # types: data, flag, link, op
    # TODO: Set the 'state' to the previous one as the default
    response_data = {"data" : "", "type" : "", "state" : "" }

    # Too quick of an update. Let's just ignore this.
    if(currentRecording != 0 and currentRecording == lastUpdate):
        add_frame_data(call_id, currentRecording+1, lastUpdate, consecutive)
        return False

    d, op = findTones(f)
    if DEBUG == True: print("Parsed Frequencies Raw:", d, op)

    # No data found update the frame and exit now. 
    if(d == False): 
        add_frame_data(call_id,currentRecording+1, lastUpdate)
        return False
        
    # Just dialing a number. Add the number then move on.
    if(op == False):
        previousChars = callInfo[1]
        add_char_to_call(call_id, previousChars + d)

        # The general case
        response_data["data"] = d
        response_data["type"] = "msg"

        cons_tmp=0
        if((d == "A" or d == "B" or d == "C" or d == "D")):
            cons_tmp = consecutive + 1
            
        add_frame_data(call_id,currentRecording+1, currentRecording+1, cons_tmp)

        # If they send a letter NOT on the normal key pad.
        if((d == "A" or d == "B" or d == "C" or d == "D") and consecutive >= 2): # Added a check here to ensure that this didn't randomly appear. 
            # TODO - add a consistent check right here. Maybe 5 seconds long or something like that?
            response_data1 = copy.deepcopy(response_data)
            response_data1["data"] = "SC5{Military_Ph0nes_Used_T0_Support_Th3se!}"
            response_data1["type"] = "flag"  
            response_data = [response_data,response_data1]
        return response_data

    # Add a quarter to the system
    elif(d == "COIN"):
        add_cash_amount(call_id, 25 + userFunds) 
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        response_data["state"] = (25 + userFunds) / 100 # Shift the decimals over
        if(userFunds >= 500): # $5
            response_data2 = copy.deepcopy(response_data) 
            response_data2["type"] = "flag"    
            response_data2["data"] = "SC5{Stealing_m0ney_fr0m_telec0m_1s_f1ne}" 
            response_data = [response_data, response_data2]

        return response_data
    
    # Add a quarter to the system
    elif(d == "QUARTER"):
        add_cash_amount(call_id, 25 + userFunds) 
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        response_data["state"] = (25 + userFunds) / 100 # Shift the decimals over

        if(userFunds >= 500): # $5
            response_data2 = copy.deepcopy(response_data) 
            response_data2["type"] = "flag"    
            response_data2["data"] = "SC5{Stealing_m0ney_fr0m_telec0m_1s_f1ne}" 
            response_data = [response_data, response_data2]
        return response_data 

    # Add a nickel to the system
    elif(d == "NICKEL"):
        add_cash_amount(call_id, 5 + userFunds) 
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        response_data["state"] = (5 + userFunds) / 100 # Shift the decimals over

        if(userFunds >= 500): # $5
            response_data2 = copy.deepcopy(response_data) 
            response_data2["type"] = "flag"    
            response_data2["data"] = "SC5{Stealing_m0ney_fr0m_telec0m_1s_f1ne}" 
            response_data = [response_data, response_data2]
        return response_data
    
    elif(d == "DIAL"):
        
        # Get information about the phone number
        numberInfo = get_phone_number_info(phoneNumber)
            
        # Calling card check 
        if(state == 4):
            if(isValidCard(phoneNumber) == False): # SO CLOSE. But not enough.
                response_data["data"] = "/bad_calling_card.wav"
                response_data["type"] = "link" 

                response_data1 = copy.deepcopy(response_data) 
                response_data1["data"] = "BAD CARD"
                response_data1["type"] = "op" 
                add_frame_data(call_id,currentRecording+1, currentRecording+1)

                return [response_data,response_data1]

            else: # If the call is valid and the state is the DISCONNECT state
                response_data["data"] = "/correct.wav"
                response_data["type"] = "link" 

                response_data1 = copy.deepcopy(response_data)
                response_data1["data"] = "SC5{Jeff_M0ss_did_this_at_GU_Back_in_the_day}"
                response_data1["type"] = "flag" 
                add_frame_data(call_id,currentRecording+1, currentRecording+1)

                return [response_data,response_data1]

        # Calling card special state
        if(phoneNumber == "7"): 
            print("Inside - why no calling card?")
            add_state_to_call(call_id, 4) # 4: Entered calling card state
            add_char_to_call(call_id, "")
            response_data["data"] = "/type_in_your_calling_card.wav"
            response_data["type"] = "link"
            response_data["state"] = "CALLING CARD"

            response_data1 = copy.deepcopy(response_data)
            response_data1["type"] = "op" 
            response_data1["data"] = "CLEAR" 
            add_frame_data(call_id,currentRecording+1, currentRecording+1)

            return [response_data,response_data1]  
        
        # If the number doesn't exist
        if(numberInfo == False):
            # TODO - Add real ring
            response_data["data"] = "/audio_files/BadCall.mp3"
            response_data["type"] = "link"
            response_data["state"] = "BAD CALL"
            response_data1 = copy.deepcopy(response_data)
            response_data1["type"] = "op" 
            response_data1["data"] = "CLEAR" 
            add_frame_data(call_id,currentRecording+1, currentRecording+1)

            return [response_data, response_data1]
        
        # IF we were in the DISCONNECT state before and we're in a valid international call
        if(state == 2 and (numberInfo[2] == True or numberInfo[2] == 1)): 
            response_data["data"] = "SC5{Blue_B0x_1s_Phreaking_Me_0uT!}"
            response_data["type"] = "flag"
            add_frame_data(call_id,currentRecording+1, currentRecording+1)

            return response_data

        # Don't want to convert state badly here
        if(state != 2 and state != 4):
            # 1 is the 'CALL' state
            add_state_to_call(call_id, 1) 

        # If it's an international call, the end user needs to have money for this
        if(numberInfo[2] == True or numberInfo[2] == 1):
            if(userFunds < 500): # $5
                response_data["data"] = "/no_money.wav" # Play that they need more money - TODO: Add real ring
                response_data["type"] = "link"
                add_frame_data(call_id,currentRecording+1, currentRecording+1)

                return response_data           

        link = numberInfo[3]
        response_data["data"] = link
        response_data["type"] = "link"
        add_frame_data(call_id,currentRecording+1, currentRecording+1)

        return response_data
    
    # Add a nickel to the system
    elif(d == "EMERGENCY"):
        add_frame_data(call_id,currentRecording+1, currentRecording+1)
        response_data["data"] = d
        response_data["type"] = "op"
        return response_data

    # 2600 Hz tone - blue box
    elif("DISCONNECT" in d):

        # Check if the state is 'IN CALL'. That's super important for this attack to work
        if(state == 1): # Ready for another call
            add_frame_data(call_id,currentRecording+1, currentRecording+1)
            # 2 is the 'DISCONNECT' state
            add_state_to_call(call_id, 2)
            add_char_to_call(call_id, "") # Clear number if this is true to add the new number.

            response_data["data"] = d
            response_data["type"] = "op"   
            response_data["state"] = "DIALING"  
            response_data1 = copy.deepcopy(response_data)

            response_data1["data"] = "CLEAR"
            response_data1["type"] = "op"   
            response_data = [response_data,response_data1]
        elif(state == 0): # State is something else...
            # 3 is the 'END' state
            add_state_to_call(call_id, 3)
            response_data["data"] = d
            response_data["type"] = "op"   
            response_data["state"] = "END"            
        
        return response_data

    # Nothing no update at all. Need to advance the frames ahead though.
    else: 
        add_frame_data(call_id,currentRecording+1, lastUpdate)

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
