# Racey Solution
- The game let's you press and unpress a button. 
- The goal is to press the same button *multiple times*. There is verification done in order to make this impossible. 
- However, there is a *time of check - time of use* (TOCTOU) race condition on this. 
- 	```
	# button has already been solved
	if(score != 0):
		return build_result("Already Pressed", 400)
	...

	cursor.execute("UPDATE buttons set score = score + ? WHERE button_id=?", (100, button_id))

	```
- The verification for checking to see if there is a score, can be *raced*. 
- If two threads hit that verification at the same time, then the query will add to the global score for a button **twice**. 
	- One thread enters at points set to 0. Passes the check.
	- A second thread enters at points set to 0. Passes the check.
	- A score for the button adds 100 to the score. Total is 100.
	A score for the button adds 100 to the score. Total is 200.
- The button cannot be pressed fast enough in the UI. So, we need to script this using bash. 
- After creating a button in the UI, we can make two simultaneous requests:
	- This request can be copied from the network tab in the browser dev tools.
	- Execute the following request twice.
	``curl -X POST <<$HOST>>/submit -d '{"press":true,"button":"<<BUTTON_ID>>"}' -H 'Content-Type: application/json' &``
	- NOTE: Notice the ``&`` at the end. This makes the request run in the background. This is crucial so that two requests can be made at the same time. Without this, it WILL not work.
	- It's easier to put the bash command above TWICE into a bash script and just execute that. 
- The file ``POC.sh`` has a full script that creates a button and outputs the flag. 
- Flag: SC4{At0mic_0r_n0T?!}
