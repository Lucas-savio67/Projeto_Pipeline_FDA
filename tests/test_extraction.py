import logging
import pytest
import json
import io
from unittest.mock import Mock, patch, MagicMock
from src.data_extraction.data_extraction import DataExtraction, ExtractionErrors
from botocore.exceptions import ClientError
def test_success_extraction(): 
    dados_teste={'campo_1':'valor_1'}
    mock_client = MagicMock()

    mock_client.get_object.return_value = {'Body':io.BytesIO(json.dumps(dados_teste).encode('utf-8')),
                                            'ResponseMetaData': {'HTTPStatusCode': 200}}

    extracao = DataExtraction(mock_client, 'bucket_teste')
    extrair = extracao.extrair_dados_apis('key_teste')
    assert extrair == {'key_teste': dados_teste}
def test_client_error(): 
    mock_client = MagicMock() 
    mock_client.get_object.side_effect = ClientError(  error_response={
        'Error': {
            'Code': 'AccessDenied',
            'Message': 'Access Denied'
        }
    },
    operation_name='PutObject'
) 
    with pytest.raises(ExtractionErrors) : 
        extracao = DataExtraction(mock_client, 'bucket_teste')
        extrair = extracao.extrair_dados_apis('key_teste')