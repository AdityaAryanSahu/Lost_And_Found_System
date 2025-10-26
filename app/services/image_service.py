import uuid
import tempfile
from datetime import datetime
import os
from typing import Optional
from fastapi import UploadFile, HTTPException, status
import logging

from app.core.storage import get_minio_client
from app.utils.image_processing import img_proc 
from app.repositories import image_repository
from app.models.image import Image, ImageModel

logger = logging.getLogger(__name__)

class ImageService:
    
    def __init__(self):
        self.storage_client = get_minio_client()
        self.image_repository = image_repository.ImageRepo()

    async def process_and_upload_image(self, file: UploadFile, item_id: str) -> Image:
        """
        Process and upload an image to storage
        """
        try:
            # Read the file content
            file_content = await file.read()
            
            if not file_content:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="File is empty"
                )
            
            # Create a temporary file to save/process the image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
                tmp.write(file_content)
                temp_path = tmp.name

            try:
                # Process the image using your utility
                img_proc(temp_path)
                
                # Re-read the processed content
                with open(temp_path, 'rb') as f:
                    processed_content = f.read()

                # Upload to MinIO
                file_id = f"{item_id}-{str(uuid.uuid4())}.webp"
                file_url = self.storage_client.upload_file(
                    file_id=file_id,
                    file_content=processed_content,
                    content_type="image/webp"
                )
                
                # ✅ FIXED: Replace 'minio' hostname with 'localhost' for frontend access
                file_url = file_url.replace("http://minio:9000", "http://localhost:9000")
                
                # ✅ FIXED: Use 'url' instead of 'path'
                image_dto = Image(
                    item_id=item_id,
                    url=file_url,  # ✅ Changed from 'path' to 'url'
                    date_uploaded=datetime.now()
                )
                
                # Save to repository
                image_model = image_dto.to_model()
                await self.image_repository.add_image(image_model)
                
                logger.info(f"Image processed and uploaded: {file_id}")
                return image_dto
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"Error processing image: {str(e)}"  # ✅ Include error message
            )

    async def delete_image(self, url: str) -> bool:
        """
        Delete an image from storage and repository
        """
        try:
            # Extract file_id from URL
            file_id = url.split('/')[-1]
            
            # Delete from storage
            storage_success = self.storage_client.delete_file(file_id)
            
            # Delete from repository
            repo_success = await self.image_repository.delete_image(url)
            
            logger.info(f"Image deleted: {file_id}")
            return storage_success and repo_success
            
        except Exception as e:
            logger.error(f"Error deleting image: {e}")
            return False

    async def get_image_by_id(self, image_id: str) -> Optional[Image]:
        """
        Get image by ID
        """
        try:
            return await self.image_repository.get_image(image_id)
        except Exception as e:
            logger.error(f"Error retrieving image: {e}")
            return None

# Dependency for FastAPI
def get_image_service() -> ImageService:
    return ImageService()
