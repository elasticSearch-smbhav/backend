from enum import Enum
from mocks.random import generateRandomString, generateRandomInt, generateRandomDateTime
import random
from dotenv import load_dotenv
from AWS.sqs import publishToSqsQueue
import os
import datetime

load_dotenv()

queueUrl = os.getenv("FULFILLMENT_ORDER_STATUS_QUEUE_URL")

class EventType(Enum):
    Order= "Order"
    Shipment = "Shipment"
    Return = "Return"
    
    
class FulfillmentOrderStatus(Enum):
    Received = "Received" 
    Invalid = "Invalid"
    Planning = "Planning"
    Processing = "Processing"
    Cancelled = "Cancelled"
    Complete = "Complete"
    CompletePartialled = "CompletePartialled"
    Unfulfillable = "Unfulfillable"
    
    
class FulfillmentShipmentStatus(Enum):
    Pending = "Pending"
    Shipped = "Shipped"
    CancelledByFulfiller = "CancelledByFulfiller"
    CancelledBySeller = "CancelledBySeller"
    
class FulfillmentShipment:
    def __init__(self, estimatedArrivalDateTime: datetime.datetime, fulfillmentShipmentStatus: FulfillmentShipmentStatus):
        self.estimatedArrivalDateTime = estimatedArrivalDateTime
        self.fulfillmentShipmentStatus = fulfillmentShipmentStatus
        
    def __str__(self):
        return f"estimatedArrivalDateTime: {self.estimatedArrivalDateTime}, fulfillmentShipmentStatus: {self.fulfillmentShipmentStatus.name}"
    
    def __dict__(self):
        return {
            "EstimatedArrivalDateTime": self.estimatedArrivalDateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "FulfillmentShipmentStatus": self.fulfillmentShipmentStatus.name
        }
        
def generateRandomFulfillmentShipment() -> FulfillmentShipment:
    #generate a random date and time
    estimatedArrivalDateTime = generateRandomDateTime()
    
    #pick a random fulfillment shipment status
    fulfillmentShipmentStatus = random.choice(list(FulfillmentShipmentStatus))
    
    return FulfillmentShipment(estimatedArrivalDateTime, fulfillmentShipmentStatus)


class fulfillmentOrderStatusNotification:
    def __init__(self, eventType: EventType, 
                 sellerId: str, 
                 statusUpdatedDateTime: datetime.datetime, 
                 sellerFulfillmentOrderId: str, 
                 filFillmentOrderStatus: FulfillmentOrderStatus, 
                 fulfillmentShipment: FulfillmentShipment):
        self.eventType = eventType
        self.sellerId = sellerId
        self.statusUpdatedDateTime = statusUpdatedDateTime
        self.sellerFulfillmentOrderId = sellerFulfillmentOrderId
        self.filFillmentOrderStatus = filFillmentOrderStatus
        self.fulfillmentShipment = fulfillmentShipment
        
    def __str__(self):
        return f"eventType: {self.eventType.name}, sellerId: {self.sellerId}, statusUpdatedDateTime: {self.statusUpdatedDateTime}, sellerFulfillmentOrderId: {self.sellerFulfillmentOrderId}, filFillmentOrderStatus: {self.filFillmentOrderStatus.name}, fulfillmentShipment: {self.fulfillmentShipment}"
    
    def __dict__(self):
        return {
            "EventType": self.eventType.name,
            "SellerId": self.sellerId,
            "StatusUpdatedDateTime": self.statusUpdatedDateTime.strftime("%Y-%m-%d %H:%M:%S"),
            "SellerFulfillmentOrderId": self.sellerFulfillmentOrderId,
            "FilFillmentOrderStatus": self.filFillmentOrderStatus.name,
            "FulfillmentShipment": self.fulfillmentShipment.__dict__()
        }
        
        
def generateRandomFulfillmentOrderStatusNotification() -> fulfillmentOrderStatusNotification:
    #pick a random event type
    eventType = random.choice(list(EventType))
    
    #generate a random date and time
    statusUpdatedDateTime = generateRandomDateTime()
    
    #generate a random seller id
    sellerId = generateRandomString(8)
    
    #generate a random seller fulfillment order id
    sellerFulfillmentOrderId = generateRandomString(8)
    
    #pick a random fulfillment order status
    filFillmentOrderStatus = random.choice(list(FulfillmentOrderStatus))
    
    #generate a random fulfillment shipment
    fulfillmentShipment = generateRandomFulfillmentShipment()
    
    return fulfillmentOrderStatusNotification(eventType, sellerId, statusUpdatedDateTime, sellerFulfillmentOrderId, filFillmentOrderStatus, fulfillmentShipment)


def publishFulfillmentOrderStatusNotification(fulfillmentOrderStatusNotification: fulfillmentOrderStatusNotification) -> fulfillmentOrderStatusNotification:
    #publish the fulfillment order status notification to the SQS queue
    publishToSqsQueue(queueUrl, fulfillmentOrderStatusNotification.__dict__())
    print(f"Published message to SQS queue: {fulfillmentOrderStatusNotification}")
    
    
