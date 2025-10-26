"""Message Repository - Data Access Layer (ASYNC with Motor)"""
from typing import Optional, List
from pymongo import DESCENDING, ASCENDING
from motor.motor_asyncio import AsyncIOMotorDatabase
import logging

from app.schemas.message import Message, Conversation
from app.core.database import get_db

logger = logging.getLogger(__name__)

class MessageRepository:
    """Repository for message and conversation database operations (ASYNC)"""
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.db = db if db is not None else get_db()
        self.messages = self.db.messages
        self.conversations = self.db.conversations
    
    # ✅ ALL methods are now async
    async def create_message(self, message: Message) -> Message:
        """Create a new message"""
        message_dict = message.to_dict()
        await self.messages.insert_one(message_dict)  # ✅ await
        return message
    
    async def create_conversation(self, conversation: Conversation) -> Conversation:
        """Create a new conversation"""
        conv_dict = conversation.to_dict()
        await self.conversations.insert_one(conv_dict)  # ✅ await
        return conversation
    
    async def update_conversation(self, conversation: Conversation) -> Conversation:
        """Update an existing conversation"""
        conv_dict = conversation.to_dict()
        await self.conversations.update_one(  # ✅ await
            {"conversation_id": conversation.conversation_id},
            {"$set": conv_dict}
        )
        return conversation
    
    async def get_conversation_by_id(self, conversation_id: str) -> Optional[Conversation]:
        """Get conversation by ID"""
        conv_dict = await self.conversations.find_one({"conversation_id": conversation_id})  # ✅ await
        if conv_dict:
            return Conversation.from_dict(conv_dict)
        return None
    
    async def get_conversation_by_participants(self, participant_ids: List[str]) -> Optional[Conversation]:
        """Get conversation by participants"""
        # ✅ Use $all to find conversations with both participants
        conv_dict = await self.conversations.find_one({
            "participant_ids": {"$all": sorted(participant_ids)}
        })
        return Conversation.from_dict(conv_dict) if conv_dict else None
    
    async def get_user_conversations(
        self,
        user_id: str,
        include_archived: bool = False,
        limit: int = 20
    ) -> List[Conversation]:
        """Get all conversations for a user"""
        query = {"participant_ids": user_id}
        if not include_archived:
            query["is_archived"] = False
        
        cursor = self.conversations.find(query).sort("last_message_at", DESCENDING).limit(limit)
        conversations = []
        async for doc in cursor:  # ✅ async for
            conversations.append(Conversation.from_dict(doc))
        return conversations
    
    async def get_messages_by_conversation(
        self,
        conversation_id: str,
        limit: int = 50
    ) -> List[Message]:
        """Get messages in a conversation"""
        cursor = self.messages.find(
            {"conversation_id": conversation_id}
        ).sort("created_at", ASCENDING).limit(limit)
        
        messages = []
        async for doc in cursor:  # ✅ async for
            messages.append(Message.from_dict(doc))
        return messages
