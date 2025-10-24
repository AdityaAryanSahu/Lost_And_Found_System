"""
Messages API Endpoints
Handles HTTP requests for messaging functionality
"""
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import JSONResponse

from app.models.message import (
    MessageCreate,
    MessageResponse,
    ConversationResponse,
    ConversationListResponse,
    MessageListResponse,
    UnreadCountResponse
)
from app.services.message_service import MessageService
from app.core.exceptions import (
    NotFoundException,
    ForbiddenException,
    ValidationException
)
from app.api.dependencies import (
    get_current_user,
    get_message_service
)
from app.schemas.user import UserModel


router = APIRouter(prefix="/messages", tags=["messages"])


@router.post(
    "/send",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Send a message"
)
async def send_message(
    message_data: MessageCreate,
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> MessageResponse:
    """
    Send a message to another user
    
    - **receiver_id**: UUID of the user to send message to
    - **content**: Text content of the message
    - **item_id**: Optional UUID of the item being discussed
    """
    try:
        message = await message_service.send_message(
            sender_id=current_user.user_id,
            receiver_id=message_data.receiver_id,
            content=message_data.content,
            item_id=message_data.item_id
        )
        
        return MessageResponse.from_domain(message)
    
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send message"
        )


@router.get(
    "/conversations",
    response_model=ConversationListResponse,
    summary="Get user conversations"
)
async def get_conversations(
    include_archived: bool = Query(False, description="Include archived conversations"),
    limit: int = Query(20, ge=1, le=100, description="Number of conversations to return"),
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> ConversationListResponse:
    """
    Get all conversations for the current user
    
    Returns list of conversations with last message preview
    """
    try:
        conversations_with_messages = await message_service.get_user_conversations(
            user_id=current_user.user_id,
            limit=limit,
            include_archived=include_archived
        )
        
        conversations = [
            ConversationResponse.from_domain(conv, last_msg)
            for conv, last_msg in conversations_with_messages
        ]
        
        return ConversationListResponse(
            conversations=conversations,
            total=len(conversations)
        )
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@router.get(
    "/conversations/{conversation_id}",
    response_model=MessageListResponse,
    summary="Get messages in a conversation"
)
async def get_conversation_messages(
    conversation_id: str,
    limit: int = Query(50, ge=1, le=100, description="Number of messages to return"),
    before: Optional[datetime] = Query(None, description="Get messages before this timestamp"),
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> MessageListResponse:
    """
    Get all messages in a specific conversation
    
    Supports pagination using the 'before' parameter
    """
    try:
        messages = await message_service.get_conversation_messages(
            conversation_id=conversation_id,
            user_id=current_user.user_id,
            limit=limit,
            before_timestamp=before
        )
        
        return MessageListResponse(
            messages=[MessageResponse.from_domain(msg) for msg in messages],
            total=len(messages),
            has_more=len(messages) == limit
        )
    
    except ForbiddenException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages"
        )


@router.get(
    "/{message_id}",
    response_model=MessageResponse,
    summary="Get a specific message"
)
async def get_message(
    message_id: str,
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> MessageResponse:
    """
    Get a specific message by ID
    """
    try:
        message = await message_service.get_message(
            message_id=message_id,
            user_id=current_user.user_id
        )
        
        return MessageResponse.from_domain(message)
    
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ForbiddenException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.patch(
    "/{message_id}/read",
    response_model=MessageResponse,
    summary="Mark message as read"
)
async def mark_message_as_read(
    message_id: str,
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> MessageResponse:
    """
    Mark a message as read (only receiver can do this)
    """
    try:
        message = await message_service.mark_message_as_read(
            message_id=message_id,
            user_id=current_user.user_id
        )
        
        return MessageResponse.from_domain(message)
    
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ForbiddenException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.patch(
    "/conversations/{conversation_id}/read",
    summary="Mark all messages in conversation as read"
)
async def mark_conversation_as_read(
    conversation_id: str,
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> JSONResponse:
    """
    Mark all unread messages in a conversation as read
    """
    try:
        count = await message_service.mark_conversation_as_read(
            conversation_id=conversation_id,
            user_id=current_user.user_id
        )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Marked {count} messages as read",
                "count": count
            }
        )
    
    except ForbiddenException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete(
    "/{message_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a message"
)
async def delete_message(
    message_id: str,
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
):
    """
    Delete a message (soft delete, only sender can delete)
    """
    try:
        await message_service.delete_message(
            message_id=message_id,
            user_id=current_user.user_id
        )
        
        return None
    
    except NotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ForbiddenException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get(
    "/unread/count",
    response_model=UnreadCountResponse,
    summary="Get unread message count"
)
async def get_unread_count(
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> UnreadCountResponse:
    """
    Get the count of unread messages for the current user
    """
    try:
        count = await message_service.get_unread_count(current_user.user_id)
        
        return UnreadCountResponse(unread_count=count)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get unread count"
        )


@router.patch(
    "/conversations/{conversation_id}/archive",
    response_model=ConversationResponse,
    summary="Archive a conversation"
)
async def archive_conversation(
    conversation_id: str,
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> ConversationResponse:
    """
    Archive a conversation
    """
    try:
        conversation = await message_service.archive_conversation(
            conversation_id=conversation_id,
            user_id=current_user.user_id
        )
        
        return ConversationResponse.from_domain(conversation, None)
    
    except ForbiddenException as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get(
    "/search",
    response_model=MessageListResponse,
    summary="Search messages"
)
async def search_messages(
    q: str = Query(..., min_length=2, description="Search query"),
    limit: int = Query(50, ge=1, le=100, description="Number of results to return"),
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> MessageListResponse:
    """
    Search messages by content
    
    Searches through all messages where the current user is a participant
    """
    try:
        messages = await message_service.search_messages(
            user_id=current_user.user_id,
            query=q,
            limit=limit
        )
        
        return MessageListResponse(
            messages=[MessageResponse.from_domain(msg) for msg in messages],
            total=len(messages),
            has_more=False
        )
    
    except ValidationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search messages"
        )