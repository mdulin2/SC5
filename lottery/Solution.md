## Solution
- The storage for all of the information is within the redis caching environment. 
- In order to prevent malicious writes, it is important that the input is validated. 
- The cache key `lottery` stores the current lottery number. But, there is a lack of input validation to ensure that current users cannot be recreated AND that the user to validate is NOT lottery. 

### Solution 1
- The 'guess' API with the form ``/guess/<name>/<value>`` stores the 'name' as the key in the redis cache and the 'value as the 'value' in the cache. 
- There is NO input validation that the user making the request is the signed up user. 
- Additionally, there is no validation on the cache key itself. 
- So, if we specify ``/guess/lottery/0`` this will make the lottery cache key be 0! This effectively allows us to contorl the lottery number for the round :) 

```
curl http://127.0.0.1:5000/guess/a/1       # Set our user guess
curl http://127.0.0.1:5000/guess/lottery/1 # Overwrite the lottery number
curl http://127.0.0.1:5000/validate/a      # Check our lottery number
```

## Solution 2 
- The `validate` API with the form ``/validate/<name>`` does no valdiation on the allowed cache keys for the API. 
- If you specify ``lottery`` as the user name, then the lottery number will be used in the comparison. 
- Since checking something against itself is always true, this will output the flag. 

```
curl http://127.0.0.1:5000/validate/lottery
```
