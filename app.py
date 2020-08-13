from flask import Flask, render_template, jsonify, make_response, request, redirect, url_for
import requests
import random
import gevent
import subprocess
import json

from random import randint
from db_connect import connect_to_database, execute_query
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 
# VIEW ROUTES
# 

# INDEX ROUTE
@app.route('/')
def index():
    """Index and information page"""
    return render_template('index.html')


# HOME ROUTE
@app.route('/home')
def home():
    """Home page"""
    return render_template('home.html')


# CUSTOMERS
@app.route('/customers', methods=['GET', 'POST'])
def show_customer():
    """Displays all customers"""

    sql_connection = connect_to_database()
    
    # Navigation to customers page, retrieves latest customer information from database
    if request.method == 'GET':
        customers = 'SELECT customerID, firstName, lastName, street, city, state, zip, phone, email FROM customers'
        customers_query = execute_query(sql_connection, customers).fetchall()
        
        return render_template('views.html', customers=customers_query, title='Customers')
    
    # Post request handles delete button, delete query deletes customer by ID and redirects to the get request route to reload the page without deleted customer
    if request.method == 'POST':
        if request.form['submit_btn'] == 'Delete':
            customerID = request.form['customerID']
            delete_query = f"DELETE FROM customers WHERE customerID={customerID}"
            execute_query(sql_connection, delete_query)
            
            return redirect('/customers')


# DISTRIBUTORS
@app.route('/distributors', defaults={'city_info': None, 'name_info': None}, methods=['POST', 'GET'])
@app.route('/distributors/<city_info>/<name_info>', methods=['POST', 'GET'])
def show_distributor(city_info, name_info):
    """Displays all distributors"""

    sql_connection = connect_to_database()
    
    if request.method == 'GET':
        distributors_query = 'SELECT distributorID, name, street, city, state, zip, phone FROM distributors'
        distributors = execute_query(sql_connection, distributors_query).fetchall()
        
    # post to handle search/filtering
    if request.method == 'POST':
        # search distributor by name
        if request.form.get('option') == 'name':
            name = request.form.get('search')
            name_query = f"SELECT name, street, city, state, zip, phone from distributors WHERE name='{name}'"
            name_info = execute_query(sql_connection, name_query).fetchall()

            # if no search results
            if not name_info:
                return render_template('views.html', title='No Search Results')

            return render_template('views.html', distributors=name_info)

        # search distributor by city
        if request.form.get('option') == 'city':
            city = request.form.get('search')
            city_query = f"SELECT name, street, city, state, zip, phone from distributors WHERE city='{city}'"
            city_info = execute_query(sql_connection, city_query).fetchall()
            # if no search results
            if not city_info:
                return render_template('views.html', title='No Search Results')
            
            return render_template('views.html', distributors=city_info)
            
    return render_template('views.html', distributors=distributors, title='Distributors')

    
# RECORDS ROUTE
@app.route('/records', methods=['POST', 'GET'])
def show_records():
    """Displays all records in the database"""

    sql_connection = connect_to_database()

    if request.method == 'GET':
        records = 'SELECT r.name, r.artist, r.year, r.price, r.img, r.quantity, d.name AS distributor FROM records r LEFT JOIN distributors d ON r.distributorID=d.distributorID'
        records_query = execute_query(sql_connection, records).fetchall()

        return render_template('views.html', records=records_query, title='Records')


# PURCHASES ROUTE
@app.route('/purchases', methods=['POST', 'GET'])
def view_purchases():
    """Displays all customer purchases, query retrieves purchase info related to customerID"""

    sql_connection = connect_to_database()

    if request.method == 'GET':
        purchases = 'SELECT purchases.purchaseID, purchases.purchaseDate, purchases.paymentMethod, purchases.totalPrice, \
        customers.firstName, customers.lastName FROM purchases LEFT JOIN customers ON customers.customerID=purchases.customerID'
        purchases_query = execute_query(sql_connection, purchases).fetchall()

        return render_template('views.html', purchases=purchases_query, title='Purchases')


