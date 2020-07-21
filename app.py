from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)

# 
# VIEWS
# 

# INDEX 
@app.route('/')
def index():
    return render_template('index.html')

# HOME
@app.route('/home')
def home():
    return render_template('home.html')

# CUSTOMERS
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

    return render_template('views.html', customers=customers, title='Customers')


# DISTRIBUTORS
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
        'name': 'Records R Us',
        'street': '123 Pike St',
        'city': 'Seattle',
        'state': 'washington',
        'zip': '98256',
        'phone': '(206) 712-3449'
        },
        {
        'id': 202,
        'name': 'House of Vinyl',
        'street': '789 Stock Pl',
        'city': 'Austin',
        'state': 'Texas',
        'zip': '76782',
        'phone': '(800) 178-3789'
        },
    ]
    return render_template('views.html', distributors=distributors, title='Distributors')


# RECORDS 
@app.route('/records')
def show_records():
    records = [{
        'id': 500,
        'price': '40',
        'quantity': '5',
        'year': '1970',
        'artist': 'The Beatles',
        'name': "Let It Be",
        'distributor': "Record Warehouse"
        },
        {
        'id': 501,
        'price': '18',
        'quantity': '2',
        'year': '1973',
        'artist': 'Black Sabbath',
        'name': 'Sabbath Bloody Sabbath',
        'distributor': "Records R Us"
        },
        {
        'id': 701,
        'price': '28',
        'quantity': '3',
        'year': '1968',
        'artist': 'Aretha Franklin',
        'name': 'Aretha Now',
        'distributor': "NULL"
        },
    ]
    return render_template('views.html', records = records, title='Records')


# PURCHASES
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
    return render_template('views.html', purchases=purchases, title='Purchases')


# ORDERS
@app.route('/orders')
def view_orders():
    orders = [
        {
            'order_id': 2018785,
            'order_date': '10-13-2016',
            'filled': True
        },
        {
            'order_id': 2015678,
            'order_date': '02-05-2019',
            'filled': False
        }
    ]

    return render_template('views.html', title='Orders', orders=orders)



# 
# FORMS
# 




# ADD CUSTOMER
@app.route('/customers/add-customer')
def add_customer():
    return render_template('forms.html', title='Add Customer')
    

# ADD DISTRIBUTOR
@app.route('/distributors/add-distributor')
def add_distributor():

    return render_template('forms.html', title='Add Distributor')

# ADD PURCHASE
@app.route('/purchases/add-purchase')
def add_purchase():

    return render_template('forms.html', title='Add Purchase')


# ADD RECORDS
@app.route('/records/add-record')
def add_record():

    return render_template('forms.html', title='Add Record')

# ADD ORDER
@app.route('/orders/add-order')
def add_order():

    return render_template('forms.html', title='Add Order')