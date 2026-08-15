import pytest
import json
from unittest.mock import Mock, patch
from src.data_extraction.data_extraction import DataExtraction, ExtractionErrors

def test_success_extraction(tmp_path):
    (tmp_path / "api1.json").write_text(json.dumps({'status': 'success', 'data': [1, 2, 3]}))

    extracao = DataExtraction()
    resultado = extracao.extrair_dados_apis(str(tmp_path))

    assert resultado == {'api1': {'status': 'success', 'data': [1, 2, 3]}}
def test_no_api(): 
    with pytest.raises(ExtractionErrors) : 
        extracao = DataExtraction()
        extrair = extracao.extrair_dados_apis('diretorio_teste')