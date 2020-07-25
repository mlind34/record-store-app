from flask import Flask, render_template, request, jsonify, make_response, redirect
from db_connect import connect_to_database, execute_query
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

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
    sql_connection = connect_to_database()
    if request.method == 'GET':
        customers = 'SELECT customerID, firstName, lastName, street, city, state, zip, phone, email FROM customers'
        customers_query = execute_query(sql_connection, customers).fetchall()
        return render_template('views.html', customers=customers_query, title='Customers')


# DISTRIBUTORS
@app.route('/distributors', methods=['POST', 'GET'])
def show_distributor():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        distributors = 'SELECT name, street, city, state, zip, phone FROM distributors'
        distributors_query = execute_query(sql_connection, distributors).fetchall()
        return render_template('views.html', distributors=distributors_query, title='Distributors')


# RECORDS 
@app.route('/records', methods=['POST', 'GET'])
def show_records():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        records = 'SELECT name, artist, year, price, quantity, distributor FROM records'
        records_query = execute_query(sql_connection, records).fetchall()
        return render_template('views.html', records=records_query, title='Records')



# PURCHASES
@app.route('/purchases', methods=['POST', 'GET'])
def view_purchases():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        purchases = 'SELECT purchaseDate, paymentMethod, totalPrice FROM purchases'
        purchases_query = execute_query(sql_connection, purchases).fetchall()
        return render_template('views.html', purchases=purchases_query, title='Purchases')



# ORDERS
@app.route('/orders', methods=['POST', 'GET'])
def view_orders():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        orders = 'SELECT orderDate, orderFilled, distributor FROM orders'
        orders_query = execute_query(sql_connection, orders).fetchall()
        return render_template('views.html', orders=orders_query, title='Orders')


# Use this or repurpose existing Purchases page for individual customer puchase SELECT
@app.route('/custpurchases/<var>', methods=['GET'])
def view_cust_purchases(var):
    id = var
    print(id)
    sql_connection = connect_to_database()
    purchases = 'SELECT purchaseDate, paymentMethod, totalPrice FROM purchases INNER JOIN customers ON customers.customerID = '+ id +' AND purchases.customerID = '+id
    name = 'SELECT firstName, lastName FROM customers WHERE customers.customerID = '+id
    purchases_query = execute_query(sql_connection, purchases).fetchall()
    name_query = execute_query(sql_connection, name).fetchall()
    if not purchases_query:
        #so table header row shows up
        purchases_query = ["noData"]
    firstName = name_query[0]['firstName']
    lastName = name_query[0]['lastName']
    return render_template('views.html', custpurchase=purchases_query, title= firstName+' '+lastName+' Purchases')






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



# Javascript Routes
