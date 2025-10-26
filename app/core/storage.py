from typing import Optional
from minio import Minio
from minio.error import S3Error
import io
import logging
from fastapi import HTTPException, status
from app.core.config import settings

logger = logging.getLogger(__name__)

class MinIOStorageClient:
    """
    MinIO client wrapper for file operations.
    Handles file uploads, downloads, and deletions.
    """
    
    def __init__(self):
        """Initialize the MinIO client using settings"""
        try:
            self.client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ROOT_USER,
                secret_key=settings.MINIO_ROOT_PASSWORD,
                secure=settings.MINIO_SECURE
            )
            self.bucket_name = settings.MINIO_BUCKET_NAME

            # Ensure bucket exists on client initialization
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
                logger.info(f"MinIO bucket '{self.bucket_name}' created.")
            else:
                logger.info(f"MinIO bucket '{self.bucket_name}' verified.")
                
        except Exception as e:
            logger.error(f"Failed to initialize MinIO client: {e}")
            raise RuntimeError(f"MinIO connection failed: {e}")

    def upload_file(self, file_id: str, file_content: bytes, content_type: str = 'image/webp') -> str:
        """
        Uploads a file to MinIO and returns the file URL.
        
        Args:
            file_id: Unique identifier for the file
            file_content: File content as bytes
            content_type: MIME type of the file
            
        Returns:
            URL of the uploaded file
        """
        data_stream = io.BytesIO(file_content)
        data_size = len(file_content)
        
        try:
            # Upload to MinIO
            result = self.client.put_object(
                self.bucket_name,
                file_id,
                data_stream,
                data_size,
                content_type=content_type
            )
            
            # Construct the public URL
            file_url = f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{result.object_name}"
            logger.info(f"File uploaded to MinIO: {file_url}")
            return file_url
            
        except S3Error as e:
            logger.error(f"MinIO upload error: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Storage service unavailable."
            )

    def delete_file(self, file_id: str) -> bool:
        """
        Deletes a file from MinIO.
        
        Args:
            file_id: Unique identifier of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.remove_object(self.bucket_name, file_id)
            logger.info(f"File deleted from MinIO: {file_id}")
            return True
        except S3Error as e:
            logger.warning(f"MinIO delete warning (file might not exist): {e}")
            return False

    def get_file_url(self, file_id: str) -> str:
        """
        Generates a public URL for a file.
        
        Args:
            file_id: Unique identifier of the file
            
        Returns:
            Public URL of the file
        """
        return f"http://{settings.MINIO_ENDPOINT}/{self.bucket_name}/{file_id}"

    def file_exists(self, file_id: str) -> bool:
        """
        Check if a file exists in MinIO.
        
        Args:
            file_id: Unique identifier of the file
            
        Returns:
            True if file exists, False otherwise
        """
        try:
            self.client.stat_object(self.bucket_name, file_id)
            return True
        except S3Error as e:
            if e.code == "NoSuchKey":
                return False
            logger.error(f"Error checking file existence: {e}")
            return False

# Dependency to access the storage client
def get_minio_client() -> MinIOStorageClient:
    return MinIOStorageClient()