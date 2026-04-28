"""
Tests for Firestore service.
"""

import pytest
from unittest.mock import patch, MagicMock
from services.firestore_service import FirestoreService

@pytest.fixture
def firestore_service():
    with patch("services.firestore_service.firestore.Client") as mock_client:
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        service = FirestoreService()
        service._db = mock_instance
        return service

@pytest.mark.asyncio
async def test_create_session(firestore_service):
    # Mock
    mock_doc = MagicMock()
    mock_collection = MagicMock()
    mock_collection.document.return_value = mock_doc
    firestore_service.db.collection.return_value = mock_collection
    
    # Test
    await firestore_service.create_session("test_user", "test_session")
    
    # Assert
    mock_doc.set.assert_called_once()

@pytest.mark.asyncio
async def test_save_message(firestore_service):
    # Mock
    mock_doc = MagicMock()
    mock_doc.id = "msg_123"
    mock_collection = MagicMock()
    mock_collection.add.return_value = [None, mock_doc]
    firestore_service.db.collection.return_value.document.return_value.collection.return_value = mock_collection
    
    # Test
    await firestore_service.save_message("test_session", "user", "Hello")
    
    # Assert
    mock_collection.add.assert_called_once()

@pytest.mark.asyncio
async def test_get_chat_history(firestore_service):
    # Mock
    mock_doc_ref = MagicMock()
    mock_doc_ref.to_dict.return_value = {"role": "user", "content": "Hi"}
    
    mock_query = MagicMock()
    mock_query.stream.return_value = [mock_doc_ref]
    firestore_service.db.collection.return_value.document.return_value.collection.return_value.order_by.return_value.limit.return_value = mock_query
    
    # Test
    history = await firestore_service.get_chat_history("test_session")
    
    # Assert
    assert len(history) == 1
    assert history[0]["role"] == "user"

@pytest.mark.asyncio
async def test_save_feedback(firestore_service):
    # Mock
    mock_collection = MagicMock()
    firestore_service.db.collection.return_value = mock_collection
    
    # Test
    await firestore_service.save_feedback("test_session", "msg_123", 5, "Good")
    
    # Assert
    mock_collection.add.assert_called_once()
