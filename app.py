from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)

@app.route('/')
def test():
    return render_template('home.html')

@app.route('/customers', methods=['GET'])
def show_customer():
    customers = [{
        'id': 100,
        'fname': 'Max',
        'lname': 'lind',
        'street': '123 Fake Street',
        'city': 'San Antonio',
        'state': 'Texas',
        'zip': '78259',
        'email': 'maxlind@yahoo.com',
        'phone': '(432) 786-9087'
        },
        {
        'id': 101,
        'fname': 'Max',
        'lname': 'lind',
        'street': '123 Fake Street',
        'city': 'San Antonio',
        'state': 'Texas',
        'zip': '78259',
        'email': 'maxlind@yahoo.com',
        'phone': '(432) 786-9087'
        },
        {
        'id': 102,
        'fname': 'Max',
        'lname': 'lind',
        'street': '123 Fake Street',
        'city': 'San Antonio',
        'state': 'Texas',
        'zip': '78259',
        'email': 'maxlind@yahoo.com',
        'phone': '(432) 786-9087'
        }
    ]

    return render_template('customers.html', customers=customers)
    

@app.route('/customers/add-customer')
def add_customer():
    return render_template('addcustomer.html')


@app.route('/distributors')
def show_distributor():

    distributors = [{
        'id': 100,
        'name': 'Record Warehouse',
        'street': '456 Dist Street',
        'city': 'Los Angeles',
        'state': 'California',
        'zip': '78259',
        'phone': '(888) 703-6517'
        },
        {
        'id': 101,
        'name': 'Record Warehouse',
        'street': '456 Dist Street',
        'city': 'Los Angeles',
        'state': 'California',
        'zip': '78259',
        'phone': '(888) 703-6517'
        },
        {
        'id': 102,
        'name': 'Record Warehouse',
        'street': '456 Dist Street',
        'city': 'Los Angeles',
        'state': 'California',
        'zip': '78259',
        'phone': '(888) 703-6517'
        },
    ]
    return render_template('distributors.html', distributors=distributors)

@app.route('/distributors/add-distributor')
def add_distributor():

    return render_template('adddistributor.html')




@app.route('/products')
def show_inventory():
    
    return render_template('products.html')

@app.route('/products/add-product')
def add_inventory():
    
    return render_template('products.html')