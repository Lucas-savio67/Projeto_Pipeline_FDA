import logging
import pytest
import json
from unittest.mock import Mock, patch, MagicMock
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
@patch('src.data_extraction.data_extraction.open')
@patch('src.data_extraction.data_extraction.Path')
def test_permission_error(mock_path_cls, mock_open, caplog):
    mock_arquivo = MagicMock()
    mock_arquivo.is_file.return_value = True
    mock_arquivo.name = 'api1.json'
    mock_arquivo.__str__.return_value = 'diretorio_teste/api1.json'

    mock_diretorio = MagicMock()
    mock_diretorio.exists.return_value = True
    mock_diretorio.iterdir.return_value = [mock_arquivo]
    mock_path_cls.return_value = mock_diretorio

    mock_open.side_effect = PermissionError("Erro de permissão")

    extracao = DataExtraction()
    with caplog.at_level(logging.WARNING):
        extrair = extracao.extrair_dados_apis('diretorio_teste')
@patch('src.data_extraction.data_extraction.json.load')
@patch('src.data_extraction.data_extraction.open')
@patch('src.data_extraction.data_extraction.Path')
def test_json_invalido(mock_path_cls, mock_open, mock_load):
    mock_arquivo = MagicMock()
    mock_arquivo.is_file.return_value = True
    mock_arquivo.name = 'api1.json'
    mock_arquivo.__str__.return_value = 'diretorio_teste/api1.json'

    mock_diretorio = MagicMock()
    mock_diretorio.exists.return_value = True
    mock_diretorio.iterdir.return_value = [mock_arquivo]
    mock_path_cls.return_value = mock_diretorio

    mock_load.side_effect = json.JSONDecodeError("Expecting value", "", 0)

    extracao = DataExtraction()

    with pytest.raises(json.JSONDecodeError):
        extracao.extrair_dados_apis('diretorio_teste')