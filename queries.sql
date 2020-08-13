-- 
-- SELECT QUERIES
-- 

-- selects all customer information
SELECT customerID, firstName, lastName, street, city, state, zip, phone, email FROM customers

-- selects all distributor information
SELECT distributorID, name, street, city, state, zip, phone FROM distributors

-- selects distributor based on name (used for search bar)
SELECT name, street, city, state, zip, phone from distributors WHERE name='{name}'

-- selects distributor based on city (used for search bar)
SELECT name, street, city, state, zip, phone from distributors WHERE city='{city}'

-- selects all record information for every record (even if record has no distribiutor)
SELECT r.name, r.artist, r.year, r.price, r.img, r.quantity, d.name AS distributor FROM records r LEFT JOIN distributors d ON r.distributorID=d.distributorID

-- selects all purchases and purchase info (even if there is no customer associated with purchase)
SELECT purchases.purchaseID, purchases.purchaseDate, purchases.paymentMethod, purchases.totalPrice, \
        customers.firstName, customers.lastName FROM purchases LEFT JOIN customers ON customers.customerID=purchases.customerID

-- selects all orders an order information
SELECT o.orderID, o.orderDate, o.distributorID, o.orderFilled, o.orderTotal, d.name AS distributor FROM orders o \
        INNER JOIN distributors d ON o.distributorID=d.distributorID ORDER BY orderID desc

-- selects purchase based on customer ID
SELECT purchaseID, purchaseDate, paymentMethod, totalPrice FROM purchases INNER JOIN customers ON customers.customerID = '+ id +' AND purchases.customerID = '+id'

-- selects customer name based on customer ID
SELECT firstName, lastName FROM customers WHERE customers.customerID = '+ id'

-- selects distributor name
SELECT distributorID from distributors WHERE name='{name}'

-- selects distributor inventory based on distributorID
SELECT name, artist, year, price, quantity, img FROM distInventory WHERE distributorID={dist_id}

-- selects purchased items based on purchase ID
SELECT name, artist, year, price, img FROM records INNER JOIN \
        purchasedItems ON purchasedItems.productID = records.productID INNER JOIN purchases ON purchases.purchaseID = purchasedItems.purchaseID \
        WHERE purchases.purchaseID = {purch_id}

-- selects record information to view under items purchased
SELECT r.productID, r.name, r.artist, r.year, r.price, r.img, r.quantity, d.name AS distributor FROM records r INNER JOIN distributors d ON r.distributorID=d.distributorID

-- selects customer ID and first name
SELECT customerID, firstName, lastName FROM customers

-- selects customer id, firstname and lastname based on customer id (used for purchase info)
SELECT customerID, firstName, lastName FROM customers WHERE \
                    customerID = {int(cust)}

-- selects distributor info (to be used when beginning an order)
SELECT distributorID, name, street, city, state, zip, phone FROM distributors

-- selects inventory based on distributor ID (to be used when creating an order)
SELECT inventoryID, distributorID, name, artist, year, price, quantity, img FROM distInventory WHERE distributorID=(SELECT distributorID FROM distributors WHERE name='{dist_name}'

-- selects ordered item information based on order ID
SELECT d.name, d.artist, d.price, d.img, o.quantity, o.orderID FROM distInventory d INNER JOIN orderedItems o ON d.inventoryID=o.inventoryID WHERE o.orderID={order_id}

-- selects ordered item information from each individual order, to be used in a loop before finalizing order
SELECT d.inventoryID, d.distributorID, d.name, d.artist, d.price, d.year, d.img, (SELECT name from distributors WHERE distributorID={orders[i]['distributor_id']}) AS distributor, o.quantity FROM distInventory d \
            INNER JOIN orderedItems o ON d.inventoryID=o.inventoryID WHERE o.orderID={orders[i]['order_id']} 


-- 
-- INSERT QUERIES
-- 

-- adds a customer
INSERT INTO customers(firstName, lastName, street, city, state, zip, email, phone) VALUES ('{firstName}', \
        '{lastName}', '{street}', '{city}', '{state}', {zip_code}, '{email}', '{phone}')

-- adds a distributor
INSERT INTO distributors(name, street, city, state, zip, phone) VALUES ('{name}', '{street}', '{city}', '{state}', '{zip_code}', '{phone}')

-- creates distInventory (used in a loop)
INSERT INTO distInventory(distributorID, artist, name, year, price, quantity, img) \
                VALUES ({dist_id}, "{artist}", "{name}", "{year}", {price}, {quantity}, "{img}")

-- adds a purchase
INSERT INTO purchases(customerID, purchaseDate, paymentMethod, totalPrice) VALUES ({custID}, \
                '{purchaseDate}', '{data}', {total})

-- adds a record that does not come from a distributor
INSERT INTO records(name, artist, year, price, quantity) VALUES ('{name}', '{artist}', '{year}', '{price}', '{quantity}')

-- adds an order
INSERT INTO orders(distributorID, orderDate, orderFilled, orderTotal) VALUES ({dist_id}, curdate(), {filled}, {total})

-- inserts items from order into relationship table (orderedItems)
INSERT INTO orderedItems(orderID, inventoryID, quantity) VALUES ({order_id}, {items[i]['id']}, {items[i]['quantity']})

-- adds records to records from orders beign filled
INSERT INTO records (productID, price, name, artist, year, distributorID, img, quantity)\
                VALUES ({j['inventoryID']}, {j['price']}, '{j['name']}', '{j['artist']}', '{j['year']}', '{j['distributorID']}', '{j['img']}', {j['quantity']}) \
                ON DUPLICATE KEY UPDATE quantity=quantity+{j['quantity']}

-- inserts items from purchase into relationship table (purchasedItems)
INSERT INTO purchasedItems(purchaseID, productID) VALUES ({last_id}, {i})


-- 
-- UPDATE QUERIES
-- 

-- updates record quantity when a record is purchased
UPDATE records SET quantity = quantity - 1 WHERE records.productID = {i}

-- updates distInventory quantity when a record is ordered
UPDATE distInventory SET quantity=quantity-{items[i]['quantity']} WHERE inventoryID={items[i]['id']}

-- sets an order to filled
UPDATE orders SET orderFilled=True WHERE orderID={orders[i]['order_id']}

-- updates records quantity when an order is filled (used as part of insert query above)
UPDATE quantity=quantity+{j['quantity']}

-- updates customer information
UPDATE customers SET firstName='{firstName}', lastName='{lastName}', street='{street}', city='{city}', state='{state}', zip='{zip_code}', phone='{phone}', email='{email}' WHERE customerID={cust_id}


-- updates distributor information
UPDATE distributors SET name='{name}', street='{street}', city='{city}', state='{state}', zip='{zip_code}', phone='{phone}' WHERE distributorID={dist_id}


-- 
-- DELETE QUERY
-- 

-- deletes a customer
DELETE FROM customers WHERE customerID={customerID}