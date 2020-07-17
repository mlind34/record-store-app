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




