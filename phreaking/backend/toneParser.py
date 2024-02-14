import numpy as np
from scipy.fft import *
from scipy.io import wavfile
import time

DEBUG = True 

# Number tones, as they are on the board
number_tones = [[697, 770, 852, 941], [1209, 1336, 1477, 1633]]
entry_list = ["1", "2", "3", "A", "4", "5", "6", "B", "7", "8", "9", "C", "*", "0", "#", "D"]

other_dtmf = {
    "1700-2200" : "COIN", 
    "1050-1100" : "NICKEL", # NICKEL is one click at this frequency - https://www.tech-faq.com/frequencies-of-the-telephone-tones.html
    "350-440" : "DIAL",
    "852-960" : "EMERGENCY", # Really 853 but it's too close to '852' in the dials to work that way.
    #"100-600" : "SC5{Audi0_Engineering_Fr0m_ZacH}" # Flag
}

other_tones = [100, 350, 440, 600, 800, 852, 960, 1050, 1100, 1700, 2200, 2600]
code = {
    2600: "DISCONNECT", # First person to solve should get a copy of this magazine (lolz) 
    800 : "QUARTER" # Quarter is one click at this frequency - https://www.tech-faq.com/frequencies-of-the-telephone-tones.html
}

all_tones = flat_list = [item for sublist in number_tones for item in sublist] + other_tones

# Start and end time are calculated in frames
def analyzeFile(file, start_time, end_time):

    # Open the file. 
    # Returns an audio sampling rate (likely 48000)
    # Returns a numpy 2D array
    rate, data = wavfile.read(file) # 

    # https://www.askpython.com/python/examples/amplitude-of-wav-files
    dataAbs = np.absolute(data) 
    avgAmp = np.average(dataAbs) 

    # Get the most dominant frequency
    if data.ndim > 1:
        data = data[:, 0]
    else:
        pass

    # Return a slice of the data from start_time to end_time
    dataToRead = data[int(start_time * rate / 1000) : int(end_time * rate / 1000) + 1]

    # Fourier Transform
    N = len(dataToRead)
    yf = rfft(dataToRead)
    xf = rfftfreq(N, 1 / rate)

    # Get all of the frequencies out of this
    # DTFM potentially needed
    index = 0
    curHit = 0
    idxs = []

    # TODO: Improve the parsing for valid entries
    # Right now, it's finding all the indexes with amplitudes greater than 1e6. 
    # If that's true, then it adds index to find the frequency later.
    # Potential improvements: Click detection would be sick.
    for elt in np.abs(yf):
        if(elt > 1e6 and (curHit + 30) < index):
            curHit = index
            idxs.append(index) 
        
        index += 1


    # Get all elements that we loud enough 
    # They get filtered down the road by checking proximity to real frequencies
    freqs = []
    for idx in idxs:
        freq = xf[idx]
        freqs.append(freq)

    if DEBUG == True: print("Parsed Frequencies Raw:", freqs)
    return freqs, avgAmp

def isCallValid(freqs, amp):

    # If the signal is too quiet
    if(amp < 100):
        return False
    
    # Too many frequencies were found for this to be a phone dial
    if(len(freqs) > 2 or len(freqs) == 0):
        return False

    return True

def takeClosest(num):
   closest = min(all_tones,key=lambda x:abs(x-num))
   if(abs(num - closest) > 10):
       return 0
   return closest

def getNumberFromTones(freqs):
    freqs.sort()

    top = number_tones[0]
    left = number_tones[1]

    try:
        # Get the number from the list
        top_index = top.index(freqs[0])
        left_index = left.index(freqs[1])
    except ValueError:
        return False

    # Errors out if i can't find it.
    number = top_index * 4 + left_index
    number = entry_list[number]
    return number


def findTones(f):
    # Sample rate is per second. To get the amount of time to listen it's sample_rate * seconds

    # TODO: Fix this check. Unsure if it's accurate
    seconds = 0.5
    sample_rate = 48000

    freqs, amp = analyzeFile(
        f, 0, seconds * sample_rate
    )

    freqs_real = []
    for freq in freqs: 
        info = takeClosest(freq)
        if(info != 0): # If the frequency isn't close enough to the expected frequencies
            freqs_real.append(info)

    freqs_real = [*set(freqs_real)]
    if DEBUG == True: print("Parsed Frequencies:", freqs_real)

    # Not valid...
    isValid = isCallValid(freqs_real, amp)
    if(isValid == False):
        return False, False
    
    # Number or operator
    if(len(freqs_real) == 2):
        op = getNumberFromTones(freqs_real)
        print("Op after get number:", op)
        if(op == False):
            # Operator codes
            return parseOperatorDTMF(freqs_real) 
        return op, False
    
    else: # Single tones
        # Operator codes, which are single tone
        op = code.get(freqs_real[0])
        if(op == None):
            return False, False
        return op, True

def parseOperatorDTMF(freqs):
    key = str(freqs[0]) + "-" + str(freqs[1]) 
    setting = other_dtmf.get(key)
    if(setting == None):
        return False, False

    return setting, True 

#mode = findTones("./audio_files/DialNine.wav")
#print(mode) 