-- 
-- CUSTOMER PAGE
-- 

-- displays customer data in table 
SELECT firstName, lastName, city, state, zip, phone, email FROM customers;

-- deletes customer from customers table
DELETE FROM customers WHERE customerID = :delete button associated with customer row

-- updates customer information
UPDATE customers SET firstName = :firstName_input, lastName = :lastName_input, street = :street_input city = :city_input, state = :state_input, zip = :zip_input, phone = :phone_input, email = :email_input;

-- view customers purchases
SELECT date, paymentMethod, totalPrice FROM purchases WHERE customerID = :id associated with row

-- ADD CUSTOMER PAGE
-- adds a customer
INSERT INTO customers(firstName, lastName, street, city, state, zip, phone, email)
    VALUES (:firstName_input, :lastName_input, :street_input, :city_input, :state_dropdown, :zip_input, :phone_input, :email_input);


-- 
-- DISTRIBUTORS PAGE
-- 
-- displays distributor data
SELECT name, street, city, state, zip, phone FROM distributors;

-- deletes distributor from distributor table
DELETE FROM distributors WHERE distributorID = :delete button associated with row

-- updates distributor information
UPDATE distributors SET name = :name_input, street = :street_input, city = :city_input, state = :state_input, zip = :zip_input, phone = :phone_input

-- ADD DISTRIBUTOR PAGE
-- add a distributor
INSERT INTO distributors(name, street, city, state, zip, phone)
    VALUES (:name_input, :street_input, :city_input, :state_dropdown, :zip_input, :phone_input);


-- 
-- RECORDS PAGE
-- 
-- displays inventory of records
SELECT name, artist, year, price, quantity, distributor FROM records;

-- updates record information
UPDATE records SET name = :name_input. artist = :artist_input, year = :year_input, price = :price_input, quantity = :quantity_input, distributor = :distributor_input

-- ADD RECORD PAGE
-- add a record
INSERT INTO records(name, artist, year, price, quantity, distributor)
    VALUES (:name_input, :artist_input, :year_input, :price_input, :quantity_input, :distributor_input);



-- 
-- ORDERS PAGE
--
-- displays order info 
SELECT orderDate, orderFilled, distributor FROM orders;


-- updates whether an order is filled or not
UPDATE orders SET orderFilled = :filled_checkbox


-- ADD ORDER PAGE
INSERT INTO orders (distributorID, orderDate, orderFilled, distributor)
    VALUES (SELECT distributorID FROM distributors where name = :distributor_name_dropdown, orderDate, orderFilled, distributor)


-- 
-- PURCHASES PAGE
-- 
-- displays all purchases
SELECT date, paymentMethod, totalPrice FROM purchases

-- ADD PURCHASE PAGE
INSERT INTO purchases (customerID, paymentMethod, totalPrice)
    VALUES (SELECT customerID from customers WHERE firstName = :firstName_text_input AND lastName = :lastName_text_input AND phone = :phone_text_input)
    