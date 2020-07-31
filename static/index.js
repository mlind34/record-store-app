let dataTable = document.getElementById('dataTable');
// console.log(dataTable);
let buttons = dataTable.querySelectorAll('input');
// console.log(buttons);

// for(let i in buttons) {
console.log(dataTable);
let buttons = document.querySelectorAll('input');
console.log(buttons);
recordsAdded = [];
for(let i in buttons) {

  // if(buttons[i].value == 'Purchases') {
    //   let data = {
    //     id: buttons[i].id
    //   };
      //contextJson = JSON.stringify(context);
      // buttons[i].addEventListener("click", (event) => {
        // let subReq = new XMLHttpRequest();
        // subReq.open("POST", "http://flip3.engr.oregonstate.edu:5199/custpurchases", true);
        // subReq.setRequestHeader("content-type", "application/json");
        // subReq.addEventListener("load", () => {
        //     document.querySelector('html').innerHTML = subReq.response;
        // })
        // data = JSON.stringify(data);
        // subReq.send(data);
        // event.preventDefault();
        // window.location.href = '/custpurchases/'+buttons[i].id

        // fetch('http://flip3.engr.oregonstate.edu:5199/custpurchases', {
        //     method: 'POST',
        //     mode: 'cors',
        //     headers: {
        //         'content-type': 'application/json'
        //     },
        //     body: contextJson,
        // }).then(function (response) {
        //     console.log(response);
        // })
//       })
//   }
// }


dataTable.addEventListener('click', (event) =>{
    let target = event.target;
    if(target.value == 'Update'){
        enableRow(target.id);
        console.log(target)
        pageType = target.parentNode.parentNode.getAttribute('name')
        let confirm = makeConfirm(target)
        console.log(pageType)
        confirm.addEventListener('click', function(){
            let data = document.getElementsByClassName('update-data')
            let id = target.id
            
            if(pageType == 'customer') {
                let first = data['firstName'].value
                let last = data['lastName'].value
                let str = data['street'].value
                let c = data['city'].value
                let st = data['state'].value
                let z = data['zip'].value
                let ph = data['phone'].value
                let em = data['email'].value
                updateCustomer(pageType, id, first, last, str, c, st, z, ph, em)
            }
            if(pageType == 'distributor') {
                let name = data['name'].value
                let street = data['street'].value
                let city = data['city'].value
                let state = data['state'].value
                let zip = data['zip'].value
                let phone = data['phone'].value
                updateDist(pageType, id, name, street, city, state, zip, phone)
            }

            
        })
    }
    event.preventDefault() 
});

function enableRow(id) {
    let row = document.getElementById(id);
    let cells = row.getElementsByClassName('table-input')
    for(let i = 0; i < cells.length; i++){
        let name = cells[i].getAttribute('name')
        let value = cells[i].innerHTML
        createInput(cells[i], name, value)
    }
}

function createInput(cell, name, value) {
    let input = document.createElement('input');
    input.setAttribute('type', 'text');
    input.setAttribute('size', '10%')
    input.setAttribute('class', 'update-data')
    input.setAttribute('name', name);
    input.setAttribute('value', value);
    cell.innerText =''
    cell.append(input)
}

      
  
  if(buttons[i].value == 'Add to Order') {
    recordsAdded = [];
    buttons[i].addEventListener("click", (event) => {
      makeConfirm(buttons[i]);
      event.preventDefault;
      recordsAdded.push(buttons[i].id);
      console.log(recordsAdded);
    });
  }
  if(buttons[i].value == 'Submit Records for Order') {
    console.log("Test");
    data = {
      recordIDs: recordsAdded
    };
    buttons[i].addEventListener("click", (event) => {
      let subReq = new XMLHttpRequest();
        subReq.open("POST", "http://flip3.engr.oregonstate.edu:5199/purchases/add-purchase/final", true);
        subReq.setRequestHeader("content-type", "application/json");
        subReq.addEventListener("load", () => {
          // window.location.href = '/purchases/add-purchase/final'
        })
        data = JSON.stringify(data);
        subReq.send(data);
        event.preventDefault();
    });
  }
}

dataTable.addEventListener('click', (event) =>{
    let target = event.target;
    if(target.value == 'Update'){
        var confirm = makeConfirm(target)
        updateRow(target.id);
    }
});



// const updateRow = (id) => {
//     var rowToUpdate = document.getElementById(id);
    
//     dataCell = rowToUpdate.getElementsByClassName('table-input');

//     checkCell = rowToUpdate.getElementsByClassName('ui checkbox');

//     for(var i = 0; i < dataCell.length; i++){
  
//         input = document.createElement('input');

//         input.setAttribute('type', 'text');

//         input.setAttribute('size', '17');
        
//         input.setAttribute('value', dataCell[i].innerText);

//         dataCell[i].innerHTML = '';

//         dataCell[i].append(input);
       
//     }
// }

    // checkInput = document.createElement('input');
    // input.setAttribute('type', 'checkbox');
    // console.log(input)
    // if(checkCell.checked == True){
    //     input.setAttribute('checked', 'True')
    // } else {
    //     input.setAttribute('checked', 'False')
    // }
    // checkCell = input



const makeConfirm = (button) => {
    if(button.value == 'Update') {
      button.setAttribute('value', 'Confirm');
      button.style.backgroundColor = 'rgb(100, 150, 240)'
      return button;
    } else if (button.value == 'Add to Order') {
      button.setAttribute('value', 'Added');
      button.style.backgroundColor = 'rgb(100, 150, 240)'
      button.disabled = true;
      return button;
    }

}

function updateCustomer(pageType, id, first, last, str, c, st, z, ph, em) {
    let customerData = {pageType: null, id: null, firstName: null, lastName: null, street: null, city: null, state: null, zip: null, phone: null, email: null}
    customerData.pageType = pageType
    customerData.id = id
    customerData.firstName = first
    customerData.lastName = last
    customerData.street = str
    customerData.city = c
    customerData.state = st
    customerData.zip = z
    customerData.phone = ph
    customerData.email = em
    updateRequest(customerData)
}
    
function updateDist(pageType, id, name, street, city, state, zip, phone) {
    let distData = {pageType: null, id: null, name: null, street: null, city: null, state: null, zip: null, phone: null}
    distData.pageType = pageType
    distData.id = id
    distData.name = name
    distData.street = street
    distData.city = city
    distData.state = state
    distData.zip = zip
    distData.phone = phone
    updateRequest(distData)
}
    

function updateRequest(postData){
    let req = new XMLHttpRequest()
    req.open("POST", "http://flip1.engr.oregonstate.edu:3457/update", true);
        req.setRequestHeader("content-type", "application/json");
        req.addEventListener("load", () => {
            if (req.status >= 200 && req.status < 400){
                if (postData['pageType'] == 'customer'){
                window.location.href = '/customers'
                } 
                if (postData['pageType'] == 'distributor') {
                    window.location.href = '/distributors'
                }
                console.log('success')
            } else {
                console.log('error in network request' + req.statusText)
            }
        });

        req.send(JSON.stringify(postData))
        event.preventDefault()

}
