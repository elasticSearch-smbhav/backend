from enum import Enum
from mocks.random import generateRandomString, generateRandomInt, generateRandomDateTime
from mocks.fulfillment_order_status import FulfillmentOrderStatus
import random
from dotenv import load_dotenv
from AWS.sqs import publishToSqsQueue
import os
from typing import List
import datetime

load_dotenv()

queueUrl = os.getenv("ORDER_QUEUE_URL")

class ListItem:
    def __init__(self, sku:str, quantity:int):
        self.sku = sku
        self.quantity = quantity
        
    
    def __str__(self):
        return f"sku: {self.sku}, quantity: {self.quantity}"
    
    def __dict__(self):
        return {
            "SKU": self.sku,
            "Quantity": self.quantity
        }
        
def generateRandomListItem() -> ListItem:
    #generate a random sku
    sku = generateRandomString(8)
    
    #generate a random quantity
    quantity = generateRandomInt(1, 10)
    
    return ListItem(sku, quantity)
        
class Order:
    def __init__(self, orderId: str, 
                 purchaseDate: datetime.datetime, 
                 listItems: List[ListItem], 
                 fulfillmentOrderStatus: FulfillmentOrderStatus = FulfillmentOrderStatus.Received):
        
        self.orderId = orderId
        self.purchaseDate = purchaseDate
        self.listItems = listItems
        self.fulfillmentOrderStatus = fulfillmentOrderStatus
        
    def __str__(self):
        return f"orderId: {self.orderId}, purchaseDate: {self.purchaseDate}, fulfillmentOrderStatus: {self.fulfillmentOrderStatus.name}, listItems: {', '.join([str(listItem) for listItem in self.listItems])}"
    
    def __dict__(self):
        return {
            "OrderId": self.orderId,
            "PurchaseDate": self.purchaseDate.strftime("%Y-%m-%d %H:%M:%S"),
            "FulfillmentOrderStatus": self.fulfillmentOrderStatus.name,
            "ListItems": [listItem.__dict__() for listItem in self.listItems]
        }
    
    @staticmethod
    def __from_dict__(data: dict):
        orderId = data["OrderId"]
        purchaseDate = datetime.datetime.strptime(data["PurchaseDate"], "%Y-%m-%d %H:%M:%S")
        fulfillmentOrderStatus = FulfillmentOrderStatus[data["FulfillmentOrderStatus"]]
        listItems = [ListItem(sku=item["SKU"], quantity=item["Quantity"]) for item in data["ListItems"]]
        
        return Order(orderId, purchaseDate, listItems, fulfillmentOrderStatus)
        
        
        
def generateRandomOrder() -> Order:
    #generate a random order id
    orderId = generateRandomString(8)
    
    #generate a random purchase date
    purchaseDate = generateRandomDateTime()
    
    #generate a random list of list items
    listItems = [generateRandomListItem() for _ in range(generateRandomInt(1, 5))]
    fulfillmentOrderStatus = random.choice(list(FulfillmentOrderStatus))
    
    return Order(orderId, purchaseDate, listItems, fulfillmentOrderStatus)

def publishOrderToQueue(order: Order):
    publishToSqsQueue(queueUrl, order.__dict__())
    print(f"Order {order.orderId} published to queue")
    
    
        