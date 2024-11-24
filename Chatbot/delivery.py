import json
from Mongo.order_access import OrderAccess
from mocks.order import Order, generateRandomOrder, ListItem
from AWS.sqs import publishToSqsQueue
from typing import List

# Initialize the OrderAccess object
order_access = OrderAccess()

def serialize_order(order: Order) -> dict:
    """
    Function to serialize the order object, excluding non-serializable methods.
    """
    order_dict=order.__dict__()
    serialized_order = {
            "OrderId": order_dict.get("OrderId"),
            "PurchaseDate": order_dict.get("PurchaseDate"),
            "FulfillmentOrderStatus": order_dict.get("FulfillmentOrderStatus"),
            "ListItems": [
                {"sku": item["SKU"], "quantity": item["Quantity"]} for item in order_dict.get("ListItems", [])
            ]
        }
        
    return serialized_order
   

def get_order(order_id: str) -> dict:
    """
    Function to fetch a specific order using the order ID.
    Returns data in a structured JSON format.
    """
    try:
        # Fetch the order from database using OrderAccess
        order = order_access.getOrder(order_id)
        if isinstance(order, Order):  # Ensure the fetched object is an Order instance
            return {
                "status": "success",
                "message": "Order found",
                "data": serialize_order(order)  # Serialize the order to remove methods
            }
        else:
            return {
                "status": "error",
                "message": f"Fetched object is not an Order instance for ID {order_id}",
                "data": None
            }

    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching order with ID {order_id}: {str(e)}",
            "data": None
        }

def get_orders_after_date(date: str) -> dict:
    """
    Function to fetch orders made after a specific date.
    Returns data in a structured JSON format.
    """
    try:
        orders = order_access.getOrdersAfterDate(date)

        if orders:
            orders_list = [serialize_order(order) for order in orders if isinstance(order, Order)]  # Serialize each order
            return {
                "status": "success",
                "message": f"Orders found after {date}",
                "data": orders_list
            }
        else:
            return {
                "status": "error",
                "message": f"No orders found after {date}",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching orders after {date}: {str(e)}",
            "data": None
        }

def get_all_orders() -> dict:
    """
    Function to fetch all orders in the system.
    Returns data in a structured JSON format.
    """
    try:
        orders = order_access.getAllOrders()

        if orders:
            orders_list = [serialize_order(order) for order in orders if isinstance(order, Order)]  # Serialize each order
            return {
                "status": "success",
                "message": "All orders fetched successfully",
                "data": orders_list
            }
        else:
            return {
                "status": "error",
                "message": "No orders found in the database",
                "data": None
            }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error fetching all orders: {str(e)}",
            "data": None
        }

# Function to publish an order to SQS
def publish_order_to_sqs(order: Order) -> dict:
    try:
        # Serialize the order and publish to the SQS queue
        serialized_order = serialize_order(order)
        publishToSqsQueue(os.getenv("ORDER_QUEUE_URL"), serialized_order)
        return {
            "status": "success",
            "message": f"Order {order.orderId} successfully published to queue",
            "data": serialized_order
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error publishing order {order.orderId} to queue: {str(e)}",
            "data": None
        }

# Testing the functions (Optional)
if __name__ == "__main__":
    # Fetch a specific order by ID
    order_response = get_order("0rj8FZJE")
    print(json.dumps(order_response, indent=2))  # Pretty print the JSON response
    print("D")
    # Fetch orders after a certain date
    orders_after_date_response = get_orders_after_date("2024-01-01")
    print(json.dumps(orders_after_date_response, indent=2))
    print("D")
    # Fetch all orders
    all_orders_response = get_all_orders()
    print(json.dumps(all_orders_response, indent=2))
    print("D")
    # Publish an order to SQS
    # order_to_publish = generateRandomOrder()
    # publish_response = publish_order_to_sqs(order_to_publish)
    # print(json.dumps(publish_response, indent=2))
