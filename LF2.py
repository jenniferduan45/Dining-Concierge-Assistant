import boto3
import json
import requests
from requests_aws4auth import AWS4Auth

# get message from SQS
def get_SQS_message():
    sqs_client = boto3.client("sqs", region_name="us-east-1")
    response = sqs_client.receive_message(
        QueueUrl='https://sqs.us-east-1.amazonaws.com/686660213986/DiningConcierge',
        MaxNumberOfMessages=5,
        WaitTimeSeconds=10,
    )
    return response.get('Messages', [])

#OpenSearch master password: Master123!

# elastic search 
def elastic_search(cuisine):
    region = 'us-east-1'
    service = 'es'
    credentials = session.get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

    host = 'https://search-test-5gj22liepdem6dqzjb44g5at2i.us-east-1.es.amazonaws.com'
    index = 'test'
    url = host + '/' + index + '/_search'

    query = {
        "size": 200,
        "query": {
            "multi_match": {
                "query": cuisine,
                "fields": ["id", "categories"]
            }
        }
    }

    # Elasticsearch 6.x requires an explicit Content-Type header
    headers = { "Content-Type": "application/json" }

    # Make the signed HTTP request
    r = requests.get(url, auth=awsauth, headers=headers, data=json.dumps(query))

    # Create the response and add some extra content to support CORS
    response = {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": '*'
        },
        "isBase64Encoded": False
    }

    # Add the search results to the response
    response['body'] = r.text
    return response

# def dining_suggestion(messages):
#     suggestion_results = []
#     for msg in messages:
#         msg['search_result'] = elastic_search(category=msg['Cuisine'])
#         suggestion_results.append(msg)
#     return suggestion_results

def query_dynamoDB(response):
    # get client
    client = boto3.resource('dynamodb')
    # get table
    table = client.Table('DiningData')
    business_ids = []
    for k in range(len(response)):
        business_ids.append(res[k]['_source']['business_id'])
    query_result = []
    for bus_id in business_ids:
        result = table.get_item(key={'business_id':bus_id})
        quesry_result.append(result)
    return query_result

# build message for users 
def construct_message(sqs_result):
    numofPeople = sqs_result['Messages'][0]['MessageAttributes']['numofPeople']
    Time = sqs_result['Messages'][0]['MessageAttributes']['diningTime']
    Date = sqs_result['Messages'][0]['MessageAttributes']['diningDate']
    Cusine = sqs_result['Messages'][0]['MessageAttributes']['Cusine']
    Region = sqs_result['Messages'][0]['MessageAttributes']['Region']
    msg_result = 'Hello! Here are your {0} restaurant suggestion in {1} for {2}, for {3} at {4}: '.format(
    Cusine, Region, numofPeople, Date, Time)    
    return msg_result

# send emails/texts
def send_message(sqs_result, msg_result):
    client = boto3.client('sns')
    ses = boto3.client('ses')
    topic_name = 'userNotification'
    # phone_number = sqs_result['Messages'][0]['MessageAttributes']['PhoneNumber']
    # client.publish(Phonenumber = phone_number, Message = msg_result)
    email_add = sqs_result['Records'][0]['messageAttributes']['Email']['stringValue']
    tpcArn = 'arn:aws:ses:us-east-1:686660213986:identity/jd3794@columbia.edu:' + topic_name
    subs = sns.subscribe(
        TopicArn=tpcArn,
        Protocol='email',
        Endpoint= email_add 
    )
    response = sns.publish(
    TopicArn = 'arn:aws:ses:us-east-1:686660213986:identity/jd3794@columbia.edu:userNotification',    
    Message=msg_result)

def lambda_handler(event, context):
    sqs_result = get_SQS_message() #1
    es_result = elastic_search(sqs_result) #2
    dynamoDB_result = query_dynamoDB(es_result, sqs_result) #3&4
    msg_result = construct_message(sqs_result) #5
    send_message(sqs_result, msg_result) #6
