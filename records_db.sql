DROP TABLE IF EXISTS `customers`;
CREATE TABLE `customers` (
  `customerID` int NOT NULL AUTO_INCREMENT,
  `firstName` varchar(255) NOT NULL,
  `lastName` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` varchar(5) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `email` varchar(40) NOT NULL,
  PRIMARY KEY (`customerID`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `purchases`;
CREATE TABLE `purchases` (
  `purchaseID` int NOT NULL AUTO_INCREMENT,
  `customerID` int,
  `purchaseDate` DATE NOT NULL,
  `paymentMethod` varchar(255) NOT NULL,
  `totalPrice` DEC(65, 2) NOT NULL,
  PRIMARY KEY (`purchaseID`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `customers`(`customerID`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `records`;
CREATE TABLE `records` (
  `productID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `artist` varchar(255) NOT NULL,
  `year` YEAR NOT NULL,
  `price` DEC(5, 2) NOT NULL,
  `quantity` int NOT NULL,
  `distributor` varchar(255),
  PRIMARY KEY (`productID`)
) ENGINE=InnoDB;



DROP TABLE IF EXISTS `distributors`;
CREATE TABLE `distributors` (
  `distributorID` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `street` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `state` varchar(255) NOT NULL,
  `zip` varchar(5) NOT NULL,
  `phone` varchar(10) NOT NULL,
  PRIMARY KEY (`distributorID`)
) ENGINE=InnoDB;

DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `orderID` int NOT NULL AUTO_INCREMENT,
  `distributorID` int,
  `orderDate` DATE NOT NULL,
  `orderFilled` BOOLEAN NOT NULL,
  `distributor` varchar(255),
  PRIMARY KEY (`orderID`),
  CONSTRAINT `distributor_ibfk_1` FOREIGN KEY (`distributorID`) REFERENCES `distributors`(`distributorID`)
) ENGINE=InnoDB;

-- RELATIONSHIP TABLES

DROP TABLE IF EXISTS `purchasedItems`;
CREATE TABLE `purchasedItems` (
    `purchasedItemID` int NOT NULL AUTO_INCREMENT,
    `purchaseID` int,
    `productID` int,
    PRIMARY KEY (`purchasedItemID`),
    CONSTRAINT `purchase_ibfk_1` FOREIGN KEY (`purchaseID`) REFERENCES `purchases` (`purchaseID`),
    CONSTRAINT `product_ibfk_2` FOREIGN KEY (`productID`) REFERENCES `records` (`productID`)
) ENGINE=InnoDB;


DROP TABLE IF EXISTS `orderedItems`;
CREATE TABLE `orderedItems` (
    `orderedItemID` int NOT NULL AUTO_INCREMENT,
    `orderID` int,
    `productID` int,
    PRIMARY KEY (`orderedItemID`),
    CONSTRAINT `order_ibfk_1` FOREIGN KEY (`orderID`) REFERENCES `orders` (`orderID`),
    CONSTRAINT `product_ibfk_3` FOREIGN KEY (`productID`) REFERENCES `records` (`productID`)
) ENGINE=InnoDB;



INSERT INTO customers (firstName, lastName, street, city, state, zip, phone, email) VALUES
    ('Joe', 'Smith', 'H Street', 'Seattle', 'WA', '78654', '345-678-9043', 'joesmith@gmail.com'),
    ('Sally', 'Anderson', 'Fake Avenue', 'Los Angeles', 'CA', '45896', '231-781-1209', 'sally_anderson@yahoo.com'),
    ('John', 'Lee', '456 Street', 'Dallas', 'TX', '89412', '456-9016-5673', 'john_lee@outlook.com')
    ;


INSERT INTO purchases (customerID, purchaseDate, paymentMethod, totalPrice) VALUES
    ((SELECT customerID FROM customers WHERE firstName = 'Joe' AND lastName = 'Smith'), '2019-07-14', 'Cash', 23.87),
    ((SELECT customerID FROM customers WHERE firstName = 'Sally' AND lastName = 'Anderson'),'2018-05-24', 'Card', 31.45),
    ((SELECT customerID FROM customers WHERE firstName = 'Joe' AND lastName = 'Smith'), '2018-05-27', 'Card', 65.17)
    ;

INSERT INTO records (name, artist, year, price, quantity, distributor) VALUES
    ('Let it Be', 'The Beatles', '1970', 15.00, 1, 'Records R Us'),
    ('Beggars Banquet', 'The Rolling Stones', '1968', 12.50, 2, 'Records R Us'),
    ('Electric Ladyland', 'Jimi Hendrix', '1968', 20.00, 1, 'Records R Us')
    ;


INSERT INTO distributors (name, street, city, state, zip, phone) VALUES
    ('Records R Us', '123 Vinyl Ave', 'San Diego', 'CA', '98054', '231-987-4537'),
    ('Vinyl Warehouse', '456 Distribution St', 'Boise', 'ID', '72341', '560-678-9014'),
    ('House of Vinyl', '123 Utah Steet', 'Salt Lake City', 'UT', '12908', '451-671-5612')
    ;

INSERT INTO orders (distributorID, orderDate, orderFilled, distributor) VALUES
    ((SELECT distributorID from distributors where name = 'House of Vinyl'), '2020-06-15', true, 'House of Vinyl'),
    ((SELECT distributorID from distributors where name = 'House of Vinyl'), '2019-01-06', true, 'Vinyl Warehouse'),
    ((SELECT distributorID from distributors where name = 'House of Vinyl'), '2018-02-18', true, 'Records R Us')
    ;


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
    