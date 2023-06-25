## Challenge 1 - Military Codes
- Dual Tone Multi Frequency (DTMF) is the encoding scheme for many of the signals for phones. In practice, this means combining two frequencies to create a unique tone. This is exactly what is done with the numbers 1,2,3... on our phones. 
- The goal of this challenge is to use A,B,C or D, which were released on operator and military phones but not commerically. 770, 852, 941
- The frequencies for the codes are "A: 697,1633", "B: 770, 1633", "C: 852, 1633", "D: 941, 1633". 
- This can be reproduced by finding recordings of the tones online or using an online generator like https://onlinetonegenerator.com/dtmf.html. 
- Flag: SC5{Military_Ph0nes_Used_T0_Support_Th3se!}

## Challenge 2 - Free Money!
- Same concept as before the previous challenge with a slight twist: it's probably not possible to find a good recording of this. Instead, students will need to *find* the frequencies themselves and find a way to generate them. 
- The website ttps://onlinetonegenerator.com/multiple-tone-generator.html contains easy ways (and is easy to googleable) to create the tones. 
- There are 3 different coin tones that can be used: "QUARTER: 800", "NICKEL: 1050,1100" and a regular coin "1700,2200". All of these should be googlable values. 
- After adding in enough money to hit $10, the user will get the flag. 
- Flag: SC5{Stealing_m0ney_fr0m_telec0m_1s_f1ne}

## Challenge 3 - Bait and Switch
- Sending the 2600Hz frequency is known to DISCONNECT phones.
- By doing so, the phone line is confused and believes that you are the <i>operator</i>. We can abuse this to place international calls for free!
- The steps are as follows: 
    - Start a valid local call with anybody in the phone book 
    - Send the 2600Hz frequency to DISCONNECT the call. Again, the website ttps://onlinetonegenerator.com/multiple-tone-generator.html can be used to generate the frequency. 
    - Place a call to a valid international number. This should output the flag!
- Flag: SC5{Blue_B0x_1s_Phreaking_Me_0uT!}

## Challenge 4 - Stealing Others Money 
- Our goal is to find a valid phone card. This requires us to brute force many different numbers until it works. 
- This can be acheived by writing code in JavaScript to do so. There is a code snippet linked to writing different frequencies to produce this in an automated fashion. Please tell students not to do this by hand; it will get very annoying to do and they'll have a bad time. 
- Here's a valid proof of concept with nice comments: 
    - ....
- The card numbers are only 7 digits in size. To find a valid card, divisble by 37. 
- Flag: SC5{Jeff_M0ss_did_this_at_GU_Back_in_the_day}