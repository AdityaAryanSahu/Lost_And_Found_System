"""
Pydantic Schemas for Message API
Data Transfer Objects for request/response validation
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, field_validator

from app.schemas.message import Message, Conversation, MessageStatus


# Request Schemas

class MessageCreate(BaseModel):
    """Schema for creating a new message"""
    receiver_id: str = Field(..., description="ID of the message receiver")
    content: str = Field(..., min_length=1, max_length=5000, description="Message content")
    item_id: Optional[str] = Field(None, description="Optional ID of related item")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Message content cannot be empty")
        return v.strip()
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "receiver_id": "507f1f77bcf86cd799439011",
                "content": "Hi, I found your lost item!",
                "item_id": "507f1f77bcf86cd799439012"
            }
        }
    }


# Response Schemas

class MessageResponse(BaseModel):
    """Schema for message response"""
    message_id: str
    conversation_id: str
    sender_id: str
    receiver_id: str
    item_id: Optional[str]
    content: str
    status: MessageStatus
    created_at: datetime
    read_at: Optional[datetime]
    is_deleted: bool
    
    @classmethod
    def from_domain(cls, message: Message) -> "MessageResponse":
        """Create response from domain model"""
        return cls(
            message_id=message.message_id,
            conversation_id=message.conversation_id,
            sender_id=message.sender_id,
            receiver_id=message.receiver_id,
            item_id=message.item_id,
            content=message.content if not message.is_deleted else "[Message deleted]",
            status=message.status,
            created_at=message.created_at,
            read_at=message.read_at,
            is_deleted=message.is_deleted,
        )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "message_id": "507f1f77bcf86cd799439011",
                "conversation_id": "507f1f77bcf86cd799439012",
                "sender_id": "507f1f77bcf86cd799439013",
                "receiver_id": "507f1f77bcf86cd799439014",
                "item_id": "507f1f77bcf86cd799439015",
                "content": "Hi, I found your lost item!",
                "status": "sent",
                "created_at": "2024-01-15T10:30:00Z",
                "read_at": None,
                "is_deleted": False
            }
        }
    }


class ConversationResponse(BaseModel):
    """Schema for conversation response with optional last message"""
    conversation_id: str
    participant_ids: List[str]
    item_id: Optional[str]
    last_message_at: datetime
    created_at: datetime
    is_archived: bool
    last_message: Optional[MessageResponse]
    unread_count: int = 0
    
    @classmethod
    def from_domain(
        cls, 
        conversation: Conversation, 
        last_message: Optional[Message] = None
    ) -> "ConversationResponse":
        """Create response from domain model"""
        return cls(
            conversation_id=conversation.conversation_id,
            participant_ids=list(conversation.participant_ids),
            item_id=conversation.item_id,
            last_message_at=conversation.last_message_at,
            created_at=conversation.created_at,
            is_archived=conversation.is_archived,
            last_message=MessageResponse.from_domain(last_message) if last_message else None,
        )
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "conversation_id": "507f1f77bcf86cd799439011",
                "participant_ids": [
                    "507f1f77bcf86cd799439012",
                    "507f1f77bcf86cd799439013"
                ],
                "item_id": "507f1f77bcf86cd799439014",
                "last_message_at": "2024-01-15T10:30:00Z",
                "created_at": "2024-01-15T09:00:00Z",
                "is_archived": False,
                "last_message": {
                    "message_id": "507f1f77bcf86cd799439015",
                    "content": "Thanks for letting me know!",
                    "status": "read"
                },
                "unread_count": 2
            }
        }
    }


class MessageListResponse(BaseModel):
    """Schema for paginated message list"""
    messages: List[MessageResponse]
    total: int
    has_more: bool = False
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "messages": [],
                "total": 25,
                "has_more": True
            }
        }
    }


class ConversationListResponse(BaseModel):
    """Schema for conversation list"""
    conversations: List[ConversationResponse]
    total: int
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "conversations": [],
                "total": 5
            }
        }
    }


class UnreadCountResponse(BaseModel):
    """Schema for unread message count"""
    unread_count: int = Field(..., ge=0, description="Number of unread messages")
    
    model_config = {
        "json_schema_extra": {
            "example": {
                "unread_count": 3
            }
        }
    }