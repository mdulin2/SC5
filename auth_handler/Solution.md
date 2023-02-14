## Solution 
- The goal is to become a user with level 10, which has two possible scenarios: 
	- Create a user at level 10 
	- Become the root user (id 0) 
- When logging in, a user can provide ANY number that is less than the length of the list. 
	- This means we can provide *negative* numbers.
- Python allows for `negative indexing` in order to iterate in reverse on a list.  
	- For instance, ``python_lst[-1]`` will be get the FINAL element in the list. 
	- https://www.geeksforgeeks.org/python-negative-index-of-element-in-list/
- There is a check to ensure we cannot become the admin user with index 0. 
- However, there is no check that negative indexes can be used. 
- So, we can use an index of -1 in order to select the only element in the list (super admin).
- Neat! :) 
- Inputs: 
```
2 - Login 
-1 - Select the 'superadmin' user by using negative indexing
5 - Print the flag
```

