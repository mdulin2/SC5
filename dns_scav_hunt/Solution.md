# DNS Records Scavenger Hunt 

## Email Destination

Solution Steps:
1. Use an MX record look up service - https://mxtoolbox.com is recommended.
    * Use the MX Lookup service.
1. Look up the MX record for "mcdonalds.com", without the quotes. 
    * It will return the IP address of the destination mail server for the domain, mcdonalds.com

Flag/Answer: 52.3.1.83

## Find the Hosting Provider

Solution Steps:</br>
There are two main steps to this solution: 
  * Look up the IP address of the domain.
  * Perform a reverse lookup

Look up the IP address of the domain:
  1. Navigate to https://mxtoolbox.com and click the SuperTool link in the upper-left.
        * Alternatively, navigate to: https://mxtoolbox.com/SuperTool.aspx
  1. In the SuperTool drop-down menu, select "DNS Lookup."
  1. Enter the domain, "maxwelldulin.com", without the quotes.
  1. Copy/note the resulting IP address. 

Perform a reverse lookup:
1. While still using the SuperTool, select "Reverse Lookup" from the drop-down menu.
1. Enter the IP address from the previous DNS lookup.
1. Note that the resulting output indicates the website is hosted from AWS.

Flag/Answer: AWS

## Domain Registration Lookup

Use a WHOIS record lookup to find the email address of the admin of the domain:
  1. Navigate to https://mxtoolbox.com and click the SuperTool link in the upper-left.
        * Alternatively, navigate to: https://mxtoolbox.com/SuperTool.aspx
  1. In the SuperTool drop-down menu, select "Whois Lookup."
  1. Enter the domain, "spokesman.com", without the quotes.
  1. Locate the "Admin Email" field in the resulting output. 

Flag/Answer: itbusiness@SPOKESMAN.COM
