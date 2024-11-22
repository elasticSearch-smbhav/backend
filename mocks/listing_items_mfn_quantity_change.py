from enum import Enum
from mocks.random import generateRandomString, generateRandomInt
import random
from dotenv import load_dotenv
from AWS.sqs import publishToSqsQueue
import os

load_dotenv()

queueUrl = os.getenv("LISTINGS_ITEM_MFN_QUANTITY_CHANGE_QUEUE_URL")

class FulfillmentChannelCode(Enum):
    MFN = "MFN"
    AFN = "AFN"

class listingItemsMfnQuantityChange:
    def __init__(self, sellerId: str, fulfillmentChannelCode: FulfillmentChannelCode,sku: str ,quantity: int):
        self.sellerId = sellerId
        self.fulfillmentChannelCode = fulfillmentChannelCode
        self.sku = sku
        self.quantity = quantity
        
    def __str__(self):
        return f"sellerId: {self.sellerId}, fulfillmentChannelCode: {self.fulfillmentChannelCode.name}, sku: {self.sku}, quantity: {self.quantity}"
    
    def __dict__(self):
        return {
            "SellerId": self.sellerId,
            "FulfillmentChannelCode": self.fulfillmentChannelCode.name,
            "Sku": self.sku,
            "Quantity": self.quantity
        }
        
def generateRandomListingItemsMfnQuantityChange() -> listingItemsMfnQuantityChange:
    #all strings are 8 characters long
    sellerId = generateRandomString(8)
    sku = generateRandomString(8)
    
    #pick a random fulfillment channel code
    fulfillmentChannelCode = random.choice(list(FulfillmentChannelCode))
    
    #generate a random quantity
    
    quantity = generateRandomInt(1, 100)
    
    return listingItemsMfnQuantityChange(sellerId, fulfillmentChannelCode, sku, quantity)


def publishListingItemsMfnQuantityChange(listingItemMfnQuantityChange: listingItemsMfnQuantityChange):
    response = publishToSqsQueue(queueUrl, listingItemMfnQuantityChange.__dict__())
    print(f"Published message to SQS queue: {response}")