
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
}

// https://www.geeksforgeeks.org/how-to-run-javascript-from-python/
function executeCall(array_input){
	start(); 
  	var execute_result = execute(array_input); 

	return execute_result; 
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function func1(){
  userTotal += var1; 
  console.log("Adding func1: ", var1);
}

function func2(){
  userTotal += var2; 
  console.log("Adding func2: ", var2);

}

function func3(param1){
  if(param1 === "ROP"){
    userTotal += var3; 
    console.log("Adding func3: ", var3);

  }else{
    console.log("Missed func3 :(");
  }
}

function func4(){
  userTotal += var4; 
  console.log("Adding func4: ", var4);
}

function func5(param1, param2){
  console.log(param1, param2)
  if(param1 === "1337" && param2 === "0x8000000"){
    userTotal += var5; 
    console.log("Adding func5: ", var5);

  }else{
    console.log("Missed func5 :(")
  }
}

function func6(){
  userTotal += var6; 
  console.log("Adding func6: ", var6);

}

function func7(){
  userTotal += var7; 
  console.log("Adding func7: ", var7);

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

 //for (elt of arr) { // Should the iteration be flipped?
 for(var index=0; index < arr.length; index++){
	var elt = arr[index]; 


      if(elt === "func1"){
        func1(); 
      }
      else if(elt === "func2"){
        func2(); 
      }
      else if(elt === "func4"){
        func4(); 
      }
      else if(elt === "func6"){
        func6(); 
      }
      else if(elt === "func7"){
        func7(); 
      }
      else if(elt == "func3"){
        func3(storage[0]);
        storage = [];
      }
      else if(elt == "func5"){
        func5(storage[1], storage[0]);
        storage = [];
      }
     else{
      console.log("Storage!?"); 
      storage.push(elt); 
    }
 }

  // Did a win occur?
  return didWin(); 
}

function callGlobal(){
	return global; 
}