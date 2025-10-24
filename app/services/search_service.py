from typing import List, Annotated
from fastapi import Depends
from app.models.search import SearchRequest
from app.models.item import ItemList, ItemResponse
from app.services.item_service import ItemService 

class SearchService:
    
    def __init__(self, item_service: Annotated[ItemService, Depends()]):
        self.item_service = item_service

    async def search_items(self, search_request: SearchRequest) -> ItemList:
       
        
        all_items = await self.item_service.get_all_items(limit=1000, offset=0)
        filtered_items: List[ItemResponse] = []
        
        for item in all_items.items:
            
            if search_request.is_claimed is not None and item.is_claimed != search_request.is_claimed:
                continue

          
            if search_request.item_type and item.type.lower() != search_request.item_type.lower():
                continue

            if search_request.query:
                query_lower = search_request.query.lower()
                if not (query_lower in item.desc.lower() or query_lower in item.type.lower()):
                    continue
            
           
            if search_request.date_from and item.created_at < search_request.date_from:
                continue

            filtered_items.append(item)
            
     
        start = search_request.offset
        end = search_request.offset + search_request.limit
        paginated_items = filtered_items[start:end]

        return ItemList(
            items=paginated_items,
            count=len(filtered_items)
        )