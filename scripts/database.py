import sqlite3

sql_script = """
PRAGMA foreign_keys = ON;

CREATE TABLE Customers (
    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
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
    status TEXT CHECK(status IN ('Shipped', 'Pending', 'Cancelled')) NOT NULL,
    order_date DATE NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

INSERT INTO Customers (first_name, email, join_date) VALUES
('Alice', 'alice.smith@example.com', '2023-01-15'),
('Bob', 'bob.jones@example.com', '2023-02-10'),
('Charlie', 'charlie.brown@example.com', '2023-03-05'),
('Diana', 'diana.prince@example.com', '2023-04-20'),
('Evan', 'evan.davis@example.com', '2023-05-12'),
('Fiona', 'fiona.gallagher@example.com', '2023-06-18'),
('George', 'george.lucas@example.com', '2023-07-22'),
('Hannah', 'hannah.montana@example.com', '2023-08-30'),
('Ian', 'ian.wright@example.com', '2023-09-14'),
('Julia', 'julia.roberts@example.com', '2023-10-01'),
('Kevin', 'kevin.bacon@example.com', '2023-10-15'),
('Laura', 'laura.croft@example.com', '2023-11-05'),
('Mike', 'mike.wazowski@example.com', '2023-11-20'),
('Nina', 'nina.simone@example.com', '2023-12-01'),
('Oscar', 'oscar.isaac@example.com', '2023-12-15'),
('Paula', 'paula.abdul@example.com', '2024-01-10'),
('Quincy', 'quincy.jones@example.com', '2024-02-14'),
('Rachel', 'rachel.green@example.com', '2024-03-01'),
('Steve', 'steve.rogers@example.com', '2024-03-15'),
('Tina', 'tina.turner@example.com', '2024-04-10');

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
(1, 3, 'Shipped', '2024-05-01'),
(5, 7, 'Pending', '2024-05-02'),
(12, 1, 'Cancelled', '2024-05-03'),
(20, 10, 'Shipped', '2024-05-04'),
(2, 5, 'Shipped', '2024-05-05'),
(8, 2, 'Pending', '2024-05-06'),
(15, 8, 'Shipped', '2024-05-07'),
(3, 4, 'Shipped', '2024-05-08'),
(18, 9, 'Cancelled', '2024-05-09'),
(7, 6, 'Shipped', '2024-05-10'),
(4, 3, 'Pending', '2024-05-11'),
(11, 7, 'Shipped', '2024-05-12'),
(19, 1, 'Shipped', '2024-05-13'),
(6, 10, 'Pending', '2024-05-14'),
(14, 2, 'Shipped', '2024-05-15'),
(9, 5, 'Cancelled', '2024-05-16'),
(17, 8, 'Shipped', '2024-05-17'),
(13, 4, 'Shipped', '2024-05-18'),
(10, 9, 'Pending', '2024-05-19'),
(16, 6, 'Shipped', '2024-05-20'),
(1, 2, 'Shipped', '2024-05-21'),
(5, 10, 'Cancelled', '2024-05-22'),
(12, 5, 'Shipped', '2024-05-23'),
(20, 8, 'Pending', '2024-05-24'),
(2, 1, 'Shipped', '2024-05-25'),
(8, 7, 'Shipped', '2024-05-26'),
(15, 4, 'Cancelled', '2024-05-27'),
(3, 9, 'Shipped', '2024-05-28'),
(18, 6, 'Pending', '2024-05-29'),
(7, 3, 'Shipped', '2024-05-30');
"""

def initialize_database():
    connection = sqlite3.connect("orders.db")
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    initialize_database()