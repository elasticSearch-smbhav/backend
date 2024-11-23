import json
from data_access.data_access import ListingAccess

ListingAccess = ListingAccess()

def lambda_handler(event, context):
    
    for record in event['Records']:
        data = json.loads(record['body'])
        
        uniqueId = data['Sku']
        status = data['Status']
        
        ListingAccess.updateListingStatus(uniqueId, status)
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }