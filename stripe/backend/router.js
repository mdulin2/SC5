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


// curl -X POST http://127.0.0.1:5000/webhook --data '{"type" : "payment_intent.succeeded"}' -H 'Content-Type: application/json'
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
      case 'payment_intent.succeeded':

        if(!event.data){
          result = {"type" : "Missing 'data' in body"}
          break;
        }

        if(!('object' in event.data)){
          result = {"type" : "Missing 'data.object' in body"}
          break; 
        }

        const paymentIntent = event.data.object;
        // TODO: Add to DB or something...
        console.log(paymentIntent); 
        break;

      default:
        result = {"type" : "unknown 'type'"}
    }
  
    // Return a response to acknowledge receipt of the event
    res.json(result);
});

// curl -X POST http://127.0.0.1:5000/stripe
app.post('/stripe', async function (req, res) {
  console.log("Price Id:", price_id); 

  const session = await stripe.checkout.sessions.create({
    
    success_url: 'https://maxwelldulin.com/success',
    line_items: [
      {price: price_id, quantity: 1},
    ],
    mode: 'payment',
  });

  console.log(session.url); 

  // Track this info in the 'Orders' table.
  res.send({"redirect_url" :session.url});

  // Where to redirect the page to - Stripe!
  return session.url; 
});


// Not the vuln :) Just trying to make it easier to use!
app.post('/login',  express.json({type: 'application/json'}), async function (req, res) {
  var data = req.body; 
  if(!req.body || !('user' in req.body)){
    res.send({"error" : "No user..."}); 
    return; 
  }

  var id; 
  var d = await db.get(`SELECT * FROM Users WHERE Name = ?`, data.user);
  if(d === undefined){ // Create the user if they don't exist.
    id = await createUser(data.user, 0); 
    d = await db.get(`SELECT * FROM Users WHERE Name = ?`, data.user);
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
  // TODO - get IP address/domain dynamically here
  const endpoint = await stripe.webhookEndpoints.create({
    url: ip + ":5000/webhook",
    enabled_events: [
      'payment_intent.payment_failed',
      'payment_intent.succeeded',
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
  query2 = "CREATE TABLE Users (UserID INTEGER PRIMARY KEY AUTOINCREMENT, Name VARCHAR, Amount Integer) "; 
  await db.exec(query2);

  // Create session management for orders
  var query = "CREATE TABLE Orders(ID INTEGER PRIMARY KEY AUTOINCREMENT, UserID INTEGER, Amount Integer, Session TEXT, FOREIGN KEY(UserID) REFERENCES Users(UserID)) "; 
  await db.exec(query); 

}

async function createUser(name, amount){
  return (await db.run("INSERT INTO Users(Name,Amount) VALUES(?,?)", [name, amount]));
}

async function testData(){
  await createUser("Maxwell", 1000); 
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
  // await setupWebhook();
}


/*
stripe.prices.update(  'price_1NfsKxE8bmyyMPHw8sJC7vQk'
,{
  active: false
})
*/
init();

app.listen(5000);





