import enum
from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class OrderStatus(str, enum.Enum):
  PENDING = "Pending"
  SHIPPED = "Shipped"
  CANCELLED = "Cancelled"
  REFUNDED = "Refunded"

  def __str__(self) -> str:
    return self.value


class Customer(Base):
  __tablename__ = "customers"

  customer_id = Column(Integer, primary_key=True)
  first_name = Column(String, nullable=False)
  last_name = Column(String, nullable=False)
  email = Column(String, nullable=False)
  join_date = Column(DateTime)
  date_of_birth = Column(DateTime)

  orders = relationship("Order", back_populates="customer")


class Product(Base):
  __tablename__ = "products"

  product_id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  category = Column(String)
  warranty_months = Column(Integer)
  price = Column(Float)

  orders = relationship("Order", back_populates="product")


class Order(Base):
  __tablename__ = "orders"

  # Explicit table-level check constraint for SQLite
  __table_args__ = (
      CheckConstraint(
          "status IN ('Pending', 'Shipped', 'Cancelled', 'Refunded')",
          name="ck_orders_status",
      ),
  )

  order_id = Column(Integer, primary_key=True)
  customer_id = Column(Integer, ForeignKey("customers.customer_id"))
  product_id = Column(Integer, ForeignKey("products.product_id"))
  status = Column(
      Enum(
          OrderStatus,
          native_enum=False,
          values_callable=lambda obj: [e.value for e in obj],
      ),
      nullable=False,
      default=OrderStatus.PENDING,
  )
  order_date = Column(DateTime)

  customer = relationship("Customer", back_populates="orders")
  product = relationship("Product", back_populates="orders")