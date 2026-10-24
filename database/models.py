from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    join_date = Column(DateTime)
    
    orders = relationship("Order", back_populates="customer")

class Product(Base):
    __tablename__ = 'products'
    
    product_id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    category = Column(String)
    warranty_months = Column(Integer)
    price = Column(Float)
    
    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = 'orders'
    
    order_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'))
    product_id = Column(Integer, ForeignKey('products.product_id'))
    status = Column(String, nullable=False)
    order_date = Column(DateTime)
    
    customer = relationship("Customer", back_populates="orders")
    product = relationship("Product", back_populates="orders")