# ORDERS ROUTE
@app.route('/orders', methods=['POST', 'GET'])
def view_orders():
    """Displays all orders"""

    sql_connection = connect_to_database()

    if request.method == 'GET':
        orders_query = "SELECT o.orderID, o.orderDate, o.distributorID, o.orderFilled, o.orderTotal, d.name AS distributor FROM orders o \
        INNER JOIN distributors d ON o.distributorID=d.distributorID ORDER BY orderID desc" 
        orders = execute_query(sql_connection, orders_query).fetchall()
        return render_template('views.html', orders=orders, title='Orders')


# CUSTOMER PURCHASES ROUTE
@app.route('/custpurchases/<var>', methods=['GET'])
def view_cust_purchases(var):
    """Displays purchases for specific customer"""

    # customerID
    id = var
    sql_connection = connect_to_database()

    purchases = 'SELECT purchaseID, purchaseDate, paymentMethod, totalPrice FROM purchases INNER JOIN customers ON customers.customerID = '+ id +' AND purchases.customerID = '+id
    name = 'SELECT firstName, lastName FROM customers WHERE customers.customerID = '+ id
    purchases_query = execute_query(sql_connection, purchases).fetchall()
    name_query = execute_query(sql_connection, name).fetchall()
    
    # if no purchase data
    if not purchases_query:
        purchases_query = ["noData"]

    firstName = name_query[0]['firstName']
    lastName = name_query[0]['lastName']

    return render_template('views.html', custpurchase=purchases_query, title= 'Purchases for ' + firstName + " " + lastName)


# 
# FORM ROUTES
# 


# ADD CUSTOMER
@app.route('/customers/add-customer', methods=['POST', 'GET'])
def add_customer():
    """Adds a new customer to the database"""

    sql_connection = connect_to_database()

    # form data
    if request.method == 'POST':
        firstName = request.form['first-name']
        lastName = request.form['last-name']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        zip_code = request.form['zip']
        email = request.form['email']
        phone = request.form['phone']
        add_customer = f"INSERT INTO customers(firstName, lastName, street, city, state, zip, email, phone) VALUES ('{firstName}', \
        '{lastName}', '{street}', '{city}', '{state}', {zip_code}, '{email}', '{phone}')"
        customer_query = execute_query(sql_connection, add_customer).fetchall()
        return redirect('/customers')
    
    return render_template('forms.html', title = 'Add Customer')
    

# ADD DISTRIBUTOR
@app.route('/distributors/add-distributor', methods=['POST', 'GET'])
def add_distributor():
    """Adds a new distributor to the database"""

    sql_connection = connect_to_database()

    # form data
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
    """Creates inventory for a newly added distributor"""

    name = request.args['name']
    sql_connection = connect_to_database()

    # get distributorID from newly created distributor
    get_dist = f"SELECT distributorID from distributors WHERE name='{name}'"
    dist = execute_query(sql_connection, get_dist).fetchall()
    dist_id = dist[0]['distributorID']


    payload = {}

    # initialize genres
    genres = ['country', 'blues', 'rock', 'pop', 'funk', 'hip-hop']

    # pick a random genre
    for i in range(1, 10):
        genre = random.choice(genres)
       
        # create API request url based on genre and page number    
        url = f"https://api.discogs.com/database/search?genre='{genre}'&page={i}&key=yAkaOKZIxeKFgRSyIXEY&secret=hbaRZHEfvIVguItMHliaGvliDAJVbBCw"
        response = requests.request("GET", url, data = payload)
        response = response.json()
        
        # use results to insert into distInventory table
        for j in range(0, 20):
            key = 'year'

            # make sure each album has a year and is from US (to avoid foreign chars)
            if key in response['results'][j] and response['results'][j]['country'] == 'US':
                title = response['results'][j]['title']

                # ensures title can be inserted in MySQL table
                title = title.replace('"', '')
                title = title.replace("'","")
                title = title.replace("*", "")
                title = title.encode('ascii', 'ignore').decode('ascii')

                # split title by delimeter to get artist and album title
                title = title.split('-')
                artist = title[0]
                name = title[1][1:]
                
                year = response['results'][j]['year']
                price = random.randint(350, 5000)/100
                quantity = randint(0, 50)
                img = response['results'][j]['cover_image']
                
                insert_inventory = f'INSERT INTO distInventory(distributorID, artist, name, year, price, quantity, img) \
                VALUES ({dist_id}, "{artist}", "{name}", "{year}", {price}, {quantity}, "{img}")'
                execute_insert = execute_query(sql_connection, insert_inventory)
    
    # after all records have been inserted, redirect to distributors page
    return redirect('/distributors')


