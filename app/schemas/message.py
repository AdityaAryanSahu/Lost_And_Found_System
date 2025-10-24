"""
Domain Model for Message Entity
Represents a message in the messaging system between users
"""
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4
from enum import Enum


class MessageStatus(str, Enum):
    """Message delivery status"""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"


class Message:
    """
    Message domain model representing a message between users
    
    Attributes:
        message_id: Unique identifier for the message
        conversation_id: ID linking messages in the same conversation
        sender_id: UUID of the user sending the message
        receiver_id: UUID of the user receiving the message
        item_id: Optional UUID of the item being discussed
        content: Text content of the message
        status: Current status of the message (sent/delivered/read)
        created_at: Timestamp when message was created
        read_at: Optional timestamp when message was read
        is_deleted: Soft delete flag
        deleted_at: Optional timestamp when message was deleted
    """
    
    def __init__(
        self,
        sender_id: str,
        receiver_id: str,
        content: str,
        message_id: Optional[str] = None,
        conversation_id: Optional[str] = None,
        item_id: Optional[str] = None,
        status: MessageStatus = MessageStatus.SENT,
        created_at: Optional[datetime] = None,
        read_at: Optional[datetime] = None,
        is_deleted: bool = False,
        deleted_at: Optional[datetime] = None,
    ):
        self.message_id = message_id or str(uuid4())
        self.conversation_id = conversation_id or self._generate_conversation_id(sender_id, receiver_id, item_id)
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.item_id = item_id
        self.content = content
        self.status = status
        self.created_at = created_at or datetime.utcnow()
        self.read_at = read_at
        self.is_deleted = is_deleted
        self.deleted_at = deleted_at
    
    def mark_as_read(self) -> None:
        """Mark message as read with current timestamp"""
        self.status = MessageStatus.READ
        self.read_at = datetime.utcnow()
    
    def mark_as_delivered(self) -> None:
        """Mark message as delivered"""
        if self.status == MessageStatus.SENT:
            self.status = MessageStatus.DELIVERED
    
    def soft_delete(self) -> None:
        """Soft delete the message"""
        self.is_deleted = True
        self.deleted_at = datetime.utcnow()
    
    def to_dict(self) -> dict:
        """Convert message to dictionary representation for MongoDB"""
        return {
            "_id": self.message_id,
            "message_id": self.message_id,
            "conversation_id": self.conversation_id,
            "sender_id": self.sender_id,
            "receiver_id": self.receiver_id,
            "item_id": self.item_id,
            "content": self.content,
            "status": self.status.value,
            "created_at": self.created_at,
            "read_at": self.read_at,
            "is_deleted": self.is_deleted,
            "deleted_at": self.deleted_at,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Message":
        """Create Message instance from dictionary (MongoDB document)"""
        return cls(
            message_id=data.get("message_id") or data.get("_id"),
            conversation_id=data.get("conversation_id"),
            sender_id=data["sender_id"],
            receiver_id=data["receiver_id"],
            item_id=data.get("item_id"),
            content=data["content"],
            status=MessageStatus(data.get("status", MessageStatus.SENT.value)),
            created_at=data.get("created_at"),
            read_at=data.get("read_at"),
            is_deleted=data.get("is_deleted", False),
            deleted_at=data.get("deleted_at"),
        )
    
    @staticmethod
    def _generate_conversation_id(sender_id: str, receiver_id: str, item_id: Optional[str] = None) -> str:
        """Generate a consistent conversation ID for two users"""
        # Sort user IDs to ensure same conversation_id regardless of who initiates
        user_ids = sorted([sender_id, receiver_id])
        if item_id:
            return f"{user_ids[0]}_{user_ids[1]}_{item_id}"
        return f"{user_ids[0]}_{user_ids[1]}"
    
    def __repr__(self) -> str:
        return f"<Message {self.message_id} from {self.sender_id} to {self.receiver_id}>"
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Message):
            return False
        return self.message_id == other.message_id


class Conversation:
    """
    Conversation domain model representing a thread of messages
    
    Attributes:
        conversation_id: Unique identifier for the conversation
        participant_ids: Set of user IDs participating in conversation
        item_id: Optional UUID of the item being discussed
        last_message_at: Timestamp of the last message
        last_message_content: Preview of the last message
        created_at: Timestamp when conversation was created
        is_archived: Whether conversation is archived
        unread_count: Count of unread messages per user
    """
    
    def __init__(
        self,
        participant_ids: set[str],
        conversation_id: Optional[str] = None,
        item_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        last_message_at: Optional[datetime] = None,
        last_message_content: Optional[str] = None,
        is_archived: bool = False,
        unread_count: Optional[dict[str, int]] = None,
    ):
        self.conversation_id = conversation_id or str(uuid4())
        self.participant_ids = participant_ids
        self.item_id = item_id
        self.last_message_at = last_message_at or created_at or datetime.utcnow()
        self.last_message_content = last_message_content
        self.created_at = created_at or datetime.utcnow()
        self.is_archived = is_archived
        self.unread_count = unread_count or {pid: 0 for pid in participant_ids}
    
    def update_last_message(self, content: str, timestamp: datetime) -> None:
        """Update the last message timestamp and content"""
        self.last_message_at = timestamp
        self.last_message_content = content
    
    def increment_unread_for_user(self, user_id: str) -> None:
        """Increment unread count for a specific user"""
        if user_id in self.unread_count:
            self.unread_count[user_id] += 1
        else:
            self.unread_count[user_id] = 1
    
    def reset_unread_for_user(self, user_id: str) -> None:
        """Reset unread count for a specific user"""
        self.unread_count[user_id] = 0
    
    def archive(self) -> None:
        """Archive the conversation"""
        self.is_archived = True
    
    def unarchive(self) -> None:
        """Unarchive the conversation"""
        self.is_archived = False
    
    def has_participant(self, user_id: str) -> bool:
        """Check if user is a participant in this conversation"""
        return user_id in self.participant_ids
    
    def get_other_participant(self, user_id: str) -> Optional[str]:
        """Get the other participant's ID in a two-person conversation"""
        others = self.participant_ids - {user_id}
        return next(iter(others)) if others else None
    
    def to_dict(self) -> dict:
        """Convert conversation to dictionary representation for MongoDB"""
        return {
            "_id": self.conversation_id,
            "conversation_id": self.conversation_id,
            "participant_ids": list(self.participant_ids),
            "item_id": self.item_id,
            "last_message_at": self.last_message_at,
            "last_message_content": self.last_message_content,
            "created_at": self.created_at,
            "is_archived": self.is_archived,
            "unread_count": self.unread_count,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Conversation":
        """Create Conversation instance from dictionary (MongoDB document)"""
        return cls(
            conversation_id=data.get("conversation_id") or data.get("_id"),
            participant_ids=set(data["participant_ids"]),
            item_id=data.get("item_id"),
            created_at=data.get("created_at"),
            last_message_at=data.get("last_message_at"),
            last_message_content=data.get("last_message_content"),
            is_archived=data.get("is_archived", False),
            unread_count=data.get("unread_count", {}),
        )
    
    def __repr__(self) -> str:
        return f"<Conversation {self.conversation_id} with {len(self.participant_ids)} participants>"