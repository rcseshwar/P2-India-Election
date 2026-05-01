import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from services.firestore_service import FirestoreService

@pytest.fixture
def mock_db():
    with patch('services.firestore_service.firestore.Client') as MockClient:
        mock_client = MockClient.return_value
        yield mock_client

@pytest.fixture
def service(mock_db):
    return FirestoreService()

@pytest.mark.asyncio
async def test_create_session(service, mock_db):
    mock_doc = MagicMock()
    mock_db.collection.return_value.document.return_value = mock_doc
    res = await service.create_session("u1", "s1")
    assert res["user_id"] == "u1"
    mock_doc.set.assert_called_once()

@pytest.mark.asyncio
async def test_get_session(service, mock_db):
    mock_doc = MagicMock()
    mock_doc.get.return_value.exists = True
    mock_doc.get.return_value.to_dict.return_value = {"id": "s1"}
    mock_db.collection.return_value.document.return_value = mock_doc
    res = await service.get_session("s1")
    assert res == {"id": "s1"}

@pytest.mark.asyncio
async def test_update_session(service, mock_db):
    mock_doc = MagicMock()
    mock_db.collection.return_value.document.return_value = mock_doc
    await service.update_session("s1", {"foo": "bar"})
    mock_doc.update.assert_called_once()

@pytest.mark.asyncio
async def test_save_message(service, mock_db):
    mock_coll = MagicMock()
    mock_ref = MagicMock()
    mock_ref.id = "m1"
    mock_coll.add.return_value = (None, mock_ref)
    mock_db.collection.return_value.document.return_value.collection.return_value = mock_coll
    res = await service.save_message("s1", "user", "hi")
    assert res == "m1"
    mock_coll.add.assert_called_once()

@pytest.mark.asyncio
async def test_get_chat_history(service, mock_db):
    mock_msg = MagicMock()
    mock_msg.to_dict.return_value = {"content": "hi"}
    mock_db.collection.return_value.document.return_value.collection.return_value.order_by.return_value.limit.return_value.stream.return_value = [mock_msg]
    res = await service.get_chat_history("s1")
    assert len(res) == 1
    assert res[0]["content"] == "hi"

@pytest.mark.asyncio
async def test_save_feedback(service, mock_db):
    mock_coll = MagicMock()
    mock_db.collection.return_value = mock_coll
    await service.save_feedback("s1", "m1", 5, "great")
    mock_coll.add.assert_called_once()

@pytest.mark.asyncio
async def test_get_election_data(service, mock_db):
    mock_doc = MagicMock()
    mock_doc.to_dict.return_value = {"foo": "bar"}
    mock_db.collection.return_value.where.return_value.stream.return_value = [mock_doc]
    res = await service.get_election_data("cat1")
    assert len(res) == 1

@pytest.mark.asyncio
async def test_seed_election_data(service, mock_db):
    mock_batch = MagicMock()
    mock_db.batch.return_value = mock_batch
    res = await service.seed_election_data([{"foo": "bar"}])
    assert res == 1
    mock_batch.commit.assert_called()

