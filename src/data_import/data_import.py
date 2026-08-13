import requests 
import logging 
from typing import Any
logger = logging.getLogger(__name__)
class DataImport: 
    def __init__(self, data_dict:dict[str, Any]) -> None: 
        self.data = data_dict 
        self.imported_data:dict[str, Any] = {}
    def importar_dados(self) -> str : 
        apis = self.data.get('apis', [])
        self.importar_dados_apis(apis)
        return self.imported_data
    def importar_dados_apis(self, apis:dict[str, Any]) -> dict[str, Any] : 
        imported_apis = {}
        api_errors = {}
        if apis :
            logger.info("A importação de APIs começou! ")
            for nome_api,info in apis.items(): 
                    params = info.get('params', None)
                    response = requests.get(url=info['url'], params=params,timeout=10)
                    if response.status_code != 200 : 
                        logger.warning(f"Erro, a API {nome_api} falhou, code: {response.status_code}")
                        api_errors[nome_api] = {'status_code': response.status_code}
                        continue 
                    else : 
                        data = response.json()
                        logger.info(f"A API {nome_api} foi importada com sucesso! ")
                        imported_apis[nome_api] = data
                        self.imported_data['apis'] = imported_apis
            logger.info("A importação de APIs terminou! ")
            logger.info(f"APIs importadas com êxito: {list(imported_apis.keys())}")
            if api_errors : 
                logger.info(f"APIs que falharam: {api_errors}")
            return self.imported_data
        else : 
            logger.info('Não há APIs para importar, pulando este módulo...')
            return 'Sem APIs para importar! '
            
