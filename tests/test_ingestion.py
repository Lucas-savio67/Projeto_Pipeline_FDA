from unittest.mock import MagicMock, patch 
from src.data_ingestion.data_ingestion import DataIngestion

import logging
import pytest

def test_success_data_ingestion(): 
    api = {'FDA_DRUG': {'campo_1': 'valor_1', 'campo_2':'valor_2'}}
    mock_client = MagicMock()
    mock_client.put_object.return_value = {'success': True, 'metadata': 'test_metadata'}
    ingested_data = {'apis':{'FDA_DRUG':'injetada'}}
    ingestao = DataIngestion(api,mock_client, 'bucket_teste')
    injetar = ingestao.injetar_dado_apis(api) 
    assert injetar == ingested_data
