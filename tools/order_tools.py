from langchain_core.tools import tool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.repositories import OrderRepository

engine = create_engine("sqlite:///orders.db")
SessionLocal = sessionmaker(bind=engine)

@tool
def get_order_status(order_id: int) -> str:
    """Return the current status of a customer order given the order_id."""
    session = SessionLocal()
    repository = OrderRepository(session)
    order = repository.get_order_by_id(order_id)
    session.close()
    if order:
        return order.status
    return "Order not found"

@tool
def cancel_order(order_id: int) -> str:
    """Cancel a customer order given the order_id and return a success message."""
    session = SessionLocal()
    repository = OrderRepository(session)
    order = repository.update_order_status(order_id, "Cancelled")
    session.close()
    if order:
        return "Order cancelled successfully"
    return "Order not found"

@tool
def process_refund(order_id: int) -> str:
    """Process a refund for a customer order given the order_id and return a success message."""
    session = SessionLocal()
    repository = OrderRepository(session)
    order = repository.update_order_status(order_id, "Refunded")
    session.close()
    if order:
        return "Refund processed successfully"
    return "Order not found"