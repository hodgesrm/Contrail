import boto3
import datetime
import urllib.request

# Make sure to create a file called "secret.py" that defines these three strings
from secret import AWS_ACCESS_KEY_ID, AWS_SECRET, AWS_BUCKET_NAME

session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET
)
s3 = session.client('s3')

print("Starting download...")

pricefile = urllib.request.URLopener()
pricefile.retrieve(
    'https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/us-east-1/index.json',
    'prices.json'
)

print("Starting upload...")

s3.upload_file('prices.json', AWS_BUCKET_NAME, datetime.datetime.utcnow().isoformat() + ".json")

print("Complete!")
