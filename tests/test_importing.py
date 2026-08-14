import pytest
from unittest.mock import Mock, patch 
from src.data_import.data_import import DataImport
@patch('src.data_import.data_import.requests.get')
def test_success_api_importing(mock_get): 
    mock_response = Mock()
    mock_response.json.return_value = {'status': 'success', 'data': [1,2,3]}
    mock_response.status_code = 200 
    mock_get.return_value = mock_response 
    fontes = {
        'FDA_DRUG': {
            'url': 'https://api.fda.gov/drug/event.json',
            'api_key': 'fake-key-de-teste',
            'max_paginas': 2
        }
    }
    api = fontes.get("FDA_DRUG")
    importador = DataImport(fontes)
    importar = importador.importar_dados_apis_generico('FDA_DRUG', api)
    assert importar == {'status': 'success', 'data': [1,2,3]}
@patch('src.data_import.data_import.requests.get')
def test_invalid_json_object(mock_get): 
    mock_response = Mock()
    mock_response.status_code = 200 
    mock_response.json.side_effect = ValueError("JSON inválido")
    mock_get.return_value = mock_response 
    fontes = {
            'FDA_DRUG': {
                'url': 'https://api.fda.gov/drug/event.json',
                'api_key': 'fake-key-de-teste',
                'max_paginas': 2
            }
        }
    api = fontes.get("FDA_DRUG")
    with pytest.raises(ValueError): 
        importador = DataImport(fontes)
        resultado = importador.importar_dados_apis_generico('FDA_DRUG', api)
@patch('src.data_import.data_import.requests.get')
def test_timeout_error(mock_get): 
    mock_get.side_effect = TimeoutError("Tempo excedido")
    fontes = {
                'FDA_DRUG': {
                    'url': 'https://api.fda.gov/drug/event.json',
                    'api_key': 'fake-key-de-teste',
                    'max_paginas': 2
                }
            }
    api = fontes.get("FDA_DRUG")
    with pytest.raises(TimeoutError): 
        importador = DataImport(fontes)
        resultado = importador.importar_dados_apis_generico('FDA_DRUG', api)
