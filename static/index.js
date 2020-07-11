

const baseUrl = 'http://flip2.engr.oregonstate.edu:6743/customers'

// Post new info to table
const postTest = () => {
    var req = new XMLHttpRequest();
    
    req.open("POST", baseUrl, true);
    req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    req.addEventListener('load', function(){
        if(req.status >= 200 && req.status < 400){
            console.log(this.responseText)   
        } else {
            console.log('error in network request ' + req.statusText);
        }
    });
    req.send();
    event.preventDefault();
}

testBtn.addEventListener('click', function(){
    postTest();
})