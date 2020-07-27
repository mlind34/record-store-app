let dataTable = document.getElementById('dataTable');
console.log(dataTable);
let buttons = document.getElementsByTagName("input");
console.log(buttons);

for(let i in buttons) {
//   if(buttons[i].value === 'Delete') {
//       buttons[i].addEventListener("click", (event) => {
//             fetch('http://flip2.engr.oregonstate.edu:4521/delete')
//                 .then(function (response) {
//                     return response.text();
//                 }).then(function (text) {
//                      console.log('GET response text:');
//                     console.log(text); // Print the greeting as text
//                 });
//       })
//   }
}


// dataTable.addEventListener('click', (event) =>{
//     let target = event.target;
//     if(target.value == 'Update'){
//         var confirm = makeConfirm(target)
//         updateRow(target.id);
//     }
// });


const updateRow = (id) => {
    var rowToUpdate = document.getElementById(id);
    
    dataCell = rowToUpdate.getElementsByClassName('table-input');

    checkCell = rowToUpdate.getElementsByClassName('ui checkbox');

    for(var i = 0; i < dataCell.length; i++){
  
        input = document.createElement('input');

        input.setAttribute('type', 'text');

        input.setAttribute('size', '17')

        input.setAttribute('value', dataCell[i].innerText)

        dataCell[i].innerHTML = '';

        dataCell[i].append(input);
       
    }

    // checkInput = document.createElement('input');
    // input.setAttribute('type', 'checkbox');
    // console.log(input)
    // if(checkCell.checked == True){
    //     input.setAttribute('checked', 'True')
    // } else {
    //     input.setAttribute('checked', 'False')
    // }
    // checkCell = input

}


const makeConfirm = (button) => {
    button.setAttribute('value', 'Confirm');
    button.style.backgroundColor = 'rgb(100, 150, 240)'
    return button;
}

