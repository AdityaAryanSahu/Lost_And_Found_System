# app/services/image_service.py
import uuid
import tempfile
from datetime import datetime
import os
from typing import List, Optional
from fastapi import UploadFile
from app.core.storage import get_storage_client, StorageClient
from app.utils.image_processing import img_proc 
from app.models.image import Image

class ImageService:
    
    def __init__(self):
        self.storage_client = get_storage_client()

    async def process_and_upload_image(self, file: UploadFile, item_id: str) -> Image:
       
        #read the file content
        file_content = await file.read()
        
        #use a temporary file to save/process the image
        with tempfile.NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            tmp.write(file_content)
            temp_path = tmp.name

        try:
            #process the image using your utility
            img_proc(temp_path) 
            
            #reread the processed content
            with open(temp_path, 'rb') as f:
                processed_content = f.read()

            #upload to MinIO/S3 mock
            file_id = f"{item_id}-{str(uuid.uuid4())}.webp" 
            file_url = await self.storage_client.upload_file(
                bucket_name="lost-and-found-items",
                file_id=file_id,
                file_content=processed_content
            )
            
            return Image(
                item_id=item_id,
                url=file_url,
                date_uploaded=datetime.now()
            )
            
        finally:
            os.unlink(temp_path)

    async def delete_image(self, url: str) -> bool:
        """Deletes an image based on its URL (mocks parsing the URL)."""
        # Mock URL parsing: 'http://minio.local/bucket_name/file_id'
        parts = url.split('/')
        if len(parts) >= 4:
            bucket_name = parts[-2]
            file_id = parts[-1]
            return await self.storage_client.delete_file(bucket_name, file_id)
        return False