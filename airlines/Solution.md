## Solution
- Read and write to the QR codes using https://qrcode.tec-it.com/en.  

## Solution 1 
- The data decoded from the QR code is ``1111|Kevin|Mitnick|22222|E|New York|Spokane|Delta|22C|Secret|12|``. 
- This is broken into ticket number, first name, last name, class, starting locatino, destination, airline, **seat info**, secret date and checksum. 
- The ``seat info`` has 22C, which is pretty obviously a seat number. 
- Flag: 22C. 

## Solution 2
- The QR codes second and third values are the first and last name respectively. Use the first name elon and last name musk with the QR code. 
- An example is this is shown below: 
- ``1111|elon|musk|22222|E|New York|Spokane|Delta|22C|Secret|12|``. 
- Convert this to a QR code via the website and scan it on the challenge. Flag will be given. 
- Flag: {'S', 'C', '5', '{', 'B', '@', 'd','N', '8', 'M', 'e', '}', '\0'}

## Solution 3 
- Everything in the text is either a number or a name besides the seat info and the 'E'. The 'E' stands for 'Economy'. 
- Change the 'E' to 'F' in order to become first class. 
- ``1111|Kevin|Mitnick|22222|F|New York|Spokane|Delta|22C|Secret|12|``
- Convert this to a QR code via the website and scan it on the challenge. Flag will be given. 
- flag: {'S', 'C', '5', '{', 'B', '&', 'd','C', 'l', 'a', 'S', 'S', '!', '}', '\0'}

## Solution 4 
- The 'secret' value is the 8th value in the structure. However, the code never sets it. What can we do? 
- The size of the 'seatInfo' array is only 16 bytes. However, the validation is ``0x20`` bytes. 
- So, there is a buffer overflow in this structure. 
- Provide a ``seatInfo`` of larger than 16 bytes to get the flag. 
- ``1111|Kevin|Mitnick|22222|E|New York|Spokane|Delta|AAAAAAAAAAAAAAAAAAAAAAAA|Secret|12|``
- Convert this to a QR code via the website and scan it on the challenge. Flag will be given. 
- flag: {'S', 'C', '5', '{', 'A', 'V', 'R','B', '0', 'F', '&', '}', '\0'};

## Solution 5
- Two things: 
    - Checksum
    - Flight number 
- Flight number is the fourth value. Simply set this to be 9675309. 
- The checksum is calculated by adding up every value prior to the checksum then modding it by 256. 
- Code for this is written below: 
    ```string="XX"
    for char in string:
    d = d + ord(char)
    print(chr(d % 256))
    ```
- Use the string, without the checksum value, within the 'XX' above. 
- Place the 'character' (not number) representing by this value into the QR code. 
- ``111111|Maxwell|Dulin|9675309|E|Austin|Spokane|Alaska|22C|Secret|/|``
- Convert this to a QR code via the website and scan it on the challenge. Flag will be given. 
- flag: {'S', 'C', '5', '{', 'C', 'h', '3','e', '7', 'Y', 'o', 's', '3', '1', 'f', '}', '\0'}

