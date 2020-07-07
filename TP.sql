drop schema TP;
CREATE SCHEMA TP
DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE TP;
SET NAMES utf8;

CREATE TABLE Customers (
	 name1 VARCHAR(30),
     passwd varchar(30),
     phone VARCHAR(30),
     email VARCHAR(30),
     address VARCHAR(30),
     customer_id INT NOT NULL,
     PRIMARY KEY (customer_id)
);
CREATE TABLE sellers (
	 sellers_id INT NOT NULL,
     name1 VARCHAR(30),
     phone VARCHAR(30),
     email VARCHAR(30),
     passwd varchar(30),
     PRIMARY KEY (sellers_id)
);
CREATE TABLE Delivery (
	 del_id INT NOT NULL,
     name1 VARCHAR(30),
     email VARCHAR(30),
     passwd varchar(30),
     area VARCHAR(30),
     phone varchar(30),
     available INT,
     stock INT,
     PRIMARY KEY (del_id)
);
CREATE TABLE Stores (
	 store_id INT NOT NULL,
     address varchar(30),
     sname VARCHAR(30),
     phone varchar(30),
     seller_id INT,
     open_time varchar(30),
     close_time varchar(30),
     type1 varchar(30),
     PRIMARY KEY (store_id),
     FOREIGN KEY(seller_id)   REFERENCES   sellers(sellers_id)
);
CREATE TABLE Menu (
	 menu_id INT NOT NULL,
     name1 VARCHAR(30),
     price INT,
     event1 float,
     store_id INT,
     PRIMARY KEY (menu_id),
     FOREIGN KEY(store_id)   REFERENCES   stores(store_id)
);
CREATE TABLE Payment (
	 payment_id INT NOT NULL,
     customer_id INT NOT NULL,
     pay_num BIGINT,
     pay_type INT,
     PRIMARY KEY (payment_id, customer_id),
     FOREIGN KEY(customer_id)   REFERENCES   customers(customer_id)
);
CREATE TABLE Orders (
	 order_id INT NOT NULL,
     order_time timestamp,
     delivery_done INT,
     del_id INT,
     payment_id INT,
     customer_id INT,
     store_id INT,
     PRIMARY KEY (order_id),
     FOREIGN KEY(del_id)   REFERENCES   delivery(del_id),
     FOREIGN KEY(payment_id)   REFERENCES   payment(payment_id),
     FOREIGN KEY(customer_id)   REFERENCES   customers(customer_id),
     FOREIGN KEY(store_id)   REFERENCES   stores(store_id)
);
CREATE TABLE Orderdetail (
      detail_order_id INT NOT NULL,
      order_id INT NOT NULL,
      menu_id INT,
      quantity INT,
      PRIMARY KEY (detail_order_id, order_id),
      FOREIGN KEY(order_id)   REFERENCES   orders(order_id) on delete cascade,
      FOREIGN KEY(menu_id)   REFERENCES   menu(menu_id) ON DELETE SET NULL
);

LOAD DATA LOCAL INFILE "d:\customer.csv" INTO table tp.customers FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE "d:\seller.csv" INTO table tp.sellers FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE "d:\menu.csv" INTO table tp.menu FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE "d:\pay.csv" INTO table tp.payment FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE "d:\store.csv" INTO table tp.stores FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
LOAD DATA LOCAL INFILE "d:\delivery.csv" INTO table tp.delivery FIELDS TERMINATED BY ',' LINES TERMINATED BY '\r\n';
