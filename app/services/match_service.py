from typing import List, Annotated
from app.models.match import MatchSearchRequest, MatchResponse, MatchList, MatchModel 
from app.models.item import ItemResponse
from app.services.item_service import ItemService 
from app.repositories import match_repository
from fastapi import Depends
from datetime import datetime


class MatchService:
    
    def __init__(self,
                 item_service: Annotated[ItemService, Depends()],
                 match_repo: match_repository):
        self.item_service = item_service
        self.match_repository = match_repo
        
    async def find_potential_matches(self, search_request: MatchSearchRequest) -> MatchList:
        
        all_items_list = await self.item_service.get_all_items(limit=1000, offset=0)
        all_items = all_items_list.items 
        potential_matches: List[MatchResponse] = []

        search_keywords = {k.lower() for k in search_request.keywords}

        for item in all_items:
            if item.is_claimed:
                continue

            score = 0.0
            reasons = []

            # 1. Type Match (Highest priority)
            if item.type.lower() == search_request.search_type.lower():
                score += 0.5  # 50% score for exact type match
                reasons.append("Exact item type match.")

            # 2. Keyword Match (from description)
            item_desc_words = set(item.desc.lower().split())
            common_keywords = search_keywords.intersection(item_desc_words)
            
            if common_keywords:
                # Add score based on the proportion of search keywords found
                keyword_score = len(common_keywords) / len(search_keywords)
                score += (keyword_score * 0.4) # Up to 40% score for keyword overlap
                reasons.append(f"Keyword overlap: {', '.join(common_keywords)}")
            
            # 3. Location Match (Simplified mock)
            if search_request.location.lower() in item.desc.lower():
                 score += 0.1 # 10% score for location keyword in description
                 reasons.append("Location mentioned in description.")


            # 4. Filter and Finalize
            if score >= 0.5: # Only return matches with 50% score or higher
                potential_matches.append(
                    MatchResponse(
                        matched_item=item,
                        score=round(score, 2),
                        mssg=f"Score {round(score*100)}%. Reasons: {'; '.join(reasons)}"
                    )
                )

        # Sort by score descending
        potential_matches.sort(key=lambda m: m.score, reverse=True)

        return MatchList(
            matches=potential_matches,
            count=len(potential_matches)
        )