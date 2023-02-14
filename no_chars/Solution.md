## Overview
- The challenge does not work... exploit the final call to ``system`` to take control of the process. 
	
### Solution
- The challenge calls ``python`` to execute the python script. However, the ENV variables are not filtered for this call. 
- Because we were using 'Python' instead of '/usr/bin/python', the 'PATH' variable could be changed! Because we control the path variable, we can load our own script as Python. 
- For instance, 
	- Create a bash script named '/tmp/python' with the contents '/bin/bash'. 
	- Set the file to be executable (``chmod +x /tmp/python``)
	- Change the PATH to look inside tmp first. export ``PATH="/tmp/:$PATH"
	- Execute the binary. Now, when it tries to load Python, it will load our bash script. 
- An additional workaround with an absolute Python path would be the 'LD_PRELOAD' to override .so files being loaded into Python. 
- Pretty neat!
