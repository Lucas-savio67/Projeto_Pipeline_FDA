from unittest.mock import Mock, patch 
from src.data_ingestion.data_ingestion import DataIngestion
def test_success_data_ingestion(): 
    api = {'FDA_DRUG': {'campo_1': 'valor_1', 'campo_2':'valor_2'}}
    ingested_data = {'apis':{'FDA_DRUG':'injetada'}}
    ingestao = DataIngestion(api)
    injetar = ingestao.injetar_dado_apis(api) 
    assert injetar == ingested_data