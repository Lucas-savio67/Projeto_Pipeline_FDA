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