# VIEW DISTRIBUTOR INVENTORY ROUTE
@app.route('/distributors/view-inventory', methods=['POST', 'GET'])
def view_dist_inventory():
    """Displays inventory for specified distributor"""

    # form data to get distributor name and ID
    if request.method == 'POST':
        dist_name = request.form['dist_name']
        dist_id = request.form['dist_id']
        sql_connection = connect_to_database()
        
        inventory_query = f"SELECT name, artist, year, price, quantity, img FROM distInventory WHERE distributorID={dist_id}"
        inventory = execute_query(sql_connection, inventory_query).fetchall()

        return render_template('views.html', inventory=inventory, dist_name=dist_name)


# PURCHASED ITEMS ROUTE
@app.route('/purchase-items', methods=['POST'])
def show_items():
    """Displays items on a customer purchase"""

    sql_connection = connect_to_database()
    
    # form data to retrieve purchaseID
    purch_id = int(request.form['purchaseID'])
    get_items = f"SELECT name, artist, year, price, img FROM records INNER JOIN \
        purchasedItems ON purchasedItems.productID = records.productID INNER JOIN purchases ON purchases.purchaseID = purchasedItems.purchaseID \
        WHERE purchases.purchaseID = {purch_id}"
    items_query = execute_query(sql_connection, get_items).fetchall()

    return render_template('views.html', purchaseItems=items_query)


# ADD PURCHASE ROUTE
@app.route('/purchases/add-purchase', defaults={'cust': None}, methods=['POST', 'GET'])
@app.route('/purchases/add-purchase/<cust>', methods=['POST', 'GET'])
def add_purchase(cust):
    """Begins  new purchase for a customer"""

    sql_connection = connect_to_database()
    
    records = 'SELECT r.productID, r.name, r.artist, r.year, r.price, r.img, r.quantity, d.name AS distributor FROM records r INNER JOIN distributors d ON r.distributorID=d.distributorID'
    records_query = execute_query(sql_connection, records).fetchall()
    return render_template('views.html', recordsPurch=records_query, title='recordsPurch', id=cust)

recordsPurchased = []

