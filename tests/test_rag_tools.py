import pytest
from unittest.mock import patch, MagicMock
from tools.rag_tools import retrieve_manual_info

@patch("tools.rag_tools.Chroma")
@patch("tools.rag_tools.OpenAIEmbeddings")
def test_retrieve_manual_info_found(mock_embeddings, mock_chroma):
    mock_vector_store = MagicMock()
    
    mock_doc_1 = MagicMock()
    mock_doc_1.page_content = "To reset the device, hold the power button for 10 seconds."
    
    mock_doc_2 = MagicMock()
    mock_doc_2.page_content = "The warranty does not cover water damage."
    
    mock_vector_store.similarity_search.return_value = [mock_doc_1, mock_doc_2]
    mock_chroma.return_value = mock_vector_store
    
    result = retrieve_manual_info.invoke({"query": "How to reset?"})
    
    assert "hold the power button" in result
    assert "water damage" in result

@patch("tools.rag_tools.Chroma")
@patch("tools.rag_tools.OpenAIEmbeddings")
def test_retrieve_manual_info_not_found(mock_embeddings, mock_chroma):
    mock_vector_store = MagicMock()
    mock_vector_store.similarity_search.return_value = []
    mock_chroma.return_value = mock_vector_store
    
    result = retrieve_manual_info.invoke({"query": "Unknown issue"})
    
    assert result == "No relevant information found in the product manuals."