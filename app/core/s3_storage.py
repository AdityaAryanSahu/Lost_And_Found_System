import boto3

# -------- MINIO CONFIG --------
minio_client = boto3.client(
    "s3",
    endpoint_url="http://localhost:9000",
    aws_access_key_id="minio_user",
    aws_secret_access_key="minio_password_123",
)
# MINIO_ENDPOINT=minio:9000
# MINIO_ROOT_USER=minio_user
# MINIO_ROOT_PASSWORD=minio_password_123
# MINIO_SECURE=False
MINIO_BUCKET_NAME= "lost-and-found"
MINIO_BUCKET = "lost-and-found"
# -------- R2 CONFIG --------
r2_client = boto3.client(
    "s3",
    endpoint_url="https://49521131c7ad36c0bf5add9f4b86b6dc.r2.cloudflarestorage.com",
    aws_access_key_id="9acab320b7b2eaab6a5223885ad08149",
    aws_secret_access_key="510e028821601c7ae0c7e75c5d4044b59238c115e8797f9e2dd095ea0881df75",
)

R2_BUCKET = "lost-found-images"

# -------- MIGRATION --------
objects = minio_client.list_objects_v2(Bucket=MINIO_BUCKET)

for obj in objects.get("Contents", []):
    key = obj["Key"]
    print(f"Copying: {key}")

    file_obj = minio_client.get_object(Bucket=MINIO_BUCKET, Key=key)

    r2_client.put_object(
        Bucket=R2_BUCKET,
        Key=key,
        Body=file_obj["Body"].read(),
        ContentType=file_obj.get("ContentType", "application/octet-stream")
    )

print("✅ Migration complete")