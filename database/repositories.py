from sqlalchemy.orm import Session
from database.models import Order, Customer

class OrderRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_order_by_id(self, order_id: int):
        return self.session.query(Order).filter(Order.order_id == order_id).first()

    def get_customer_by_email_dob(self, mail: str, date_of_birth: str):
        return self.session.query(Customer).filter(
            Customer.email == mail,
            Customer.date_of_birth == date_of_birth
        ).first()

    def update_order_status(self, order_id: int, new_status: str):
        order = self.get_order_by_id(order_id)
        if order:
            order.status = new_status
            self.session.commit()
            return order
        return None