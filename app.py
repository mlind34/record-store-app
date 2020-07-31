from flask import Flask, render_template, jsonify, make_response, request, redirect, url_for
import requests
import random
import gevent
import subprocess
from random import randint
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
@app.route('/customers', methods=['GET', 'POST'])
def show_customer():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        customers = 'SELECT customerID, firstName, lastName, street, city, state, zip, phone, email FROM customers'
        customers_query = execute_query(sql_connection, customers).fetchall()
        return render_template('views.html', customers=customers_query, title='Customers')
    
    if request.method == 'POST':
        if request.form['submit_btn'] == 'Delete':
            customerID = request.form['customerID']
            delete_query = f"DELETE FROM customers WHERE customerID={customerID}"
            execute_query(sql_connection, delete_query)
            return redirect('/customers')

    

@app.route('/update', methods=['POST'])
def update_customer():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        
        data = request.get_json()

        print(data['pageType'])
        if data['pageType'] == 'customer':
            cust_id = data['id']
            firstName = data['firstName']
            lastName = data['lastName']
            street = data['street']
            city = data['city']
            state = data['state']
            zip_code = data['zip']
            phone = data['phone']
            email = data['email']

            cust_query = f"UPDATE customers SET firstName='{firstName}', lastName='{lastName}', street='{street}', city='{city}', state='{state}', zip='{zip_code}', phone='{phone}', email='{email}' WHERE customerID={cust_id}"
            execute_query(sql_connection, cust_query)

            return redirect('/customers')

        if data['pageType'] == 'distributor':
            dist_id = data['id']
            name = data['name']
            street = data['street']
            city = data['city']
            state = data['state']
            zip_code = data['zip']
            phone = data['phone']

            dist_query = f"UPDATE distributors SET name='{name}', street='{street}', city='{city}', state='{state}', zip='{zip_code}', phone='{phone}' WHERE distributorID={dist_id} "
            execute_query(sql_connection, dist_query)

            return redirect('/distributors')

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
@app.route('/customers/add-customer', methods=['POST', 'GET'])
def add_customer():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        firstName = request.form['first-name']
        lastName = request.form['last-name']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        email = request.form['email']
        phone = request.form['phone']
        add_customer = f"INSERT INTO customers(firstName, lastName, street, city, state, email, phone) VALUES ('{firstName}', '{lastName}', '{street}', '{city}', '{state}', '{email}', '{phone}')"
        customer_query = execute_query(sql_connection, add_customer).fetchall()
        return redirect('/customers')
    
    return render_template('forms.html', title = 'Add Customer')
    


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
        print(genre)
       
        url = f"https://api.discogs.com/database/search?genre='{genre}'&page={i}&key=yAkaOKZIxeKFgRSyIXEY&secret=hbaRZHEfvIVguItMHliaGvliDAJVbBCw"
        response = requests.request("GET", url, data = payload)
        response = response.json()
        
        for j in range(0, 20):
            key = 'year'
           
            if key in response['results'][j] and response['results'][j]['country'] == 'US':
                title = response['results'][j]['title']
     
                
                year = response['results'][j]['year']
                price = randint(3, 50)
                quantity = randint(0, 50)
                img = response['results'][j]['cover_image']
                
                insert_inventory = f'INSERT INTO distInventory(distributorID, title, year, price, quantity, img) VALUES ({dist_id}, "{title}", "{year}", {price}, {quantity}, "{img}")'
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
@app.route('/records/add-record', methods=['POST', 'GET'])
def add_record():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        name = request.form['name']
        artist = request.form['artist']
        price = request.form['price']
        quantity = request.form['quantity']
        year = request.form['year']
        distributor = request.form['distributor']
        add_record = f"INSERT INTO records(name, artist, year, price, quantity, distributor) VALUES ('{name}', '{artist}', '{year}', '{price}', '{quantity}', '{distributor}')"
        record_query = execute_query(sql_connection, add_record).fetchall()


        return redirect('/records')
    
    return render_template('forms.html', title = 'Add Record')



# SELECT DISTRIBUTOR
@app.route('/orders/add-order/select-distributor', methods=['POST', 'GET'])
def select_dist():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        
        distributors = 'SELECT distributorID, name, street, city, state, zip, phone FROM distributors'
        distributors_query = execute_query(sql_connection, distributors).fetchall()
        return render_template('forms.html', title='Create Order', distributor_order=distributors_query)

# CREATE ORDER
@app.route('/orders/add-order/create-order', methods=['GET', 'POST'])
def create_order():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        dist_name = request.form['Distributor']
        print(dist_name)
        dist_inventory_query = f"SELECT title, year, price, quantity, img FROM distInventory WHERE distributorID=(SELECT distributorID FROM distributors WHERE name='{dist_name}')"
        dist_inventory = execute_query(sql_connection, dist_inventory_query).fetchall()
        return render_template('forms.html', dist_inventory=dist_inventory, dist_name=dist_name)

# CONFIRM ORDER
@app.route('/orders/add-order/confirm-order', methods=['GET', 'POST'])
def confirm_order():
    if request.method == 'POST':
        print(request.form)

    return render_template('views.html', title='Order Confirmed')


