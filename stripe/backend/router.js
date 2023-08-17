const express = require('express');
const http = require('http');
const sqlite3 = require('sqlite3'); 

const sqlite = require('sqlite')

// TODO - fix secret later to be dynamic
const stripe = require('stripe')('sk_test_51NfrqUE8bmyyMPHw83wFfROqb8umMSH8otHsaHwMX2QIuSoSkhPFllEIuLCor3eCMBSt0ltP7mi0cpOeAfiS1aVk003ZracLWT');

var app = express();
let db; 

// this is a top-level await for opening the connection
(async () => {
  // open the database
  db = await sqlite.open({
    filename: '/tmp/database.db',
    driver: sqlite3.Database
  })
})()
// Holds the single product we sell
let product_id = "";
let price_id = "";
let ip = ""; 

// http://maxwelldulin.com:5000/user/Maxwell
app.get("/winner/:userid", async function (req, res) {
  var d = await db.get(`SELECT * FROM Users WHERE UserID = ?`, req.params.userid)
  if(d === undefined){ // Create the user if they don't exist.
      res.send({"error" : "User DNE"});
      return; 
  }
  if(d.Amount >= 20){
      res.send({"flag" : "SC5{asdfasfd}"})
      return;
  }
  res.send({"error" : "Need to get 20 orders to get flag"})
   
});

// curl -X POST http://127.0.0.1:5000/webhookssion.completed", "data" :{"object" : {"metadata" : {"payment_id" : 4}}}}' -H 'Content-Type: application/json'
app.post('/webhook', express.json({type: 'application/json'}), async function (req, res) {

    const event = req.body; 
    console.log(event); 
    var result; 
    if(!('type' in event)){
      res.json({"type" : "Missing 'type' in body"});
      return; 
    }

    // TODO - Perform signature validation here

    // TODO - Check data in the 'Owners' to see if the ID for our order exists or not.
    // Handle the event
    switch (event.type) {
      case 'checkout.session.completed':

        if(!event.data){
          result = {"type" : "Missing 'data' in body"}
          break;
        }

        if(!('object' in event.data)){
          result = {"type" : "Missing 'data.object' in body"}
          break; 
        }
        var session_obj = event.data.object;
        if(!('metadata') in event.data.object){
          result = {"type" : "Missing 'data.object.metadata' in body"}
          break;
        }

        if(!('payment_id') in event.data.object.metadata){
          result = {"type" : "Missing 'data.object.metadata.payment_id' in body"}
          break;
        }

        var tracking_id = event.data.object.metadata.payment_id;
        var d = await db.get(`SELECT * FROM Orders WHERE ID = ?`, [tracking_id]);
		 console.log(d)

   	var user = await db.get(`SELECT * FROM Users WHERE UserID = ?`, d.UserID)
        updateUser(user.UserID, user.Amount + 1)
	result = {"error" : false, "message" : "Successfully bought!"}
        break;

      default:
        result = {"type" : "unknown 'type'"}
    }
  
    // Return a response to acknowledge receipt of the event
    res.json(result);
});

// curl -X POST http://127.0.0.1:5000/stripe/admin
app.post('/stripe/:userid', async function (req, res) {

   var user = await db.get(`SELECT * FROM Users WHERE UserID = ?`, req.params.userid)
   console.log(d) 
   if(user === undefined){
	res.send({"error" : "user dne"})
	return;
   }
   if(user.Amount > 2){
	res.send({"error" : "User hit the limit"})
	return;
   }

   // Get the amount of orders
   var d = await db.get(`SELECT COUNT(ID) from Orders`);
   var id;
   if(d['COUNT(ID)'] == null){
      id = 1;
   }
   else {
      id = d['COUNT(ID)'] + 1;
   }
   console.log(d, id)

 console.log("Price Id:", price_id);

  const session = await stripe.checkout.sessions.create({
    success_url: 'https://maxwelldulin.com/success',
    line_items: [
      {price: price_id, quantity: 1},
    ],
    mode: 'payment',
    metadata : {
	payment_id: id
    }
  });

  createOrder(user.UserID, session.url);

  // Track this info in the 'Orders' table.
  res.send({"redirect_url" :session.url, "id" : id});
 
  // Where to redirect the page to - Stripe!
  return session.url; 
});

