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
        print(customers_query)
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

        if data['pageType'] == 'Distributors':
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
        records = 'SELECT productID, name, artist, year, price, quantity, distributor FROM records'
        records_query = execute_query(sql_connection, records).fetchall()
        return render_template('views.html', records=records_query, title='Records')



# PURCHASES
@app.route('/purchases', methods=['POST', 'GET'])
def view_purchases():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        purchases = 'SELECT purchases.purchaseID, purchases.purchaseDate, purchases.paymentMethod, purchases.totalPrice, \
        customers.firstName, customers.lastName FROM purchases INNER JOIN customers ON customers.customerID = purchases.customerID'
        purchases_query = execute_query(sql_connection, purchases).fetchall()
        return render_template('views.html', purchases=purchases_query, title='Purchases')



# ORDERS
@app.route('/orders', methods=['POST', 'GET'])
def view_orders():
    sql_connection = connect_to_database()
    if request.method == 'GET':
        orders_query = "SELECT orderID, orderDate, distributor, distributorID, orderFilled, orderTotal FROM orders ORDER BY orderID desc" 
        orders = execute_query(sql_connection, orders_query).fetchall()
        return render_template('views.html', orders=orders, title='Orders')


# Use this or repurpose existing Purchases page for individual customer puchase SELECT
@app.route('/custpurchases/<var>', methods=['GET'])
def view_cust_purchases(var):
    id = var
    sql_connection = connect_to_database()
    purchases = 'SELECT purchaseID, purchaseDate, paymentMethod, totalPrice FROM purchases INNER JOIN customers ON customers.customerID = '+ id +' AND purchases.customerID = '+id
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
            key2 = 'results'
            if key in response['results'][j] and response['results'][j]['country'] == 'US':
                title = response['results'][j]['title']
                title = title.replace('"', '')
                title = title.replace("'","")
                title = title.encode('ascii', 'ignore').decode('ascii')
                title = title.split('-')
                artist = title[0]
                name = title[1][1:]
                
                year = response['results'][j]['year']
                price = random.randint(350, 5000)/100
                print(price)
                quantity = randint(0, 50)
                img = response['results'][j]['cover_image']
                
                insert_inventory = f'INSERT INTO distInventory(distributorID, artist, name, year, price, quantity, img) VALUES ({dist_id}, "{artist}", "{name}", "{year}", {price}, {quantity}, "{img}")'
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
        
        inventory_query = f"SELECT name, artist, year, price, quantity, img FROM distInventory WHERE distributorID={dist_id}"
        inventory = execute_query(sql_connection, inventory_query).fetchall()
        

        return render_template('views.html', inventory=inventory, dist_name=dist_name)



#SHOW ITEMS ON A PURCHASE
@app.route('/purchaseItems', methods=['POST'])
def show_items():
    sql_connection = connect_to_database()
    purch_id = int(request.form['purchaseID'])
    get_items = f"SELECT name, artist, year, price, distributor FROM records INNER JOIN \
        purchasedItems ON purchasedItems.productID = records.productID INNER JOIN purchases ON purchases.purchaseID = purchasedItems.purchaseID \
        WHERE purchases.purchaseID = {purch_id}"
    items_query = execute_query(sql_connection, get_items).fetchall()
    return render_template('views.html', purchaseItems=items_query)

# ADD PURCHASE
@app.route('/purchases/add-purchase', defaults={'cust': None}, methods=['POST', 'GET'])
@app.route('/purchases/add-purchase/<cust>', methods=['POST', 'GET'])
def add_purchase(cust):
    sql_connection = connect_to_database()
    # if request.method == 'POST':
    records = 'SELECT productID, name, artist, year, price, quantity, distributor FROM records'
    records_query = execute_query(sql_connection, records).fetchall()
    return render_template('views.html', recordsPurch=records_query, title='recordsPurch', id=cust)

recordsPurchased = []

