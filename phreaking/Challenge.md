## Prefix 
- The original implementation on automatic phone call routing was broken. The operation actions were encoded into the same channel as the users voice audio. Do you see the problem here? By sending special tones, it was possible for the caller to influence the state of the phone system. This meant free calls, unlimited data and much more. Welcome to a blast from the past. 

- NOTE: This system is actually parsing audios files. This challenge is about recreating the original attacks to get free calls. The audio parsing requires a fairly quiet area in order to work. Additionally, if the audio is too loud it distorts the signal and it won't get picked up. With this in mind, have fun! :) 

## Challenge 1 - Military Codes (5) 
- You know the sounds that your phone makes when you type in a number? Beep! These tones are special; they are encoded with information about what number is being dialed using Dual Tone Multi-Frequency (DTMF). 
- Besides 0-9,*,#, the original phones included A,B,C,D on them as well. However, commerical products didn't have them. Can you produce one of the letters? 
- Hint: These codes use Dual Tone Multi-Frequency (DTMF). This means you'll beed a way to play two frequencies at once in order to produce these signals. 
- Hint: Use 'https://onlinetonegenerator.com/multiple-tone-generator.html' to generate DTMF codes. 

## Challenge 2 - Free Money! (6) 
- When you deposit a coin into a payphone, the <i>sound</i> is what signifies to the company that money was deposited. By <i>spoofing</i> this sound, it is possible to deposit fake coins! To get the flag, deposit $10 worth of fake coins. 
- NOTE: The original implementation required clicks. However, I'm not cool enough to write this in software. So, the proper frequency will be alright. 
- Hint: This attack was called a <i>Red Box</i> back in the day. 
- Hint: There are several different coin frequencies. If you are trying one of the three valid ones and it's not working, please talk to an organizer. Two are DTMF and one is a single frequency.

## Challenge 3 - Bait and Switch (8) 
- There is a special frequency that will <i>drop</i> the current call you're in. At this point, the phone believes that it's being controlled by the operator and not a regular user. You are now a superuser! 
- To solve this challenge, get an international call for free by using a <i>blue box</i> attack. To be precise, make a call, <b>DISCONNECT</b> the call and make a valid international call to get the flag. 
- HINT: This is a single frequency. 
- HINT: The frequency is the name of a famous hacker magazine. 

## Challenge 4 - Stealing Others Money (10) 
- Back in the day, if you wanted to pay for a phone call you could use a <i>calling card</i>. This was a credit-card-like card that had credits from telecom companies to make phone calls. However, the randomization of these wasn't great and the space can be brute forced. 
- To solve this challenge, dial the special number <code>7</code> then enter in a valid calling card. If your card is correct, you'll get a flag. NOTE: All calling cards start with 789 in your region.
- Hint: Trying this by hand isn't feasible. Please write JavaScript code to make the noises. Use the code link at <TODO> (JS Fiddle seems like the way to go here) 