// curl http://maxwelldulin.com:5000/user/admin
app.get('/user/:userid', async function (req, res) {		

  var d = await db.get(`SELECT * FROM Users WHERE UserID = ?`, req.params.userid)
  res.send(d)
});

app.get('/Orders/:userid', async function (req, res) {		

  var d = await db.get(`SELECT * FROM Orders WHERE UserID = ?`, req.params.userid)
  res.send(d)
});

// Not the vuln :) Just trying to make it easier to use!
// curl -X POST http://127.0.0.1:5000/login --data '{"user" : "admin"'} -H "Content-Type:application/json
app.post('/login',  express.json({type: 'application/json'}), async function (req, res) {
  var data = req.body; 
  if(!req.body || !('user' in req.body)){
    res.send({"error" : "No user..."}); 
    return; 
  }

  var id; 
  var d = await db.get(`SELECT * FROM Users WHERE UserID = ?`, data.user);
  if(d === undefined){ // Create the user if they don't exist.
    id = await createUser(data.user, 0); 
    d = await db.get(`SELECT * FROM Users WHERE UserID = ?`, data.user);
    id = d['UserID'];
  }
  else{
    id = d['UserID'];
  }

  // MaxNote: If the value is undefined, then it's removed from the response. Weird!
  res.send({"error" : false, "ID" : id});
  return; 
}); 

async function createHitman(){
  const products = (await stripe.products.list({
  }))['data']; 

  if(products.length > 0){
    product_id = products[0]['id'];  // Just take the first one
    return; 
  }

  // Create the product if it doesn't exist.
  const product = await stripe.products.create({
    name: 'Hitman',
  });

  // Call again to set the product info
  await createHitman(); 
  return; 
}

async function createPrice(){

  const prices = (await stripe.prices.list({
    limit: 3,
    product: product_id, 
    active : true
  }))['data']; 

  if(prices.length > 0){
    price_id = prices[0]['id']; 
    return; 
  }

  const price = await stripe.prices.create({
    unit_amount: 200000, // $2000
    currency: 'usd',
    product: product_id,
  });
  
  // Call again to set it.
  await createPrice();
}

async function setupWebhook(){

  const webhookEndpoints = await stripe.webhookEndpoints.list({
  limit: 3,
});

  console.log(webhookEndpoints)
  if(webhookEndpoints.data.length > 1){
     return; 
  }

  // TODO - get IP address/domain dynamically here
  const endpoint = await stripe.webhookEndpoints.create({
    url: "http://" + "maxwelldulin.com" + ":5000/webhook",
    enabled_events: [
      'checkout.session.completed'
    ],
  });
}

async function getRemoteIp(){
  var options = {
    host: 'api.ipify.org',
    port: 80,
    path: '/'
  };
  
  http.get(options, function(res) {
    res.setEncoding('utf8')
    res.on("data", function(chunk) {
      console.log(chunk); 
      ip = chunk;
    });
  });
}

async function initDb(){

  // Individual user tracking
  query2 = "CREATE TABLE Users (UserID VARCHAR PRIMARY KEY, Amount Integer) "; 
  await db.exec(query2);

  // Create session management for orders
  var query = "CREATE TABLE Orders(ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID VARCHAR, Amount Integer, Session TEXT, FOREIGN KEY(UserID) REFERENCES Users(UserID)) "; 
  await db.exec(query); 
}

async function createUser(name, amount){
  return (await db.run("INSERT INTO Users(UserID,Amount) VALUES(?,?)", [name, amount]));
}

async function updateUser(id, amount){
  return (await db.run("UPDATE Users SET Amount = ? WHERE UserID = ?", [amount, id]));
}

async function createOrder(UserId, Session){
  return (await db.run("INSERT INTO Orders(UserID, Amount, Session) VALUES (?,1,?)", [UserId, Session]));
}

async function testData(){
  await createUser("Maxwell", 1)
}

async function init(){
  await createHitman(); 
  await createPrice();
  await getRemoteIp();

  try{
    await initDb(); 
    await testData();
  }

  catch(err){
    console.log("DB already created..."); 
  }
  await setupWebhook();
}


/*
stripe.prices.update(  'price_1NfsKxE8bmyyMPHw8sJC7vQk'
,{
  active: false
})

*/

//stripe.webhookEndpoints.del('we_1Ng9KXE8bmyyMPHwI5h9jfZ9')
init();

app.listen(5000);





