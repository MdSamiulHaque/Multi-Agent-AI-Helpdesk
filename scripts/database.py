import sqlite3

sql_script = """
PRAGMA foreign_keys = OFF;

DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Customers;

PRAGMA foreign_keys = ON;

CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    date_of_birth DATE NOT NULL,
    email TEXT NOT NULL,
    join_date DATE NOT NULL
);

CREATE TABLE Products (
    product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    warranty_months INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    status TEXT CHECK(status IN ('Shipped', 'Pending', 'Cancelled', 'Refunded')) NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Customers (first_name, last_name, date_of_birth, email, join_date) VALUES
('Evelyn', 'Taylor', '1987-03-15', 'evelyn.taylor@example.com', '2026-06-01'),
('Daniel', 'Moore', '1992-08-22', 'daniel.moore@example.com', '2026-06-04'),
('Ava', 'Jackson', '1999-11-10', 'ava.jackson@example.com', '2026-06-09'),
('Matthew', 'Martin', '1984-01-05', 'matthew.martin@example.com', '2026-06-12'),
('Isabella', 'Lee', '1996-05-18', 'isabella.lee@example.com', '2026-06-18'),
('Jackson', 'Perez', '1991-09-27', 'jackson.perez@example.com', '2026-06-25'),
('Abigail', 'Thompson', '1989-12-14', 'abigail.thompson@example.com', '2026-07-02'),
('Sebastian', 'White', '2002-04-03', 'sebastian.white@example.com', '2026-07-07'),
('Emily', 'Harris', '1993-07-19', 'emily.harris@example.com', '2026-07-15'),
('Jack', 'Sanchez', '1986-10-30', 'jack.sanchez@example.com', '2026-07-21'),
('Ella', 'Clark', '1998-02-11', 'ella.clark@example.com', '2026-07-29'),
('Aiden', 'Ramirez', '1990-06-24', 'aiden.ramirez@example.com', '2026-08-03'),
('Chloe', 'Lewis', '1995-12-01', 'chloe.lewis@example.com', '2026-08-11'),
('Samuel', 'Robinson', '1983-09-08', 'samuel.robinson@example.com', '2026-08-18'),
('Grace', 'Walker', '2001-01-20', 'grace.walker@example.com', '2026-08-26'),
('David', 'Young', '1994-03-31', 'david.young@example.com', '2026-09-02'),
('Zoey', 'Allen', '1988-11-17', 'zoey.allen@example.com', '2026-09-09'),
('Carter', 'King', '1997-08-13', 'carter.king@example.com', '2026-09-14'),
('Penelope', 'Wright', '1991-04-29', 'penelope.wright@example.com', '2026-09-22'),
('Wyatt', 'Scott', '1985-06-07', 'wyatt.scott@example.com', '2026-09-28'),
('Riley', 'Torres', '2000-10-15', 'riley.torres@example.com', '2026-10-04'),
('Owen', 'Nguyen', '1993-05-26', 'owen.nguyen@example.com', '2026-10-10'),
('Layla', 'Hill', '1996-01-09', 'layla.hill@example.com', '2026-10-16'),
('Julian', 'Flores', '1989-07-03', 'julian.flores@example.com', '2026-10-21'),
('Nora', 'Green', '1992-02-18', 'nora.green@example.com', '2026-10-27');

INSERT INTO Products (name, category, warranty_months, price) VALUES
('Quantum Processor 9', 'Electronics', 1, 499.99),
('Holo-Projector Lite', 'Electronics', 1, 299.50),
('Neural Link Headset', 'Electronics', 1, 150.00),
('Plasma Battery Pack', 'Electronics', 1, 45.99),
('Aether Router', 'Electronics', 1, 120.25),
('Nano-Sensors (100pk)', 'Electronics', 1, 89.99),
('Hyper-Drive SSD 2TB', 'Electronics', 1, 199.99),
('Sonic Screwdriver V2', 'Electronics', 1, 340.00),
('Gravity Glove', 'Electronics', 1, 850.00),
('Smart Lens', 'Electronics', 1, 199.00);

INSERT INTO Orders (customer_id, product_id, status, order_date) VALUES
(1, 3, 'Shipped', '2026-05-01'),
(5, 7, 'Pending', '2026-05-02'),
(12, 1, 'Cancelled', '2026-05-03'),
(20, 10, 'Shipped', '2026-05-04'),
(2, 5, 'Shipped', '2026-05-05'),
(8, 2, 'Pending', '2026-05-06'),
(15, 8, 'Shipped', '2026-05-07'),
(3, 4, 'Shipped', '2026-05-08'),
(18, 9, 'Cancelled', '2026-05-09'),
(7, 6, 'Shipped', '2026-05-10'),
(4, 3, 'Pending', '2026-05-11'),
(11, 7, 'Shipped', '2026-05-12'),
(19, 1, 'Shipped', '2026-05-13'),
(6, 10, 'Pending', '2026-05-14'),
(14, 2, 'Shipped', '2026-05-15'),
(9, 5, 'Cancelled', '2026-05-16'),
(17, 8, 'Shipped', '2026-05-17'),
(13, 4, 'Shipped', '2026-05-18'),
(10, 9, 'Pending', '2026-05-19'),
(16, 6, 'Shipped', '2026-05-20'),
(1, 2, 'Shipped', '2026-05-21'),
(5, 10, 'Cancelled', '2026-05-22'),
(12, 5, 'Shipped', '2026-05-23'),
(20, 8, 'Pending', '2026-05-24'),
(2, 1, 'Shipped', '2026-05-25'),
(8, 7, 'Shipped', '2026-05-26'),
(15, 4, 'Cancelled', '2026-05-27'),
(3, 9, 'Shipped', '2026-05-28'),
(18, 6, 'Pending', '2026-05-29'),
(7, 3, 'Shipped', '2026-10-29');
"""

def initialize_database():
    connection = sqlite3.connect("orders.db")
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()