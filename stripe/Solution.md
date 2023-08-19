## Solution 
- The goal of the challenge is to purchase hitman for free. 
- By going through Stripe, we're required to pay.
- The flow for the application is as follows: 
	- /Login - create a user
	- /stripe/:user - Order a hitman as a specific user
	- Redirects to stripe for you to pay
	- Callback is made from stripe to the application to finalize the state changes. 
- According to Stripe, the callback function should ONLY be callable by stripe
	- Typically, this is done via a signature check.
- The application is missing the signature or IP check!
	- This means that anybody can call the API directly to redeem their purchase multiple times. 
- Exploit flow: 
	- /Login - create a user (can be done through UI)
	- /stripe:/user - Order a hitman (can be done through UI). NOTE: Save the 'ID' from this request. 
	- Call the callback function directly. Do this until the user has 20+ in their inventory:
	```

	curl -X POST http://127.0.0.1:5000/webhook --data '{"type" : "checkout.session.completed", "data" :{"object" : {"metadata" : {"payment_id" : <<PaymentID>>}}}}' -H 'Content-Type: application/json'
	```
	- Calling this directly will take trial and error on figuring out the shape and data required for this. Students should read the source code and look at error messages to figure this out.
	- Check the winner function!
