from datetime import datetime, timedelta
from delivery import get_orders_after_date, get_order
from typing import List, Dict, Any

# Define SLA Parameters (Assumed SLA: 48 hours from order date)
SLA_HOURS = 48*7000

def parse_order_time(order: dict) -> datetime:
    """
    Function to safely parse the order's purchase date into a datetime object.
    """
    purchase_date = order.get('PurchaseDate')
  
    
    if purchase_date and isinstance(purchase_date, str):
        return datetime.strptime(purchase_date, "%Y-%m-%d %H:%M:%S")
    elif isinstance(purchase_date, datetime):
        return purchase_date
    else:
        raise ValueError(f"Invalid purchase date type: {type(purchase_date)}")

def check_order_sla(order: dict) -> Dict[str, Any]:
    """
    Function to check whether an order is within the SLA (48 hours).
    Returns a dictionary with the order SLA status and time difference.
    """
    current_time = datetime.now()
    
    # Ensure the order exists and has data
    order_data = order
    # print("*****************")
    # print(order_data)
    # print("*****************")
    # print(order)
    if not order_data:
        return {"order_id": None, "sla_status": "Order data is missing or invalid", "time_diff": None}

    try:
        order_time = parse_order_time(order_data)
    except ValueError as e:
        return {"order_id": order_data.get('OrderId'), "sla_status": f"Error parsing order: {str(e)}", "time_diff": None}
    
    # Calculate the time difference between the current time and the order time
    time_diff = current_time - order_time
    sla_limit = timedelta(hours=SLA_HOURS)

    # Determine if order is within SLA or overdue
    if time_diff <= sla_limit:
        return {
            "order_id": order_data.get('OrderId'),
            "sla_status": "Within SLA",
            "time_diff": str(time_diff)
        }
    else:
        overdue_by = time_diff - sla_limit
        return {
            "order_id": order_data.get('OrderId'),
            "sla_status": "Overdue",
            "time_diff": str(overdue_by)
        }

def check_orders_after_date_sla(date: str) -> Dict[str, Any]:
    """
    Function to check SLA compliance for all orders after a specific date.
    """
    try:
        orders = get_orders_after_date(date)
        overdue_orders = []

        for order in orders:
            sla_status = check_order_sla(order)
            if sla_status["sla_status"] == "Overdue":
                overdue_orders.append(sla_status)

        if overdue_orders:
            return {"status": "Overdue orders", "orders": overdue_orders}
        else:
            return {"status": "All orders are within SLA", "orders": []}
    except Exception as e:
        return {"status": "Error", "message": f"Error checking SLA for orders after {date}: {str(e)}"}

def check_all_orders_sla() -> Dict[str, Any]:
    """
    Function to check SLA compliance for all orders in the system.
    """
    try:
        all_orders = get_all_orders()  # Ensure this function is defined
        overdue_orders = []

        for order in all_orders:
            sla_status = check_order_sla(order)
            if sla_status["sla_status"] == "Overdue":
                overdue_orders.append(sla_status)

        if overdue_orders:
            return {"status": "Overdue orders", "orders": overdue_orders}
        else:
            return {"status": "All orders are within SLA", "orders": []}
    except Exception as e:
        return {"status": "Error", "message": f"Error checking SLA for all orders: {str(e)}"}

# Test the functions here (Optional)
if __name__ == "__main__":
    # Check SLA for a specific order
    order_id = "0rj8FZJE"  # Replace with an actual order ID
    order = get_order(order_id)
    if order:
        print(f"Order details: {order}")
        sla_status = check_order_sla(order)
        print(type(sla_status))
        print(sla_status)
    else:
        print(f"Order with ID {order_id} not found.")

    # Check SLA for orders placed after a certain date
    # Uncomment this to test
    # print(check_orders_after_date_sla("2024-01-01"))

    # Check SLA for all orders in the system
    # Uncomment this to test
    # print(check_all_orders_sla())
