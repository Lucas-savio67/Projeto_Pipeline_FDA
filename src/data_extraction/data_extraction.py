import logging
import json
from typing import Any
from pathlib import Path
logger = logging.getLogger(__name__)
class ExtractionErrors(Exception): 
    pass
class DataExtraction : 
    def __init__(self) -> None : 
        self.extracted_data : dict[str, dict[str,Any]] = {}
    def extrair_dados(self) -> dict[str, dict[str,Any]]: 
        dados = Path('data/bronze/')
        if not dados.exists(): 
            logger.error(f"Erro, nenhum arquivo foi injetado no caminho! ")
            raise ExtractionErrors(f"Erro, nenhum arquivo foi injetado no caminho! ")
        logger.info("Começando o fluxo de extração...")
        for tipo_dado in dados.iterdir(): 
            try :
                if tipo_dado.name == 'apis' and tipo_dado.is_dir(): 
                    logger.info("Procurando por APIs injetadas...")
                    api_data = self.extrair_dados_apis('data/bronze/apis/')
                    self.extracted_data['apis'] = api_data
            except ExtractionErrors as e : 
                logger.warning(str(e))
            except json.JSONDecodeError as e: 
                logger.warning(str(e))
            except PermissionError as e : 
                logger.warning(str(e))
        logger.info("O fluxo de extracão terminou! ")
        logger.info(f"Dados extraídos: {self.extracted_data}")
        return self.extracted_data
    def extrair_dados_apis(self, diretorio:str) -> dict[str,Any]: 
        extracted_apis = {}
        diretorio = Path(diretorio)
        if not diretorio.exists(): 
            logger.warning("Nenhuma API foi encontrada! ")
            raise ExtractionErrors("Nenhuma API foi encontrada! ")
        try :
            for arquivo in diretorio.iterdir(): 
                if arquivo.is_file(): 
                    nome_api = arquivo.name.split('.json')
                    caminho_arquivo = f'{arquivo}' 
                    try :
                        with open(caminho_arquivo, 'r', encoding='utf-8') as f : 
                            api_data = json.load(f)
                            extracted_apis[nome_api[0]] = api_data
                        logger.info(f"O arquivo {arquivo} foi extraído com sucesso! ")
                    except json.JSONDecodeError as e : 
                        logger.warning(f"Erro {e}, o JSON {nome_api} é inválido! ")
                    except PermissionError as e : 
                        logger.warning(f"Erro {e}, permissão de leitura negada para a API {nome_api}! ")
        except NotADirectoryError as e : 
            raise ExtractionErrors("Erro, o caminho fornecido não é um diretório! ") 
        return extracted_apis