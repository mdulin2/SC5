from toneParser import * 
from dbHandler import * 


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
    d, op = findTones(f)
    if DEBUG == True: print("Parsed Frequencies Raw:", d, op)

    # No data found. Exit now. 
    if(d == False): 
        return 
    
    # Just dialing a number. Add the number then move on.
    if(op == False):
        previousChars = callInfo[1]
        add_char_to_call(call_id, previousChars + d)
        return d

    # Add a quarter to the system
    if(d == "COIN"):
        add_cash_amount(call_id, 25 + callInfo[4]) 
        return d 
    
    # TODO Handle the other codes

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
