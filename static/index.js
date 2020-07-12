function addCustomer() {

    let name = document.getElementById('addCustomer');

    let customer = {
        name: name.value
    }

    fetch(`${window.origin}/customers/add-customer`, {
        method: "POST",
        credentials: "include",
        body: JSON.stringify(customer),
        cache: "no-cache",
        headers: new Headers({
            "content-type": "application/json"
        })
    
    }).then(function(response) {

        if (response.status !== 200){
            
            console.log(`Error in request ${response.status}`);

            return ;

        }

        response.json().then(function(data) {

            console.log(data)

        })

    })

}