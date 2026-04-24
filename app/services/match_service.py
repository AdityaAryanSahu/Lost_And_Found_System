from typing import List, Annotated
from app.models.match import MatchSearchRequest, MatchResponse, MatchList, MatchModel 
from app.models.item import ItemResponse
from app.services.item_service import ItemService 
from app.repositories import match_repository
from fastapi import Depends
from datetime import datetime
from app.services.noti_service import NotificationService
from app.repositories.user_repository import UserRepo


class MatchService:
    
    def __init__(self,
                 item_service: Annotated[ItemService, Depends()],
                 match_repo: match_repository.MatchRepo,
                notification_service: Annotated[NotificationService, Depends()]):
        self.item_service = item_service
        self.match_repository = match_repo
        self.notification_service = notification_service
        
    async def find_potential_matches(self, search_request: MatchSearchRequest) -> MatchList:
        
        all_items_list = await self.item_service.get_all_items(limit=1000, offset=0)
        all_items = all_items_list.item_list
        potential_matches: List[MatchResponse] = []

        search_keywords = {k.lower() for k in search_request.keywords}

        for item in all_items:
            if item.is_claimed:
                continue

            if item.post_type == search_request.post_type:
                continue 
                
            score = 0.0
            reasons = []

            #highest priority to the type match
            if item.type.lower() == search_request.search_type.lower():
                score += 0.5  # 50% score for exact type match
                reasons.append("Exact item type match.")

            #then desc match using keywords
            item_desc_words = set(item.desc.lower().split())
            common_keywords = search_keywords.intersection(item_desc_words)
            
            if common_keywords:
                keyword_score = len(common_keywords) / len(search_keywords)
                score += (keyword_score * 0.4) 
                reasons.append(f"Keyword overlap: {', '.join(common_keywords)}")
            
            #match the locatiom
            if search_request.location.lower() in item.desc.lower():
                 score += 0.1 # 10% score for location keyword in description
                 reasons.append("Location mentioned in description.")


            #filter and crate a response
            if score >= 0.5: 
                potential_matches.append(
                    MatchResponse(
                        matched_item=item,
                        item_id=item.item_id,
                        score=round(score, 2),
                        mssg=f"Score {round(score*100)}%. Reasons: {'; '.join(reasons)}"
                    )
                )

        potential_matches.sort(key=lambda m: m.score, reverse=True)

        return MatchList(
            matches=potential_matches,
            count=len(potential_matches)
        )
        
    async def run_automated_matching(self, new_item_id: str):
       
        new_item = await self.item_service.get_item_id(new_item_id)
        if not new_item:
            return

        all_items_list = await self.item_service.get_all_items(limit=1000, offset=0)
        all_items = all_items_list.item_list

        new_item_desc_words = set(new_item.desc.lower().split())

        for existing_item in all_items:
            if existing_item.item_id == new_item.item_id or existing_item.is_claimed:
                continue

            score = 0.0

            #type Match
            if existing_item.type.lower() == new_item.type.lower():
                score += 0.5 

            #keyword Match
            existing_item_desc_words = set(existing_item.desc.lower().split())
            common_keywords = new_item_desc_words.intersection(existing_item_desc_words)
            
            if common_keywords and new_item_desc_words:
                min_len = min(len(new_item_desc_words), len(existing_item_desc_words))
                keyword_score = len(common_keywords) / min_len
                score += (keyword_score * 0.4) 
                
            print(f"in automanted matching ofund score: {score}")

            if score >= 0.65:
                match_data = MatchModel(
                    item_id_a=new_item.item_id,
                    item_id_b=existing_item.item_id,
                    score=round(score, 2),
                    matched_at=datetime.now()
                )
                await self.match_repository.add_match(match_data)
                await self.notification_service.notify_match_found(new_item.user_id, new_item.type, score)
                await self.notification_service.notify_match_found(existing_item.user_id, existing_item.type, score)
                

    async def get_saved_matches(self, item_id: str):
        return await self.match_repository.get_match_by_item(item_id)