# After records have been selected for a purchase
@app.route('/purchases/add-purchase/final', defaults={'cust': None}, methods=['POST', 'GET', 'ADD'])
@app.route('/purchases/add-purchase/final/<cust>', methods=['POST', 'GET', 'ADD'])
def add_purchase_final(cust):
    """Creates a purchase"""

    sql_connection = connect_to_database()
    customerID = None
    if request.method == 'ADD':
        recordsPurchased.clear()
        data = request.get_json()

        # records selected for purchase
        recordArray = data['recordIDs']
        
        if 'id' in data:
            customerID = int(data['id'])
        recordArray = [int(i) for i in recordArray]
        
        if recordArray:
            for i in recordArray:
                recordsPurchased.append(i)
            if customerID is None:
                # return for javascript function
                return render_template('forms.html', title='Add Purchase')
            else:
                return render_template('forms.html', title='Add Purchase')

    
    if request.method == 'GET':
        if recordsPurchased:
            if cust is None:
                customers = "SELECT customerID, firstName, lastName FROM customers"
                customers_query = execute_query(sql_connection, customers).fetchall()
                return render_template('forms.html', title='Add Purchase', customers=customers_query) 
            else:
                customer = f"SELECT customerID, firstName, lastName FROM customers WHERE \
                    customerID = {int(cust)}"
                customer_query = execute_query(sql_connection, customer).fetchall()
                return render_template('forms.html', title='Add Purchase', customer=customer_query)
        else:
            return redirect('/purchases/add-purchase')
    

    if request.method == 'POST':
        if recordsPurchased:
            custID = int(request.form['customer'])
            purchaseDate = request.form['purchasedate']
            data = request.form['method']
            total = 0

            # gets record information and inserts into purchase
            for i in recordsPurchased:
                price_query = f"SELECT price FROM records WHERE records.productID = {i}"
                price_query_ex = execute_query(sql_connection, price_query).fetchall()
                total += price_query_ex[0]['price']
            insert_purchases = f"INSERT INTO purchases(customerID, purchaseDate, paymentMethod, totalPrice) VALUES ({custID}, \
                '{purchaseDate}', '{data}', {total})"
            purchases_query = execute_query(sql_connection, insert_purchases).fetchall()
            last_purchase_id = f"SELECT LAST_INSERT_ID()"
            last_purch_id_query = execute_query(sql_connection, last_purchase_id).fetchall()
            last_id = last_purch_id_query[0]['LAST_INSERT_ID()']
            for i in recordsPurchased:
                insert_purchasedItems = f"INSERT INTO purchasedItems(purchaseID, productID) VALUES ({last_id}, {i})"
                exe_purchasedItems = execute_query(sql_connection, insert_purchasedItems).fetchall()
                update_quant = f"UPDATE records SET quantity = quantity - 1 WHERE records.productID = {i}"
                update_quant_query = execute_query(sql_connection, update_quant).fetchall()

        recordsPurchased.clear()
        return redirect('/purchases')


# ADD RECORDS
@app.route('/records/add-record', methods=['POST', 'GET'])
def add_record():
    """Adds a record to the database"""

    sql_connection = connect_to_database()

    # form data for record info
    if request.method == 'POST':
        name = request.form['name']
        artist = request.form['artist']
        price = request.form['price']
        quantity = request.form['quantity']
        year = request.form['year']
        add_record = f"INSERT INTO records(name, artist, year, price, quantity) VALUES ('{name}', '{artist}', '{year}', '{price}', '{quantity}')"
        record_query = execute_query(sql_connection, add_record).fetchall()

        # redirect to records, after adding
        return redirect('/records')
    
    return render_template('forms.html', title = 'Add Record')


# ADD A NEW ORDER

# 1. SELECT DISTRIBUTOR
@app.route('/orders/add-order/select-distributor', methods=['POST', 'GET'])
def select_dist():
    """Select a distributor to order from"""

    sql_connection = connect_to_database()
    if request.method == 'GET':
        distributors = 'SELECT distributorID, name, street, city, state, zip, phone FROM distributors'
        distributors_query = execute_query(sql_connection, distributors).fetchall()
        
        return render_template('forms.html', title='Create Order', distributor_order=distributors_query)


# 2. SELECT ITEMS FOR ORDER
@app.route('/orders/add-order/create-order', methods=['GET', 'POST'])
def create_order():
    """Displays inventory for particular distributor to select items from"""

    sql_connection = connect_to_database()
    if request.method == 'POST':
        if request.form['distributor'] != None:
            dist_name = request.form['distributor']
            dist_inventory_query = f"SELECT inventoryID, distributorID, name, artist, year, price, quantity, img FROM distInventory WHERE distributorID=(SELECT distributorID FROM distributors WHERE name='{dist_name}')"
            dist_inventory = execute_query(sql_connection, dist_inventory_query).fetchall()

            return render_template('forms.html', dist_inventory=dist_inventory, dist_name=dist_name)

    
