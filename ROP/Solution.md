# Solution 
- The code in ``code.js`` is taking in user input and deciding which function to execute. If the user can execute ALL functions, then they get the flag. 
- func1, func2, func4, func6 and func7 don't take any parameters. 
- func3 requires a single parameter - "ROP". 
- func5 requires two parameters - "0x8000000" and "1337".
- The parameter goes BEFORE the function call. For instance, to call func3 with the parameter 'ROP' you would use ["ROP", "func3"].
- The solution is below to call every function with the proper parameters:
["func1", "func2", "ROP", "func3", "func4", "0x8000000", "1337", "func5", "func6", "func7"]


# Hints to give 
- Explanation of what a stack as a data structure is by adding real-life examples
- Since a stack follows a Last In First Out (LIFO) principle, the parameters should go before the functions
