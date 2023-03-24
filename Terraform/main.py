import boto3
from wand.image import Image

def lambda_handler(event, context):
    # Set up S3 client
    s3 = boto3.client('s3')

    # Retrieve list of objects in S3 bucket
    bucket_name = 'your_bucket_name'
    objects = s3.list_objects_v2(Bucket=bucket_name)

    # Loop through objects and convert images to GIF format
    for obj in objects['Contents']:
        key = obj['Key']
        if key.endswith('.jpg') or key.endswith('.jpeg') or key.endswith('.png'):
            # Download image from S3
            image_file = s3.get_object(Bucket=bucket_name, Key=key)['Body'].read()

            # Convert image to GIF format using Wand library
            with Image(blob=image_file) as img:
                img.format = 'gif'
                gif_file = img.make_blob()

            # Upload GIF file to S3
            gif_key = key[:-4] + '.gif'
            s3.put_object(Bucket=bucket_name, Key=gif_key, Body=gif_file)