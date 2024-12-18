from flask import Flask,jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from Mongo.listing_access import ListingAccess
from Mongo.order_access import OrderAccess
from mocks.order import Order, publishOrderToQueue
from mocks.listing_items_status_change import Status,listingsItemStatusChange, publishListingItemsStatusChange
from mocks.listing_items_mfn_quantity_change import listingItemsMfnQuantityChange, FulfillmentChannelCode, publishListingItemsMfnQuantityChange
from mocks.fulfillment_order_status import FulfillmentOrderStatus, generateWithOrderIdAndStatus, publishFulfillmentOrderStatusNotification
from flask import request
import os
from Chatbot.agent import SLAAgent
from Prince.forecast import getForecast, getForecastForId

app = Flask(__name__)
listingAccess = ListingAccess()
orderAccess = OrderAccess()
model_name = "meta-llama/Llama-3-70b-chat-hf" 
agent = SLAAgent(model=model_name)


@app.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify that the service is running properly.
    """
    try:
        # Add any additional checks here, such as database connectivity, external service status, etc.
        return jsonify({
            "status": "success",
            "message": "Service is healthy",
            "details": {
                "service": "running",
                "database": "connected",  # Replace with actual check if required
                "uptime": "72 hours"     # Add more metrics if needed
            }
        }), 200
    except Exception as e:
        return jsonify({
            "status": "failure",
            "message": "Service is unhealthy",
            "details": {
                "error": str(e)
            }
        }), 500


@app.post("/listing")
def getListing():
    try:
        body = request.get_json()
        
        listingId = body["UniqueId"]
        
        listing = listingAccess.getListing(listingId)
        
        return listing.__dict__()
        
    except Exception as e:
        print(e)
        return {
            "message": "Error fetching listing"
        }, 402

@app.get('/listings')
def paginatedListings():
    
    try:
        pageNumber = int(request.args.get('page'))
        pageSize = int(request.args.get('size'))
        
        listings = listingAccess.getPaginated(pageNumber, pageSize)
        
        returnList = []
        
        for listing in listings:
            returnList.append(listing.__dict__())
            
        return {
            "listings": returnList
        }
        
    except Exception as e:
        pageNumber = 0
        pageSize = 50
        listings = listingAccess.getPaginated(pageNumber, pageSize)
        
        returnList = []
        
        for listing in listings:
            returnList.append(listing.__dict__())
            
        return {
            "listings": returnList
        }

@app.get('/listings/<uniqueId>')
def getListingById(uniqueId):
    try:
        listing = listingAccess.getListing(uniqueId)
        return listing.__dict__()
        
    except Exception as e:
        print(e)
        return {
            "message": "Error fetching listing"
        }, 402
        
@app.post('/placeorder')
def placeOrder():
    try:
        body = request.get_json()
        
        order = Order.__from_dict__(body)
        
        #publish order to queue
        publishOrderToQueue(order)
        
        orderAccess.insertOrder(order)
        
        return {
            "message": "Order placed successfully"
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error placing order"
        }, 402
        

@app.get("/allorders")
def getAllOrders():
    try:
        orders = orderAccess.getAllOrders()
        
        returnList = []
        
        for order in orders:
            returnList.append(order.__dict__())
            
        return {
            "orders": returnList
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error fetching orders"
        }, 402
        
@app.post("/orderprice")
def getOrderPrice():
    try:
        body = request.get_json()
        
        orderId = body["OrderId"]
        
        price = orderAccess.getPrice(orderId)
        
        return {
            "price": price
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error fetching order price"
        }, 402

#list of orders
@app.post("/orderprices")
def getOrderPrices():
    try:
        body = request.get_json()
        
        orders = [Order.__from_dict__(order) for order in body["Orders"]]
        
        prices =  orderAccess.getPrices(orders)
            
        return {
            "prices": prices
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error fetching order prices"
        }, 402
        
@app.post("/publishlistingupdateevent")
def publishListingUpdateEvent():
    try:
        body = request.get_json()
        
        sku = body["Sku"]
        status = body["Status"]
        status = Status[status]
        
        event = listingsItemStatusChange("hackathon",sku,status)
        
        publishListingItemsStatusChange(event)
        
        return {
            "message": "Event published successfully"
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error publishing event"
        }, 402
        
@app.post("/publishlistingquantitychangeevent")
def publishListingQuantityChangeEvent():
    try:
        body = request.get_json()
        
        sku = body["Sku"]
        quantity = body["Quantity"]
        
        event = listingItemsMfnQuantityChange("hackathon", FulfillmentChannelCode.MFN, sku, quantity)
        
        publishListingItemsMfnQuantityChange(event)
        
        return {
            "message": "Event published successfully"
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error publishing event"
        }, 402
        
@app.post("/publishorderstatuschangeevent")
def publishOrderStatusChangeEvent():
    try:
        body = request.get_json()
        
        orderId = body["OrderId"]
        status = body["Status"]
        status = FulfillmentOrderStatus[status]
        
        event = generateWithOrderIdAndStatus(orderId, status)
        
        publishFulfillmentOrderStatusNotification(event)
        
        return {
            "message": "Event published successfully"
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error publishing event"
        }, 402
        


@app.route('/getChatResponse', methods=['POST'])
def get_chat_response():
    try:
        # Parse JSON body from the request
        body = request.get_json()
        if not body or "prompt" not in body:
            return jsonify({"message": "Invalid request: 'prompt' is required"}), 400
        prompt = body["prompt"]
        response = agent.ask_question(prompt)
        return jsonify(response)

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"message": "Error fetching response"}), 500


@app.route('/forecast', methods=['POST'])
def forecast():
    try:
        body = request.get_json()
        
        productId = body["Sku"]
        
        forecast = getForecastForId(productId)
        
        return {
            "forecast": forecast
        }
        
    except Exception as e:
        print(e)
        return {
            "message": "Error fetching forecast"
        }, 402

def run():
    load_dotenv()
    CORS(app)
    app.run(port=8080,host="0.0.0.0", debug=True)

#order place api
#listing by seller
#invoice generation
#number of order by status date range
#publish all events api
#total order price between months