
/*
Mimicing the famous Horcrux's pwnable.kr challenge in JavaScript 

TODO: 
- Output logs to UI about WHICH functions were executed
- Create backend execution to output the flag.
*/

var userTotal = 0; 
var total = 0; 
var var1;
var var2;
var var3;
var var4;
var var5;
var var6;
var var7;
var logging_string; 

function start(){
	var1 = getRandomInt(10000000000); 
	var2 = getRandomInt(10000000000); 
	var3 = getRandomInt(10000000000); 
	var4 = getRandomInt(10000000000); 
	var5 = getRandomInt(10000000000); 
	var6 = getRandomInt(10000000000); 
	var7 = getRandomInt(10000000000); 
	
	userTotal = 0; 
	total = var1 + var2 + var3 + var4 + var5 + var6 + var7;
  logging_string = "";
}

function executeCall(){
	start(); 
	
	var array_input = document.getElementById("array_input").value;
	array_input = JSON.parse(
		array_input
	); 

  console.log(array_input); 
  var execute_result = execute(array_input); 

	var logging = document.getElementById("logging");
  logging.innerHTML = logging_string;

  // If we execute this...
  if(execute_result === true){
    logging.innerHTML = logging.innerHTML + "<br><br><b>Success!</b> :)"
  }
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function func1(){
  userTotal += var1; 
  console.log("Adding func1: ", var1);
  logging_string += "<br/>Adding func1: " + var1; 
}

function func2(){
  userTotal += var2; 
  console.log("Adding func2: ", var2);
  logging_string += "<br/>Adding func2: " + var2; 

}

function func3(param1){
  logging_string += "<br/>Param1: " + param1; 
  if(param1 === "ROP"){
    userTotal += var3; 
    console.log("Adding func3: ", var3);
    logging_string += "<br/>Adding func3: " + var3; 

  }else{
    console.log("Missed func3 :(");
    logging_string += "<br/>Missed func3 :("; 
  }
}

function func4(){
  userTotal += var4; 
  console.log("Adding func4: ", var4);
  logging_string += "<br/>Adding func4: " + var4; 
}

function func5(param1, param2){
  logging_string += "<br/>Param1: " + param1; 
  logging_string += "<br/>Param2: " + param2; 

  if(param1 === "1337" && param2 === "0x8000000"){
    userTotal += var5; 
    logging_string += "<br/>Adding func5: " + var5; 
    console.log("Adding func5: ", var5);

  }else{
    console.log("Missed func5 :(")
    logging_string += "<br/>Missed func5 :("; 
  }
}

function func6(){
  userTotal += var6; 
  console.log("Adding func6: ", var6);
  logging_string += "<br/>Adding func6: " + var6; 

}

function func7(){
  userTotal += var7; 
  console.log("Adding func7: ", var7);
  logging_string += "<br/>Adding func7: " + var7; 

}

function didWin(){
  if(total === userTotal){
    return true; 
  }

  return false; 
}

// Execute the function
function execute(arr){

 var storage = []; // Parameter storage

 for (elt of arr) { // Should the iteration be flipped?

    // Function pointers to call
    if(elt.startsWith("func")){
      const func = window[elt];  // Getting function to call dynamically. 'func1', 'func2', 'func...'
      if(storage.length === 0){
         func();
      }
      else if(storage.length === 1){
         func(storage[0]);
      }

      // TODO: Should I flip this?
      else if(storage.length === 2){
         func(storage[1], storage[0]);
      }
      storage = [];
    }
   
  // Parameters to add to th call
  else {
      storage.push(elt); 
    }
  } 

  // Did a win occur?
  return didWin(); 

}

// Set the default value
var array_input = document.getElementById("array_input");
array_input.value = '["func1", "func2"]'; 

/*
// USER INPUT

arr = [
	"func1", "func2", "ROP" ,"func3", "func4", "1337", "0x8000000", "func5", "func6", "func7"
]; 
execute(arr); 
didWin(); 
*/