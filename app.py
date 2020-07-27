from flask import Flask, render_template, jsonify, make_response, request, redirect, url_for
import requests
import random
from random import randint
# import grequests
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
        distributors = 'SELECT distributorID, name, street, city, state, zip, phone FROM distributors'
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
@app.route('/distributors/add-distributor', methods=['POST', 'GET'])
def add_distributor():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        name = request.form['distName']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        phone = request.form['phone']
        zip_code = request.form['zip']

        add_dist = f"INSERT INTO distributors(name, street, city, state, zip, phone) VALUES ('{name}', '{street}', '{city}', '{state}', '{zip_code}', '{phone}')"
            
        dist_query = execute_query(sql_connection, add_dist).fetchall()
        return redirect(url_for('create_inventory', name=name))
    
    return render_template('forms.html', title='Add Distributor')


# CREATES DISTRIBUTOR INVENTORY
@app.route('/distributors/add-distributor/add-inventory')
def create_inventory():
    name = request.args['name']
    print(name)
    sql_connection = connect_to_database()

    # get distributor newly created distributor ID
    get_dist = f"SELECT distributorID from distributors WHERE name='{name}'"
    dist = execute_query(sql_connection, get_dist).fetchall()
    dist_id = dist[0]['distributorID']


    payload = {}
    genres = ['country', 'blues', 'rock', 'pop', 'funk', 'hip-hop']

    for i in range(1, 10):
        genre = random.choice(genres)
       
        url = f"https://api.discogs.com/database/search?genre='{genre}'&page={i}&key=yAkaOKZIxeKFgRSyIXEY&secret=hbaRZHEfvIVguItMHliaGvliDAJVbBCw"
        response = requests.request("GET", url, data = payload)
        response = response.json()
        
        for j in range(0, 20):
            key = 'year'
            if key in response['results'][j]:
                title = response['results'][j]['title']
                title = title.replace("'", "\\'")
                
                
                year = response['results'][j]['year']
                price = randint(3, 50)
                quantity = randint(0, 50)
                img = response['results'][j]['cover_image']
                
                insert_inventory = f"INSERT INTO distInventory(distributorID, title, year, price, quantity, img) VALUES ({dist_id}, '{title}', '{year}', {price}, {quantity}, '{img}')"
                execute_insert = execute_query(sql_connection, insert_inventory)
    

    return redirect('/distributors')


# VIEW DISTRIBUTOR INVENTORY
@app.route('/distributors/view-inventory', methods=['POST', 'GET'])
def view_dist_inventory():
    if request.method == 'POST':
        print(request.form['dist_id'])
        dist_name = request.form['dist_name']
        dist_id = request.form['dist_id']
        sql_connection = connect_to_database()
        
        inventory_query = f"SELECT title, year, price, quantity, img FROM distInventory WHERE distributorID={dist_id}"
        inventory = execute_query(sql_connection, inventory_query).fetchall()
        

        return render_template('views.html', inventory=inventory, dist_name=dist_name)



# ADD PURCHASE
@app.route('/purchases/add-purchase')
def add_purchase():

    return render_template('forms.html', title='Add Purchase')


# ADD RECORDS
@app.route('/records/add-record')
def add_record():

    return render_template('forms.html', title='Add Record')



# CREATE ORDER
@app.route('/orders/add-order/select-distributor', methods=['POST', 'GET'])
def add_order():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        
        distributors = 'SELECT distributorID, name, street, city, state, zip, phone FROM distributors'
        distributors_query = execute_query(sql_connection, distributors).fetchall()
        return render_template('forms.html', title='Create Order', distributor_order=distributors_query)


    if request.method == 'POST':
        dist_name = request.form['Distributor']
        print(dist_name)
        dist_inventory_query = f"SELECT title, year, price, quantity, img FROM distInventory WHERE distributorID=(SELECT distributorID FROM distributors WHERE name='{dist_name}')"
        dist_inventory = execute_query(sql_connection, dist_inventory_query).fetchall()
        return render_template('forms.html', dist_inventory=dist_inventory)


# Javascript Routes
