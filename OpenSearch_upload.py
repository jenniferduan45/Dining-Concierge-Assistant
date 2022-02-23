import requests
import boto3
import csv
from opensearchpy import OpenSearch
from io import BytesIO

host = 'search-test-5gj22liepdem6dqzjb44g5at2i.us-east-1.es.amazonaws.com' 
port = 443
auth = ('master', 'Master123!')

client = OpenSearch(
    hosts = [{'host': host, 'port': port}],
    http_compress = True,
    http_auth = auth,
    use_ssl = True,
    verify_certs = True,
    ssl_assert_hostname = False,
    ssl_show_warn = False
)

with open('restaurants.csv', newline='') as f:
    reader = csv.reader(f)
    restaurants = list(reader)

for restaurant in restaurants:
    index_data = {
        'id': restaurant[0],
        'categories': restaurant[2]
    }
    print ('dataObject', index_data)

    client.index(index="test", doc_type="Restaurant", id=restaurant[0], body=index_data, refresh=True)