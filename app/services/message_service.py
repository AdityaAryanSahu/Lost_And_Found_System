"""Message Service - Business Logic Layer (ASYNC)"""
from datetime import datetime
from typing import Optional
import uuid
import logging

from app.schemas.message import Message, Conversation, MessageStatus
from app.repositories.message_repository import MessageRepository

logger = logging.getLogger(__name__)

class MessageService:
    """Service class for managing messages and conversations (ASYNC)"""
    
    def __init__(self, message_repository: MessageRepository):
        self.message_repo = message_repository
    
    async def send_message(
    self,
    sender_id: str,
    receiver_id: str,
    content: str,
    item_id: Optional[str] = None
) -> Message:
        """Send a message"""
        if not content or not content.strip():
            raise ValueError("Message content cannot be empty")
        
        if sender_id == receiver_id:
            raise ValueError("Cannot send message to yourself")
        
        conversation = await self._get_or_create_conversation(sender_id, receiver_id, item_id)
        
        message = Message(
            message_id=str(uuid.uuid4()),
            conversation_id=conversation.conversation_id,
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content.strip(),
            item_id=item_id,
            status=MessageStatus.SENT,
            created_at=datetime.utcnow()
        )
        
        await self.message_repo.create_message(message)
        
        # Use conversation's built-in methods
        conversation.update_last_message(content[:100], message.created_at)
        conversation.increment_unread_for_user(receiver_id)
        
        await self.message_repo.update_conversation(conversation)
        
        return message

    
    async def _get_or_create_conversation(
    self,
    user1_id: str,
    user2_id: str,
    item_id: Optional[str] = None
) -> Conversation:
        """Get existing conversation or create new one"""
        participant_ids = sorted([user1_id, user2_id])
        conversation = await self.message_repo.get_conversation_by_participants(participant_ids)
        
        if not conversation:
            # Pass participant_ids as a SET, not list
            conversation = Conversation(
                participant_ids=set([user1_id, user2_id]),  # Convert to set
                conversation_id=str(uuid.uuid4()),
                item_id=item_id,
                created_at=datetime.utcnow(),
                last_message_at=datetime.utcnow(),
                last_message_content=None,
                is_archived=False,
                unread_count={}  #This is now in __init__
            )
            await self.message_repo.create_conversation(conversation)
        
        return conversation

    
    async def get_user_conversations(self, user_id: str, include_archived: bool = False, limit: int = 20):
        return await self.message_repo.get_user_conversations(user_id, include_archived, limit)  #  await
    
    async def get_conversation(self, conversation_id: str):
        return await self.message_repo.get_conversation_by_id(conversation_id)  #  await
    
    async def get_conversation_messages(self, conversation_id: str, limit: int = 50):
        return await self.message_repo.get_messages_by_conversation(conversation_id, limit)  #  await
    
    async def mark_conversation_as_read(self, conversation_id: str, user_id: str):
        conversation = await self.get_conversation(conversation_id)  #  await
        if user_id in conversation.unread_count:
            conversation.unread_count[user_id] = 0
            await self.message_repo.update_conversation(conversation)  #  await
