## Airline Tickets
- Have you ever considered what's on an airline ticket? Your name? Location? Let's find out! This series of challenges will delve into a series of challenges to interact with an Arduino via QR codes.

## Challenge 1
- What is the seat number and row of the airline ticket given? Reverse engineer the format!
- HINT: QR code is just a representation of text :)

## Challenge 2 
- Set the name of the ticket to be Elon Musk when scanning the QR code. Build a valid QR code from the previous QR code given. 
- Scan the QR code on the ticket scanner to get the flag.

## Challenge 3 
- Set the ticket to be first class. Build a valid QR code from the previous QR code given. 
- Scan the QR code on the ticket scanner to get the flag.
- HINT: What does the 'E' stand for? 

## Challenge 4
- Can you find a way to write into the 'Secret' part of the ticket? 
- HINT: Read the source code of the Ardunio challenge. 
- HINT: You can't manually set it ;) You'll need another vulnerability.

## Challenge 5
- The final section of the ticket is a checksum.
- Reverse engineer the Arduino code to recreate a valid checksum with a flight number of '9675309'.  