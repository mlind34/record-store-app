// const customerTable = document.getElementById('customerTable');


// customerTable.addEventListener('click', function(){
//     let target = event.target;
//     if(target.value == 'Update'){
//         var confirm = makeConfirm(target)
//         updateRow(target.id);
//     }
// });


// const updateRow = (id) => {
//     var rowToUpdate = document.getElementById(id);
    
//     dataCell = rowToUpdate.getElementsByClassName('table-input');

//     for(var i = 0; i < dataCell.length; i++){
//         input = document.createElement('input');

//         input.setAttribute('type', 'text');

//         input.setAttribute('size', '17')

//         input.setAttribute('value', dataCell[i].innerHTML)

//         dataCell[i].innerHTML = '';

//         dataCell[i].append(input);
//     }
// }


// const makeConfirm = (button) => {
//     button.setAttribute('value', 'Confirm');
//     button.style.backgroundColor = 'rgb(100, 150, 240)'
//     return button;
// }


// fetch('http://flip2.engr.oregonstate.edu:4521/customers')
//     .then(function (response) {
//         return response.text();
//     }).then(function (text) {
//         console.log('GET response text:');
//         console.log(text); // Print the greeting as text
//     });

// // Send the same request
// fetch('http://flip2.engr.oregonstate.edu:4521/customers')
//     .then(function (response) {
//         return response.json(); // But parse it as JSON this time
//     })
//     .then(function (json) {
//         console.log('GET response as JSON:');
//         console.log(json); // Here’s our JSON object
//     })

