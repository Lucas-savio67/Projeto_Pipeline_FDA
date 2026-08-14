import logging 
import json 
logger = logging.getLogger(__name__)
from typing import Any 
class IngestionErrors(Exception): 
    pass
class DataIngestion : 
    def __init__(self, imported_data:dict[str, dict[str,Any]]) -> None : 
        self.imported_data = imported_data 
    def injetar_dados(self) -> str : 
        ingested_data = {}
        if not self.imported_data : 
            logger.error("Erro, nenhum dado foi importado, o dicionário está vazio! ")
            raise IngestionErrors("Erro, nenhum dado foi importado, o dicionário está vazio! ")
        logger.info("Começando o fluxo  de ingestão dos dados! ")
        apis = self.imported_data.get('apis', {})
        data =self.injetar_dado_apis(apis)
        ingested_data['dados_injetados'] = data
        logger.info("O fluxo de ingestão terminou")
        logger.info(f"Dados injetados com sucesso: {ingested_data}")

    def injetar_dado_apis(self, apis:dict[str,Any]) -> dict : 
        ingested_apis = {}
        if not apis : 
            logger.warning("O tipo de dado API não foi encontrado! ")
        logger.info("Começando o fluxo de ingestão das APIs...")
        for nome_api, api in apis.items() :
            logger.info(f"Injetando a APi {nome_api} no diretório data! ")
            output_file = f'data/{nome_api}.json'
            with open(output_file, 'w') as f : 
                json.dump(api, f) 
            logger.info(f"A API {nome_api} foi carregada no diretório data com sucesso! ")
        ingested_apis['apis'] = nome_api
        return ingested_apis