# after records have been selected for a purchase
@app.route('/purchases/add-purchase/final', defaults={'cust': None}, methods=['POST', 'GET', 'ADD'])
@app.route('/purchases/add-purchase/final/<cust>', methods=['POST', 'GET', 'ADD'])
def add_purchase_final(cust):
    sql_connection = connect_to_database()
    customerID = None
    if request.method == 'ADD':
        recordsPurchased.clear()
        data = request.get_json()
        recordArray = data['recordIDs']
        if 'id' in data:
            customerID = int(data['id'])
        recordArray = [int(i) for i in recordArray]
        if recordArray:
            for i in recordArray:
                recordsPurchased.append(i)
            if customerID is None:
                # this return is for javascript function
                return render_template('forms.html', title='Add Purchase')
            else:
                # customer_query = f'SELECT customerID, firstName, lastName FROM customers \
                # WHERE customerID = {customerID}'
                # get_customers = execute_query(sql_connection, customer_query).fetchall()
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
            print(request.form['customer'])
            custID = int(request.form['customer'])
            purchaseDate = request.form['purchasedate']
            data = request.form['method']
            print(type(custID), type(purchaseDate), type(data))
            total = 0
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
        print(request.form)
        dist_name = request.form['distributor']
        print(dist_name)
        dist_inventory_query = f"SELECT inventoryID, distributorID, name, artist, year, price, quantity, img FROM distInventory WHERE distributorID=(SELECT distributorID FROM distributors WHERE name='{dist_name}')"
        dist_inventory = execute_query(sql_connection, dist_inventory_query).fetchall()
        return render_template('forms.html', dist_inventory=dist_inventory, dist_name=dist_name)

# CONFIRM ORDER
@app.route('/orders/add-order/confirm-order', methods=['GET', 'POST'])
def confirm_order():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        orderData = request.get_json()
        print(orderData)
        dist_id = orderData['dist_id']
        filled = orderData['filled']
        total = orderData['total']
        order_query = f"INSERT INTO orders(distributorID, orderDate, orderFilled, distributor, orderTotal) VALUES ({dist_id}, curdate(), {filled}, (SELECT name from distributors WHERE distributorID={dist_id}), {total})"
        execute_query(sql_connection, order_query)

        order_q = "SELECT last_insert_id()"
        order_id = execute_query(sql_connection, order_q).fetchall()
        order_id = order_id[0]['last_insert_id()']
        items = orderData['items']
        print(items)


        # SUBTRACT FROM INVENTORY 

        for i in range(len(items)):
            ordered_items_query = f"INSERT INTO orderedItems(orderID, inventoryID, quantity) VALUES ({order_id}, {items[i]['id']}, {items[i]['quantity']})"
            execute_query(sql_connection, ordered_items_query)

            update_dist_query = f"UPDATE distInventory SET quantity=quantity-{items[i]['quantity']} WHERE inventoryID={items[i]['id']}"
            execute_query(sql_connection, update_dist_query)

        return redirect('/orders')

# VIEW ORDER
@app.route('/orders/view-order', methods=['GET', 'POST'])
def view_order():
    sql_connection = connect_to_database()
    if request.method == 'POST':
        order_id = request.form['order_id']

        items_query = f"SELECT d.name, d.artist, d.price, d.img, o.quantity FROM distInventory d INNER JOIN orderedItems o ON d.inventoryID=o.inventoryID WHERE o.orderID={order_id}"
        ordered_items = execute_query(sql_connection, items_query).fetchall()

        print(ordered_items)

        return render_template('views.html', ordered_items=ordered_items)



# ORDER FILLED
@app.route('/orders/fill-orders', methods=['POST', 'GET'])
def fill_orders():
    sql_connection = connect_to_database()
    data = request.get_json()
    if request.method == 'POST':
        orders = data['orders']
        records = []
        print(orders)
        for i in range(len(orders)):
            
            order_info_query = f"SELECT d.inventoryID, d.name, d.artist, d.price, d.year, (SELECT name from distributors WHERE distributorID={orders[i]['distributor_id']}) AS distributor, o.quantity FROM distInventory d \
            INNER JOIN orderedItems o ON d.inventoryID=o.inventoryID WHERE o.orderID={orders[i]['order_id']} "

            # order_filled = f"UPDATE orders SET orderFilled=True WHERE orderID={orders[i]['order_id']}"
            # execute_query(sql_connection, order_filled)

            record_info = execute_query(sql_connection, order_info_query).fetchall()

            records += [record_info]

        print("-----------------TEST---------------------")
        for i in range(len(records)):
            print(records[i])
            add_records_query = f"INSERT INTO records (productID, price, name, artist, year, distributor, quantity)\
             VALUES ({records[i]['inventoryID']}, {records[i]['price']}, '{records[i]['name']}', \
            '{records[i]['artist']}', '{records[i]['year']}', '{records[i]['distributor']}', {records[i]['quantity']}) \
            ON DUPLICATE KEY UPDATE SET quantity=quantity+{records[i]['quantity']}"

            execute_query(sql_connection, add_records_query)

            
    
        return redirect('/records')