# 3. CONFIRM ORDER
@app.route('/orders/add-order/confirm-order', methods=['GET', 'POST'])
def confirm_order():
    """Order confirmation"""
    
    sql_connection = connect_to_database()

    # form data to add order
    if request.method == 'POST':
        orderData = request.get_json()
        dist_id = orderData['dist_id']
        filled = orderData['filled']
        total = orderData['total']
        order_query = f"INSERT INTO orders(distributorID, orderDate, orderFilled, orderTotal) VALUES ({dist_id}, curdate(), {filled}, {total})"
        execute_query(sql_connection, order_query)

        order_q = "SELECT last_insert_id()"
        order_id = execute_query(sql_connection, order_q).fetchall()
        order_id = order_id[0]['last_insert_id()']
        items = orderData['items']
        
        for i in range(len(items)):
            # adds items to orderedItems relationship table tied to last_insert_id()
            ordered_items_query = f"INSERT INTO orderedItems(orderID, inventoryID, quantity) VALUES ({order_id}, {items[i]['id']}, {items[i]['quantity']})"
            execute_query(sql_connection, ordered_items_query)

            # subtracts from distInventory
            update_dist_query = f"UPDATE distInventory SET quantity=quantity-{items[i]['quantity']} WHERE inventoryID={items[i]['id']}"
            execute_query(sql_connection, update_dist_query)

        return redirect('/orders')


# VIEW ITEMS ON ORDER
@app.route('/orders/view-order', methods=['GET', 'POST'])
def view_order():
    """Displays items on a particular order"""

    sql_connection = connect_to_database()

    # uses orderID to retrieve information from relationship table
    if request.method == 'POST':
        order_id = request.form['order_id']
        items_query = f"SELECT d.name, d.artist, d.price, d.img, o.quantity, o.orderID FROM distInventory d INNER JOIN orderedItems o ON d.inventoryID=o.inventoryID WHERE o.orderID={order_id}"
        ordered_items = execute_query(sql_connection, items_query).fetchall()
        orderID = ordered_items[0]['orderID']

        return render_template('views.html', ordered_items=ordered_items, orderID=orderID)


# ORDER FILLED
@app.route('/orders/fill-orders', methods=['POST', 'GET'])
def fill_orders():
    """Fills an order and adds ordered items to records in shop"""

    sql_connection = connect_to_database()
    data = request.get_json()

    if request.method == 'POST':
        orders = data['orders']
        records = []

        # loop through orders and gather information
        for i in range(len(orders)):
            
            order_info_query = f"SELECT d.inventoryID, d.distributorID, d.name, d.artist, d.price, d.year, d.img, (SELECT name from distributors WHERE distributorID={orders[i]['distributor_id']}) AS distributor, o.quantity FROM distInventory d \
            INNER JOIN orderedItems o ON d.inventoryID=o.inventoryID WHERE o.orderID={orders[i]['order_id']} "

            # set order filled to True
            order_filled = f"UPDATE orders SET orderFilled=True WHERE orderID={orders[i]['order_id']}"
            execute_query(sql_connection, order_filled)

            record_info = execute_query(sql_connection, order_info_query).fetchall()

            records.append(record_info)

        # for every record on the order insert it into database, if record already exists in database, update quantity
        for i in records:
            for j in i:
                add_records_query = f"INSERT INTO records (productID, price, name, artist, year, distributorID, img, quantity)\
                VALUES ({j['inventoryID']}, {j['price']}, '{j['name']}', '{j['artist']}', '{j['year']}', '{j['distributorID']}', '{j['img']}', {j['quantity']}) \
                ON DUPLICATE KEY UPDATE quantity=quantity+{j['quantity']}"

                execute_query(sql_connection, add_records_query)
    
        return redirect('/records')


# UPDATE ROUTE
# Handles updates for customers and distributors
@app.route('/update', methods=['POST'])
def update_customer():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        
        data = request.get_json()

        # Receives javascript xhr request and updates information for customers
        if data['pageType'] == 'Customers':
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

        # Receives javascript xhr request to update distributor information
        if data['pageType'] == 'Distributors':
            dist_id = data['id']
            name = data['name']
            street = data['street']
            city = data['city']
            state = data['state']
            zip_code = data['zip']
            phone = data['phone']
            dist_query = f"UPDATE distributors SET name='{name}', street='{street}', city='{city}', state='{state}', zip='{zip_code}', phone='{phone}' WHERE distributorID={dist_id}"
            execute_query(sql_connection, dist_query)
            return redirect('/distributors')