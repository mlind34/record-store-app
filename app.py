from flask import Flask, render_template, request, jsonify, make_response
app = Flask(__name__)

@app.route('/')
def test():
    return render_template('home.html')

@app.route('/customers')
def show_customer():
    customers = [
        {
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
        'fname': 'Alex',
        'lname': 'DeWald',
        'street': '456 Another Fake Street',
        'city': 'Lincoln',
        'state': 'Nebraska',
        'zip': '79872',
        'email': 'alexdewald@yahoo.com',
        'phone': '(231) 901-2356'
        },
        {
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
        'fname': 'Alex',
        'lname': 'DeWald',
        'street': '456 Another Fake Street',
        'city': 'Lincoln',
        'state': 'Nebraska',
        'zip': '79872',
        'email': 'alexdewald@yahoo.com',
        'phone': '(231) 901-2356'
        }
    ]

    return render_template('customers.html', title='Customers', customers=customers)
    

@app.route('/customers/add-customer')
def add_customer():
    
    return render_template('addcustomer.html')




