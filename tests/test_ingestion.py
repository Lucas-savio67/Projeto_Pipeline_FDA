from unittest.mock import Mock, patch 
from src.data_ingestion.data_ingestion import DataIngestion
import logging
import pytest
def test_success_data_ingestion(): 
    api = {'FDA_DRUG': {'campo_1': 'valor_1', 'campo_2':'valor_2'}}
    ingested_data = {'apis':{'FDA_DRUG':'injetada'}}
    ingestao = DataIngestion(api)
    injetar = ingestao.injetar_dado_apis(api) 
    assert injetar == ingested_data
@patch('src.data_ingestion.data_ingestion.json.dump')
def test_typeerror(mock_dump, caplog): 
    api = {}
    ingestao = DataIngestion(api)
    mock_dump.side_effect = TypeError("Erro de tipo")
    with caplog.at_level(logging.WARNING): 
        ingestao.injetar_dado_apis(api)
@patch('src.data_ingestion.data_ingestion.open')
def test_oserror(mock_open,caplog): 
    api = {}
    ingestao = DataIngestion(api)
    mock_open.side_effect = OSError("Erro de sistema")
    with caplog.at_level(logging.WARNING): 
        ingestao = ingestao.injetar_dado_apis(api)