from datetime import datetime
from langchain_core.tools import tool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.repositories import OrderRepository

engine = create_engine("sqlite:///orders.db")
SessionLocal = sessionmaker(bind=engine)

@tool
def check_refund_eligibility(order_id: int) -> str:
    """Check if an order meets the 30-day policy and refund threshold guardrails."""
    session = SessionLocal()
    repository = OrderRepository(session)
    order = repository.get_order_by_id(order_id)
    
    if not order:
        session.close()
        return "Order not found"
        
    if order.status == "Refunded":
        session.close()
        return "Ineligible: Order is already refunded"
        
    days_since_order = (datetime.now() - order.order_date).days
    
    if days_since_order > 30:
        session.close()
        return "Escalate: Order exceeds 30-day return window"
        
    if order.product and order.product.price > 500.0:
        session.close()
        return "Escalate: Refund amount exceeds automated threshold"
        
    session.close()
    return "Eligible for automated refund"