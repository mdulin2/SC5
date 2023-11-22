## Hitman Central 
- You found a website that sells hitman but has a limit on how many you can purchase. Can you find a way to purchase 20 hitman with a single account to get the bulk of them for free? 
- Credit card info: 4242 4242 4242 4242, 01/25, 777

- Hint: 
	- The service uses Stripe callbacks: https://stripe.com/docs/webhooks#best-practices
	- Read the source code of the nodejs router
	- Understanding the flow of data from Stripe to the website helps solve this challenge.
		- https://cdn.wpsimplepay.com/wp-content/uploads/2022/12/wp-simple-pay-add-endpoint.png
	- Curl is your friend!
