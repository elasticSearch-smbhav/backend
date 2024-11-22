import boto3
from kafka.admin import KafkaAdminClient, NewTopic
from dotenv import load_dotenv
import os

load_dotenv()

awsAccessKey = os.getenv("MSK_ACCESS")
awsSecretKey = os.getenv("MSK_SECRET")
clusterArn = os.getenv("MSK_CLUSTER_ARN")
region = "eu-north-1"

def getBrokerEndpoints(clusterArn):
    client = boto3.client(
        'kafka',
        aws_access_key_id=awsAccessKey,
        aws_secret_access_key=awsSecretKey,
        region_name=region
    )
    response = client.get_bootstrap_brokers(ClusterArn=clusterArn)
    print(response)
    return response.get("BootstrapBrokerStringTls")


def _createKafkaTopic(bootstrapServers, topicName, partitions=1, replicationFactor=2):
    try:
        adminClient = KafkaAdminClient(
            bootstrap_servers=bootstrapServers,
            security_protocol="SSL"  # Ensure proper security setup
        )
        topic = NewTopic(name=topicName, num_partitions=partitions, replication_factor=replicationFactor)
        adminClient.create_topics([topic])
        print(f"Topic '{topicName}' created successfully.")
    except Exception as e:
        print(f"Error creating topic: {e}")
        
def createKafkaTopic(topicName):
    bootstrapServers = getBrokerEndpoints(clusterArn)
    print(bootstrapServers)
    _createKafkaTopic(bootstrapServers, topicName)
    
    
    