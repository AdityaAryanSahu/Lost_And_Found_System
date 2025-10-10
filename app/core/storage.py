
from typing import Optional, Dict
from fastapi import UploadFile

MOCK_STORAGE: Dict[str, Dict[str, bytes]] = {
    "lost-and-found-items": {},
    "user-avatars": {}
}


class StorageClient:
    """
    Simulates a MinIO/S3 storage client wrapper.
    In a real app, this would use the minio library.
    """
    
    async def upload_file(self, bucket_name: str, file_id: str, file_content: bytes) -> str:
        """Mocks uploading a file and returns the file URL."""
        
        if bucket_name not in MOCK_STORAGE:
            MOCK_STORAGE[bucket_name] = {}
            
        MOCK_STORAGE[bucket_name][file_id] = file_content
        
        # Returns a mock URL
        return f"http://minio.local/{bucket_name}/{file_id}"

    async def get_file(self, bucket_name: str, file_id: str) -> Optional[bytes]:
        """Mocks retrieving file content."""
        return MOCK_STORAGE.get(bucket_name, {}).get(file_id)

    async def delete_file(self, bucket_name: str, file_id: str) -> bool:
        """Mocks deleting a file."""
        if bucket_name in MOCK_STORAGE and file_id in MOCK_STORAGE[bucket_name]:
            del MOCK_STORAGE[bucket_name][file_id]
            return True
        return False

# Dependency to access the storage client
def get_storage_client() -> StorageClient:
    return StorageClient()