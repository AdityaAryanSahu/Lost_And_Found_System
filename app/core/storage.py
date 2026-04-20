from typing import Optional
import boto3
import io
import logging
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)

class R2StorageClient:
    """
    Cloudflare R2 client wrapper (S3-compatible).
    Handles file uploads, deletions, and URL generation.
    """

    def __init__(self):
        try:
            self.client = boto3.client(
                "s3",
                endpoint_url=settings.R2_ENDPOINT,
                aws_access_key_id=settings.R2_ACCESS_KEY,
                aws_secret_access_key=settings.R2_SECRET_KEY,
                region_name="auto"
            )

            self.bucket_name = settings.R2_BUCKET_NAME

            logger.info(f"Connected to R2 bucket: {self.bucket_name}")

        except Exception as e:
            logger.error(f"Failed to initialize R2 client: {e}")
            raise RuntimeError(f"R2 connection failed: {e}")

    def upload_file(
        self,
        file_id: str,
        file_content: bytes,
        content_type: str = "image/webp"
    ) -> str:
        """
        Upload file to R2 and return public URL.
        """
        try:
            self.client.put_object(
                Bucket=self.bucket_name,
                Key=file_id,
                Body=io.BytesIO(file_content),
                ContentType=content_type
            )

            file_url = f"{settings.R2_PUBLIC_URL}/{file_id}"
            logger.info(f"File uploaded to R2: {file_url}")

            return file_url

        except Exception as e:
            logger.error(f"R2 upload error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Storage service unavailable."
            )

    def delete_file(self, file_id: str) -> bool:
        """
        Delete file from R2.
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=file_id
            )
            logger.info(f"File deleted from R2: {file_id}")
            return True

        except Exception as e:
            logger.warning(f"R2 delete warning: {e}")
            return False

    def get_file_url(self, file_id: str) -> str:
        """
        Return public URL of file.
        """
        return f"{settings.R2_PUBLIC_URL}/{file_id}"

    def file_exists(self, file_id: str) -> bool:
        """
        Check if file exists in R2.
        """
        try:
            self.client.head_object(
                Bucket=self.bucket_name,
                Key=file_id
            )
            return True

        except Exception:
            return False


# Dependency
def get_r2_client() -> R2StorageClient:
    return R2StorageClient()