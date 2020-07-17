from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/home')
def home():
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

    return render_template('customers.html', customers=customers, title='Customers')
    

@app.route('/customers/add-customer')
def add_customer():
    return render_template('addcustomer.html', title='Add Customer')


@app.route('/distributors')
def show_distributor():

    distributors = [{
        'id': 200,
        'name': 'Record Warehouse',
        'street': '456 Dist Street',
        'city': 'Los Angeles',
        'state': 'California',
        'zip': '78259',
        'phone': '(888) 703-6517'
        },
        {
        'id': 201,
        'name': 'Record Warehouse',
        'street': '456 Dist Street',
        'city': 'Los Angeles',
        'state': 'California',
        'zip': '78259',
        'phone': '(888) 703-6517'
        },
        {
        'id': 202,
        'name': 'Record Warehouse',
        'street': '456 Dist Street',
        'city': 'Los Angeles',
        'state': 'California',
        'zip': '78259',
        'phone': '(888) 703-6517'
        },
    ]
    return render_template('distributors.html', distributors=distributors, title='Distributors')

@app.route('/distributors/add-distributor')
def add_distributor():

    return render_template('addistributor.html', title='Add Distributor')




@app.route('/records')
def show_records():
    records = [{
        'id': 200,
        'price': 'Record Warehouse',
        'quantity': '456 Dist Street',
        'year': 'Los Angeles',
        'artist': 'California',
        'type': '78259',
        'name': '(888) 703-6517'
        },
        {
        'id': 201,
        'price': 'Record Warehouse',
        'quantity': '456 Dist Street',
        'year': 'Los Angeles',
        'artist': 'California',
        'type': '78259',
        'name': '(888) 703-6517'
        },
        {
        'id': 201,
        'price': 'Record Warehouse',
        'quantity': '456 Dist Street',
        'year': 'Los Angeles',
        'artist': 'California',
        'type': '78259',
        'name': '(888) 703-6517'
        },
    ]
    return render_template('records.html', records = records, title='Records')

@app.route('/records/add-record')
def add_record():

    return render_template('addrecord.html', title='Add Record')

@app.route('/purchases')
def view_purchases():
    purchases = [
        {
            'id': 709,
            'purchaseDate': '01-23-2019',
            'paymentMethod': 'Card',
            'paid': True,
            'totalPrice': 56.98 
        },
        {
            'id': 710,
            'purchaseDate': '11-29-2017',
            'paymentMethod': 'Cash',
            'paid': True,
            'totalPrice': 45.18 
        },
        {
            'id': 711,
            'purchaseDate': '05-03-2018',
            'paymentMethod': 'Card',
            'paid': True,
            'totalPrice': 5.67 
        }
    ]
    return render_template('purchases.html', purchases=purchases, title='Purchases')


@app.route('/purchases/add-purchase')
def add_purchase():

    return render_template('addpurchase.html', title='Add Purchase')


@app.route('/orders')
def view_orders():
    return render_template('orders.html', title='Orders')


@app.route('/orders/add-order')
def add_order():
    return render_template('addorder.html', title='Add Order')