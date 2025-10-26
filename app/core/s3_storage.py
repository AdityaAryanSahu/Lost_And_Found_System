import boto3
import io
import logging
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)

class S3StorageClient:
    """
    AWS S3 storage client for file operations.
    Replaces MinIO for production deployments.
    """
    
    def __init__(self):
        # Initialize S3 client
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_REGION
        )
        self.bucket_name = settings.AWS_S3_BUCKET
        
        # Ensure bucket exists
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            logger.info(f"S3 bucket '{self.bucket_name}' verified.")
        except Exception as e:
            logger.error(f"Failed to verify S3 bucket: {e}")
            raise RuntimeError("S3 connection failed during startup.")

    def upload_file(self, file_id: str, file_content: bytes, content_type: str = 'image/webp') -> str:
        """Uploads a file to S3 and returns the file URL."""
        
        try:
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_id,
                Body=file_content,
                ContentType=content_type
            )
            
            # Construct the public URL
            file_url = f"{settings.AWS_S3_URL}/{self.bucket_name}/{file_id}"
            logger.info(f"File uploaded to S3: {file_url}")
            return file_url
            
        except Exception as e:
            logger.error(f"S3 upload error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Storage service unavailable."
            )

    def delete_file(self, file_id: str) -> bool:
        """Deletes a file from S3."""
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=file_id
            )
            logger.info(f"File deleted from S3: {file_id}")
            return True
        except Exception as e:
            logger.warning(f"S3 delete warning: {e}")
            return False

    def get_file_url(self, file_id: str) -> str:
        """Generates a public URL for a file."""
        return f"{settings.AWS_S3_URL}/{self.bucket_name}/{file_id}"

# Dependency
def get_storage_client() -> S3StorageClient:
    return S3StorageClient()