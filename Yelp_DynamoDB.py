import json
import csv
import time
from collections import defaultdict
import simplejson as json
import boto3
from datetime import datetime
import requests
from decimal import *

def lambda_handler (event, context):	
	dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
	table = dynamodb.Table('test')
	API_KEY = 'ECFNcAjrYLgEQUhZZAj9BFpRPBNwJVFu6RQcchve8o6hqQmmyuLm4Jj0uNP47A3kMfV9MIXtG8qkOlPXckub3PJxmW378dEvfvPUIbsg_ddDqnzDuu0lPUKnHocVYnYx' 
	ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
	ENDPOINT_ID = 'https://api.yelp.com/v3/businesses/' # + {id}
	HEADERS = {'Authorization': 'bearer %s' % API_KEY}
	cuisines = ["chinese", "korean", "thai", "japanese", "french", "mediterranean", "mexican", "italian", "greek", "american"]
	PARAMETERS = {'term': 'food', 
			  'limit': 50,
			  'radius': 10000,
			  'offset': 200,
			  'location': 'Manhattan'}

	for cuisine in cuisines: 
		response = requests.get(url = ENDPOINT, params =  PARAMETERS, headers=HEADERS)
		PARAMETERS['term'] = cuisine
		business_data = response.json()['businesses']
		for business in business_data:
			now = datetime.now()
			dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
			table.put_item(
			Item = {
				'business_id':is_null(business['id']),
				'name':  is_null(business['name']),
				'cuisine': is_null(cuisine),
				'rating': is_null(Decimal(business['rating'])),
				'Number of Reviews' : is_null(Decimal(business['review_count'])),
				'Address': is_null(business['location']['address1']),
				'Zip Code': is_null(business['location']['zip_code']),
				'Latitude': is_null(str(business['coordinates']['latitude'])),
				'Longitude': is_null(str(business['coordinates']['longitude'])),
				'insertedAtTimestamp': is_null(dt_string)
					}
			)

def is_null (input):
	if len(str(input)) == 0:
		return 'N/A'
	else:
		return input