"""Messages API Endpoints"""
from fastapi import APIRouter, Depends, HTTPException, Query, status
import logging

from app.models.message import (
    MessageCreate,
    MessageResponse,
    ConversationResponse,
    ConversationListResponse,
    MessageListResponse
)
from app.services.message_service import MessageService
from app.core.exceptions import ValidationException
from app.api.dependencies import get_current_user, get_message_service
from app.schemas.user import UserModel

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/send", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    message_data: MessageCreate,
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> MessageResponse:
    try:
        # ✅ Direct await
        message = await message_service.send_message(
            sender_id=current_user.user_id,
            receiver_id=message_data.receiver_id,
            content=message_data.content,
            item_id=message_data.item_id
        )
        return MessageResponse.from_domain(message)
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations", response_model=ConversationListResponse)
async def get_conversations(
    include_archived: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> ConversationListResponse:
    """Get all conversations"""
    try:
        # ✅ Direct await - NO asyncio.to_thread
        conversations = await message_service.get_user_conversations(
            user_id=current_user.user_id,
            include_archived=include_archived,
            limit=limit
        )
        return ConversationListResponse(
            conversations=[ConversationResponse.from_domain(conv) for conv in conversations],
            total=len(conversations)
        )
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/conversations/{conversation_id}", response_model=MessageListResponse)
async def get_conversation_messages(
    conversation_id: str,
    limit: int = Query(50, ge=1, le=200),
    current_user: UserModel = Depends(get_current_user),
    message_service: MessageService = Depends(get_message_service)
) -> MessageListResponse:
    """Get messages in conversation"""
    try:
        # ✅ Direct await - NO asyncio.to_thread
        conversation = await message_service.get_conversation(conversation_id)
        
        if current_user.user_id not in conversation.participant_ids:
            raise HTTPException(status_code=403, detail="No access")
        
        # ✅ Direct await
        messages = await message_service.get_conversation_messages(
            conversation_id=conversation_id,
            limit=limit
        )
        
        # ✅ Direct await
        await message_service.mark_conversation_as_read(
            conversation_id=conversation_id,
            user_id=current_user.user_id
        )
        
        return MessageListResponse(
            messages=[MessageResponse.from_domain(msg) for msg in messages],
            total=len(messages)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))
