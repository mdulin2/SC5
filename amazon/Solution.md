## Solution 

When an OTP (one time password) is created, there is a 1 out of a 10,000 chance that it can be guessed. However,  
there is no limit on the amount of OTPs that can be created! Because of this flaw, we can create a bunch of OTPs and   
hope that one of them is correct when we finally guess it. A simple payload for this can be seen below: 

```
python -c 'print "jbezos\n" + "$money$\n" + "1\n" * 30000 + "2\n" + "1111\n" + "3\n"' | ./amazon
```

An additional solution is to simply try each and every combination until one of them is correct. This is possible   
because there are no brute force protections on this. 
