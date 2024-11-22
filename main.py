from mocks.fulfillment_order_status import generateRandomFulfillmentOrderStatusNotification, publishFulfillmentOrderStatusNotification
from mocks.listing_items_mfn_quantity_change import generateRandomListingItemsMfnQuantityChange, publishListingItemsMfnQuantityChange
from mocks.listing_items_status_change import generateRandomListingItemsStatusChange, publishListingItemsStatusChange
from mocks.order import generateRandomOrder, publishOrderToQueue
from Mongo.order_access import OrderAccess
from Mongo.listing_access import ListingAccess
from AWS.kafka import createKafkaTopic
def main():
    # listingItemsMfnQuantityChange = generateRandomListingItemsMfnQuantityChange()
    # publishListingItemsMfnQuantityChange(listingItemsMfnQuantityChange)
    
    # fulfillmentOrderStatusNotification = generateRandomFulfillmentOrderStatusNotification()
    # publishFulfillmentOrderStatusNotification(fulfillmentOrderStatusNotification)
    
    # listingItemsStatusChange = generateRandomListingItemsStatusChange()
    # publishListingItemsStatusChange(listingItemsStatusChange)
    
    # order = generateRandomOrder()
    # obj = OrderAccess()
    
    # print(obj.getAllOrders()[0].__dict__())
    # publishOrderToQueue(order)
    
    l = ListingAccess()
    
    print(l.getAllListings()[0])
    
if __name__ == "__main__":
    main()
