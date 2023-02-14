const hostName = 'localhost'

function guessNumber(number) {
    const Http = new XMLHttpRequest();
    const url='http://'+ hostName + ':5000/guess/'+ window.location.search.split('user=')[1] + '/' + number;
    Http.onreadystatechange = (e) => {
        p = document.getElementsByClassName("alert")[0];
        p.innerHTML = Http.responseText;
    }
    
    Http.open("GET", url);
    Http.send();
}

function validateGuess() {
    const Http = new XMLHttpRequest();
    const url='http://'+ hostName + ':5000/validate/' + window.location.search.split('user=')[1];
    Http.onreadystatechange = (e) => {
        p = document.getElementsByClassName("alert")[0];
        p.innerHTML = Http.responseText;
    }
    
    Http.open("GET", url);
    Http.send();
}

function register(userName) {
    const Http = new XMLHttpRequest();
    const url='http://'+ hostName+ ':5000/register/' + userName;
    console.log('registered');
    Http.onreadystatechange = (e) => {
        //console.log(Http.readyState);
        if (Http.readyState === XMLHttpRequest.DONE) {
            p = document.getElementsByClassName("alert")[0];
            p.innerHTML = Http.responseText;
            window.location.href = 'http://'+ hostName + ':8091/lottery.html?user=' + userName;
            console.log('registered and reroute');
        }
        console.log(e);
    }
    
    Http.open("GET", url);
    Http.send();
}

function getPrevious() {
    const Http = new XMLHttpRequest();
    const url='http://'+ hostName + ':5000/history';
    Http.onreadystatechange = (e) => {
        if (Http.readyState === XMLHttpRequest.DONE) {
            ul = document.createElement('ul');
            document.getElementById('myItemList').appendChild(ul);
            var obj = JSON.parse(Http.responseText);
            (obj['History']).forEach(function (item) {
                let li = document.createElement('li');
                ul.appendChild(li);
                li.innerHTML += item;
            });
        }
    }
    
    Http.open("GET", url);
    Http.send();
}
