from unittest.mock import MagicMock, patch 
from src.data_ingestion.data_ingestion import DataIngestion
from botocore.exceptions import ClientError
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
def test_client_error(caplog): 
    api = {'FDA_DRUG': {'campo_1': 'valor_1', 'campo_2':'valor_2'}}
    client_mock = MagicMock()
    client_mock.put_object.side_effect = ClientError(error_response={
        'Error': {
            'Code': 'AccessDenied',
            'Message': 'Access Denied'
        }
    },
    operation_name='PutObject'
)
    with caplog.at_level(logging.WARNING): 
        ingestao = DataIngestion(api,client_mock, 'bucket_teste')
        injetar = ingestao.injetar_dado_apis(api) 
def test_type_error(caplog): 
    api = {'FDA_DRUG': {'campo_1': 'valor_1', 'campo_2':'valor_2'}}
    mock_client =MagicMock()
    mock_client.put_object.side_effect = TypeError("Erro, JSON inválido! ")
    with caplog.at_level(logging.WARNING): 
        ingestao = DataIngestion(api,mock_client, 'bucket_teste')
        injetar = ingestao.injetar_dado_apis(api) 