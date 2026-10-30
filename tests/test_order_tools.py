import pytest
from tools.order_tools import get_order_status, cancel_order, process_refund
from tools.auth_tool import authenticate_user_by_email_and_dob

def test_get_order_status_found():
    result = get_order_status.invoke({"order_id": 1})
    assert result == "Shipped"

def test_get_order_status_not_found():
    result = get_order_status.invoke({"order_id": 99999})
    assert result == "Order not found"

def test_cancel_order():
    result = cancel_order.invoke({"order_id": 2})
    assert result == "Order cancelled successfully"
    status = get_order_status.invoke({"order_id": 2})
    assert status == "Cancelled"

def test_process_refund():
    result = process_refund.invoke({"order_id": 4})
    assert result == "Refund processed successfully"
    status = get_order_status.invoke({"order_id": 4})
    assert status == "Refunded"

def test_authenticate_user_success():
    result = authenticate_user_by_email_and_dob.invoke({
        "mail": "evelyn.taylor@example.com",
        "date_of_birth": "1987-03-15"
    })
    assert result == "1"

def test_authenticate_user_not_found():
    result = authenticate_user_by_email_and_dob.invoke({
        "mail": "unknown@example.com",
        "date_of_birth": "1990-01-01"
    })
    assert result == "Customer not found"
