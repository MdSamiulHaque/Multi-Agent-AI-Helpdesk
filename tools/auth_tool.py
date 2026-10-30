from langchain_core.tools import tool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.repositories import OrderRepository

engine = create_engine("sqlite:///orders.db")
SessionLocal = sessionmaker(bind=engine)

@tool
def authenticate_user_by_email_and_dob(mail: str, date_of_birth: str) -> str:
    """Return the customer id if the given email and date of birth are correct."""
    session = SessionLocal()
    repository = OrderRepository(session)
    customer = repository.get_customer_by_email_dob(mail, date_of_birth)
    session.close()
    if customer:
        return str(customer.customer_id)
    return "Customer not found"