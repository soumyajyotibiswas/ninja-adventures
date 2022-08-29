# Create S3 buckets with boto3

```Python
import boto3
bucket_name = '<bucket_name>'
region = '<region_code>'
# Create S3 client
s3_client = boto3.client('s3', region_name=region)
location = {'LocationConstraint': region}
# Create bucket
s3_client.create_bucket(Bucket=bucket_name,CreateBucketConfiguration=location)
# Apply public block access
response = s3_client.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    }
)
# See public block access is applied
s3_client.get_public_access_block(
    Bucket=bucket_name
)
```
