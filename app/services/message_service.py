"""
Message Service - Business Logic Layer
Handles messaging operations, conversation management, and business rules
"""
from datetime import datetime
from typing import Optional, List, Tuple

from app.models.message import Message, Conversation, MessageStatus
from app.repositories.message_repository import MessageRepository
from app.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    ValidationException
)
from app.core.cache import cache_manager


class MessageService:
    """
    Service class for managing messages and conversations
    
    Handles business logic for:
    - Sending messages
    - Reading messages
    - Managing conversations
    - Message validation
    """
    
    def __init__(self, message_repository: MessageRepository):
        """
        Initialize MessageService with repository
        
        Args:
            message_repository: Repository for message data access
        """
        self.message_repo = message_repository
    
    async def send_message(
        self,
        sender_id: str,
        receiver_id: str,
        content: str,
        item_id: Optional[str] = None
    ) -> Message:
        """
        Send a message from one user to another
        
        Args:
            sender_id: ID of the sender
            receiver_id: ID of the receiver
            content: Message content
            item_id: Optional ID of related item
            
        Returns:
            Created Message object
            
        Raises:
            ValidationException: If message content is invalid
        """
        # Validate message content
        self._validate_message_content(content)
        
        # Check if sender is trying to message themselves
        if sender_id == receiver_id:
            raise ValidationException("Cannot send message to yourself")
        
        # Get or create conversation
        conversation = await self._get_or_create_conversation(
            sender_id, receiver_id, item_id
        )
        
        # Create message
        message = Message(
            sender_id=sender_id,
            receiver_id=receiver_id,
            content=content,
            conversation_id=conversation.conversation_id,
            item_id=item_id,
            status=MessageStatus.SENT,
        )
        
        # Save message to database
        await self.message_repo.create_message(message)
        
        # Update conversation last message time and increment unread count
        conversation.update_last_message(content, message.created_at)
        conversation.increment_unread_for_user(receiver_id)
        await self.message_repo.update_conversation(conversation)
        
        # Invalidate conversation cache
        await self._invalidate_conversation_cache(sender_id, receiver_id)
        
        return message
    
    async def get_message(self, message_id: str, user_id: str) -> Message:
        """
        Get a specific message by ID
        
        Args:
            message_id: ID of the message
            user_id: ID of the requesting user
            
        Returns:
            Message object
            
        Raises:
            NotFoundException: If message not found
            ForbiddenException: If user is not a participant
        """
        message = await self.message_repo.get_message_by_id(message_id)
        
        if not message:
            raise NotFoundException(f"Message {message_id} not found")
        
        # Check if user is sender or receiver
        if user_id not in [message.sender_id, message.receiver_id]:
            raise ForbiddenException("You are not authorized to view this message")
        
        return message
    
    async def get_conversation_messages(
        self,
        conversation_id: str,
        user_id: str,
        limit: int = 50,
        before_timestamp: Optional[datetime] = None
    ) -> List[Message]:
        """
        Get messages in a conversation with pagination
        
        Args:
            conversation_id: ID of the conversation
            user_id: ID of the requesting user
            limit: Maximum number of messages to return
            before_timestamp: Get messages before this timestamp (for pagination)
            
        Returns:
            List of Message objects
            
        Raises:
            ForbiddenException: If user is not a participant
        """
        # Verify user is participant in conversation
        conversation = await self.message_repo.get_conversation_by_id(conversation_id)
        if not conversation or not conversation.has_participant(user_id):
            raise ForbiddenException("You are not a participant in this conversation")
        
        # Get messages
        messages = await self.message_repo.get_messages_by_conversation(
            conversation_id,
            limit=limit,
            before_timestamp=before_timestamp
        )
        
        return messages
    
    async def get_user_conversations(
        self,
        user_id: str,
        limit: int = 20,
        include_archived: bool = False
    ) -> List[Tuple[Conversation, Optional[Message]]]:
        """
        Get all conversations for a user with last message preview
        
        Args:
            user_id: ID of the user
            limit: Maximum number of conversations to return
            include_archived: Whether to include archived conversations
            
        Returns:
            List of tuples (Conversation, last_message)
        """
        # Try cache first
        cache_key = f"user_conversations:{user_id}:{include_archived}"
        cached = await cache_manager.get(cache_key)
        if cached:
            return cached
        
        # Get conversations from repository
        conversations = await self.message_repo.get_user_conversations(
            user_id,
            limit=limit,
            include_archived=include_archived
        )
        
        # Get last message for each conversation
        result = []
        for conversation in conversations:
            last_message = await self.message_repo.get_last_message_in_conversation(
                conversation.conversation_id
            )
            result.append((conversation, last_message))
        
        # Cache for 5 minutes
        await cache_manager.set(cache_key, result, ttl=300)
        
        return result
    
    async def mark_message_as_read(
        self,
        message_id: str,
        user_id: str
    ) -> Message:
        """
        Mark a message as read
        
        Args:
            message_id: ID of the message
            user_id: ID of the user (must be receiver)
            
        Returns:
            Updated Message object
            
        Raises:
            ForbiddenException: If user is not the receiver
        """
        message = await self.get_message(message_id, user_id)
        
        # Only receiver can mark as read
        if message.receiver_id != user_id:
            raise ForbiddenException("Only the receiver can mark message as read")
        
        # If already read, return as is
        if message.status == MessageStatus.READ:
            return message
        
        # Mark as read
        message.mark_as_read()
        await self.message_repo.update_message(message)
        
        # Update conversation unread count
        conversation = await self.message_repo.get_conversation_by_id(message.conversation_id)
        if conversation and user_id in conversation.unread_count:
            if conversation.unread_count[user_id] > 0:
                conversation.unread_count[user_id] -= 1
                await self.message_repo.update_conversation(conversation)
        
        return message
    
    async def mark_conversation_as_read(
        self,
        conversation_id: str,
        user_id: str
    ) -> int:
        """
        Mark all unread messages in a conversation as read
        
        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user
            
        Returns:
            Number of messages marked as read
        """
        # Verify user is participant
        conversation = await self.message_repo.get_conversation_by_id(conversation_id)
        if not conversation or not conversation.has_participant(user_id):
            raise ForbiddenException("You are not a participant in this conversation")
        
        # Mark all messages as read
        count = await self.message_repo.mark_conversation_messages_as_read(
            conversation_id, user_id
        )
        
        # Invalidate cache
        await self._invalidate_conversation_cache(user_id)
        
        return count
    
    async def delete_message(
        self,
        message_id: str,
        user_id: str
    ) -> bool:
        """
        Soft delete a message (only sender can delete)
        
        Args:
            message_id: ID of the message
            user_id: ID of the user
            
        Returns:
            True if deleted successfully
            
        Raises:
            ForbiddenException: If user is not the sender
        """
        message = await self.get_message(message_id, user_id)
        
        # Only sender can delete
        if message.sender_id != user_id:
            raise ForbiddenException("Only the sender can delete their message")
        
        message.soft_delete()
        await self.message_repo.update_message(message)
        
        return True
    
    async def get_unread_count(self, user_id: str) -> int:
        """
        Get count of unread messages for a user
        
        Args:
            user_id: ID of the user
            
        Returns:
            Count of unread messages
        """
        # Try cache first
        cache_key = f"unread_count:{user_id}"
        cached = await cache_manager.get(cache_key)
        if cached is not None:
            return cached
        
        count = await self.message_repo.get_unread_count(user_id)
        
        # Cache for 1 minute
        await cache_manager.set(cache_key, count, ttl=60)
        
        return count
    
    async def archive_conversation(
        self,
        conversation_id: str,
        user_id: str
    ) -> Conversation:
        """
        Archive a conversation
        
        Args:
            conversation_id: ID of the conversation
            user_id: ID of the user
            
        Returns:
            Updated Conversation object
            
        Raises:
            ForbiddenException: If user is not a participant
        """
        conversation = await self.message_repo.get_conversation_by_id(conversation_id)
        
        if not conversation or not conversation.has_participant(user_id):
            raise ForbiddenException("You are not a participant in this conversation")
        
        conversation.archive()
        await self.message_repo.update_conversation(conversation)
        
        # Invalidate cache
        await self._invalidate_conversation_cache(user_id)
        
        return conversation
    
    async def search_messages(
        self,
        user_id: str,
        query: str,
        limit: int = 50
    ) -> List[Message]:
        """
        Search messages by content
        
        Args:
            user_id: ID of the user
            query: Search query string
            limit: Maximum number of results
            
        Returns:
            List of matching messages
        """
        if not query or len(query.strip()) < 2:
            raise ValidationException("Search query must be at least 2 characters")
        
        return await self.message_repo.search_messages(user_id, query, limit)
    
    # Private helper methods
    
    def _validate_message_content(self, content: str) -> None:
        """Validate message content"""
        if not content or not content.strip():
            raise ValidationException("Message content cannot be empty")
        
        if len(content) > 5000:
            raise ValidationException("Message content too long (max 5000 characters)")
    
    async def _get_or_create_conversation(
        self,
        user1_id: str,
        user2_id: str,
        item_id: Optional[str] = None
    ) -> Conversation:
        """Get existing conversation or create new one"""
        # Try to find existing conversation
        conversation = await self.message_repo.find_conversation_between_users(
            user1_id, user2_id, item_id
        )
        
        if conversation:
            return conversation
        
        # Create new conversation
        conversation = Conversation(
            participant_ids={user1_id, user2_id},
            item_id=item_id,
        )
        
        await self.message_repo.create_conversation(conversation)
        
        return conversation
    
    async def _invalidate_conversation_cache(self, *user_ids: str) -> None:
        """Invalidate conversation-related caches for users"""
        for user_id in user_ids:
            await cache_manager.delete(f"user_conversations:{user_id}:True")
            await cache_manager.delete(f"user_conversations:{user_id}:False")
            await cache_manager.delete(f"unread_count:{user_id}")