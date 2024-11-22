import boto3
import time
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Create SQS client
accessKey = os.getenv("ACCESS_KEY")
secretKey = os.getenv("SECRET_KEY")

sqs = boto3.client('sqs', region_name="eu-north-1", aws_access_key_id=accessKey, aws_secret_access_key=secretKey)

def publishToSqsQueue(queueUrl, messageBody={}):
    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queueUrl,
        DelaySeconds=10,
        MessageBody=json.dumps(messageBody)
    )

    return response