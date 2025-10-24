"""
Message Repository - Data Access Layer
Handles all database operations for messages and conversations using MongoDB
"""
from datetime import datetime
from typing import Optional, List
from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.database import Database
from pymongo.collection import Collection

from app.schemas.message import Message, Conversation, MessageStatus
from app.core.database import get_db


class MessageRepository:
    """
    Repository for message and conversation database operations with MongoDB
    
    Handles CRUD operations and queries for MongoDB database
    """
    
    def __init__(self, db: Database = None):
        """
        Initialize repository with MongoDB database
        
        Args:
            db: MongoDB database instance (optional, will use default if not provided)
        """
        self.db = db or get_db()
        self.messages: Collection = self.db.messages
        self.conversations: Collection = self.db.conversations
        
        # Create indexes for better query performance
        self._ensure_indexes()
    
    def _ensure_indexes(self):
        """Create necessary indexes for efficient queries"""
        # Message indexes
        self.messages.create_index("message_id", unique=True)
        self.messages.create_index("conversation_id")
        self.messages.create_index([("conversation_id", DESCENDING), ("created_at", DESCENDING)])
        self.messages.create_index("sender_id")
        self.messages.create_index("receiver_id")
        self.messages.create_index([("receiver_id", ASCENDING), ("status", ASCENDING)])
        self.messages.create_index([("content", "text")])  # Text index for search
        
        # Conversation indexes
        self.conversations.create_index("conversation_id", unique=True)
        self.conversations.create_index("participant_ids")
        self.conversations.create_index([("participant_ids", ASCENDING), ("last_message_at", DESCENDING)])
        self.conversations.create_index("item_id")
    
    # Message Operations
    
    async def create_message(self, message: Message) -> Message:
        """
        Create a new message in the database
        
        Args:
            message: Message domain model
            
        Returns:
            Created Message object
        """
        message_dict = message.to_dict()
        self.messages.insert_one(message_dict)
        return message
    
    async def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """
        Get a message by its ID
        
        Args:
            message_id: ID of the message
            
        Returns:
            Message object or None if not found
        """
        doc = self.messages.find_one({"message_id": message_id})
        
        if not doc:
            return None
        
        return Message.from_dict(doc)
    
    async def update_message(self, message: Message) -> Message:
        """
        Update an existing message
        
        Args:
            message: Message domain model with updated fields
            
        Returns:
            Updated Message object
        """
        self.messages.update_one(
            {"message_id": message.message_id},
            {
                "$set": {
                    "status": message.status.value,
                    "read_at": message.read_at,
                    "is_deleted": message.is_deleted,
                    "deleted_at": message.deleted_at,
                }
            }
        )
        
        return message
    
    async def get_messages_by_conversation(
        self,
        conversation_id: str,
        limit: int = 50,
        before_timestamp: Optional[datetime] = None
    ) -> List[Message]:
        """
        Get messages in a conversation with pagination
        
        Args:
            conversation_id: ID of the conversation
            limit: Maximum number of messages to return
            before_timestamp: Get messages before this timestamp
            
        Returns:
            List of Message objects ordered by created_at DESC
        """
        query = {"conversation_id": conversation_id}
        
        if before_timestamp:
            query["created_at"] = {"$lt": before_timestamp}
        
        cursor = self.messages.find(query).sort("created_at", DESCENDING).limit(limit)
        
        return [Message.from_dict(doc) for doc in cursor]
    
    async def get_unread_messages_in_conversation(
        self,
        conversation_id: str,
        user_id: str
    ) -> List[Message]:
        """
        Get all unread messages in a conversation where user is receiver
        
        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user (receiver)
            
        Returns:
            List of unread Message objects
        """
        query = {
            "conversation_id": conversation_id,
            "receiver_id": user_id,
            "status": {"$ne": MessageStatus.READ.value},
            "is_deleted": False
        }
        
        cursor = self.messages.find(query)
        
        return [Message.from_dict(doc) for doc in cursor]
    
    async def get_last_message_in_conversation(
        self,
        conversation_id: str
    ) -> Optional[Message]:
        """
        Get the most recent message in a conversation
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            Latest Message object or None
        """
        doc = self.messages.find_one(
            {"conversation_id": conversation_id, "is_deleted": False},
            sort=[("created_at", DESCENDING)]
        )
        
        if not doc:
            return None
        
        return Message.from_dict(doc)
    
    async def get_unread_count(self, user_id: str) -> int:
        """
        Get count of unread messages for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            Count of unread messages
        """
        count = self.messages.count_documents({
            "receiver_id": user_id,
            "status": {"$ne": MessageStatus.READ.value},
            "is_deleted": False
        })
        
        return count
    
    async def search_messages(
        self,
        user_id: str,
        query_text: str,
        limit: int = 50
    ) -> List[Message]:
        """
        Search messages by content where user is participant
        
        Args:
            user_id: ID of the user
            query_text: Search query
            limit: Maximum results
            
        Returns:
            List of matching Message objects
        """
        # Use MongoDB text search
        query = {
            "$text": {"$search": query_text},
            "$or": [
                {"sender_id": user_id},
                {"receiver_id": user_id}
            ],
            "is_deleted": False
        }
        
        cursor = self.messages.find(query).sort("created_at", DESCENDING).limit(limit)
        
        return [Message.from_dict(doc) for doc in cursor]
    
    async def delete_message(self, message_id: str) -> bool:
        """
        Permanently delete a message (use soft delete in practice)
        
        Args:
            message_id: ID of the message
            
        Returns:
            True if deleted successfully
        """
        result = self.messages.delete_one({"message_id": message_id})
        return result.deleted_count > 0
    
    # Conversation Operations
    
    async def create_conversation(self, conversation: Conversation) -> Conversation:
        """
        Create a new conversation
        
        Args:
            conversation: Conversation domain model
            
        Returns:
            Created Conversation object
        """
        conversation_dict = conversation.to_dict()
        self.conversations.insert_one(conversation_dict)
        return conversation
    
    async def get_conversation_by_id(
        self,
        conversation_id: str
    ) -> Optional[Conversation]:
        """
        Get a conversation by ID
        
        Args:
            conversation_id: ID of the conversation
            
        Returns:
            Conversation object or None
        """
        doc = self.conversations.find_one({"conversation_id": conversation_id})
        
        if not doc:
            return None
        
        return Conversation.from_dict(doc)
    
    async def update_conversation(self, conversation: Conversation) -> Conversation:
        """
        Update a conversation
        
        Args:
            conversation: Conversation domain model
            
        Returns:
            Updated Conversation object
        """
        self.conversations.update_one(
            {"conversation_id": conversation.conversation_id},
            {
                "$set": {
                    "last_message_at": conversation.last_message_at,
                    "last_message_content": conversation.last_message_content,
                    "is_archived": conversation.is_archived,
                    "unread_count": conversation.unread_count,
                }
            }
        )
        
        return conversation
    
    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 20,
        include_archived: bool = False
    ) -> List[Conversation]:
        """
        Get all conversations for a user
        
        Args:
            user_id: ID of the user
            limit: Maximum conversations to return
            include_archived: Whether to include archived conversations
            
        Returns:
            List of Conversation objects ordered by last_message_at DESC
        """
        query = {"participant_ids": user_id}
        
        if not include_archived:
            query["is_archived"] = False
        
        cursor = self.conversations.find(query).sort("last_message_at", DESCENDING).limit(limit)
        
        return [Conversation.from_dict(doc) for doc in cursor]
    
    async def find_conversation_between_users(
        self,
        user1_id: str,
        user2_id: str,
        item_id: Optional[str] = None
    ) -> Optional[Conversation]:
        """
        Find existing conversation between two users
        
        Args:
            user1_id: ID of first user
            user2_id: ID of second user
            item_id: Optional ID of related item
            
        Returns:
            Conversation object or None
        """
        query = {
            "participant_ids": {"$all": [user1_id, user2_id]}
        }
        
        if item_id:
            query["item_id"] = item_id
        
        doc = self.conversations.find_one(query)
        
        if not doc:
            return None
        
        return Conversation.from_dict(doc)
    
    async def mark_conversation_messages_as_read(
        self,
        conversation_id: str,
        user_id: str
    ) -> int:
        """
        Mark all unread messages in a conversation as read for a user
        
        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user
            
        Returns:
            Number of messages updated
        """
        result = self.messages.update_many(
            {
                "conversation_id": conversation_id,
                "receiver_id": user_id,
                "status": {"$ne": MessageStatus.READ.value}
            },
            {
                "$set": {
                    "status": MessageStatus.READ.value,
                    "read_at": datetime.utcnow()
                }
            }
        )
        
        # Update conversation unread count
        conversation = await self.get_conversation_by_id(conversation_id)
        if conversation:
            conversation.reset_unread_for_user(user_id)
            await self.update_conversation(conversation)
        
        return result.modified_count
    
    async def get_conversation_unread_count(
        self,
        conversation_id: str,
        user_id: str
    ) -> int:
        """
        Get unread message count for a specific conversation
        
        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user
            
        Returns:
            Count of unread messages
        """
        count = self.messages.count_documents({
            "conversation_id": conversation_id,
            "receiver_id": user_id,
            "status": {"$ne": MessageStatus.READ.value},
            "is_deleted": False
        })
        
        return count