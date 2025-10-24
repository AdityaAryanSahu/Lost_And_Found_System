
import uuid
import tempfile
from datetime import datetime
import os
from typing import List, Optional, Annotated
from fastapi import UploadFile, Depends
from app.core.storage import get_storage_client, StorageClient
from app.utils.image_processing import img_proc 
from app.repositories import image_repository
from app.models.image import Image, ImageModel



class ImageService:
    
    def __init__(self, 
                 storage_client: Annotated[StorageClient, Depends(get_storage_client)],
                 image_repo: image_repository):
        self.storage_client = storage_client
        self.image_repository = image_repo

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
            image_dto = Image(
            item_id=item_id,
            url=file_url,
            date_uploaded=datetime.now()
        )
            
            image_model = image_dto.to_model()
            await self.image_repository.add_image(image_model)
        
        finally:
            os.unlink(temp_path)
            
        return image_dto
            
       

    async def delete_image(self, url: str) -> bool:
        parts = url.split('/')
        bucket_name = parts[-2]
        file_id = parts[-1]
        storage_success = await self.storage_client.delete_file(bucket_name, file_id)
        repo_success = await self.image_repository.delete_image(url)
        
        return storage_success and repo_success