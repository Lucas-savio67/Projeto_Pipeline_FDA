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
    def importar_dados_apis(self, apis:dict[str, Any]) -> dict[str, Any] : 
        imported_apis = {}
        if apis :
            for tipo_dado,chave in apis.items(): 
                for nome_api,info in chave.items(): 
                    if info['params']: 
                        response = requests.get(info['url'], info['params'], timeout=10)
                    else : 
                        response = requests.get(info['url'], timeout=10)
                    if response.status_code != 200 : 
                        logger.warning(f"Erro, a API {nome_api} falhou, code: {response.status_code}")
                        continue 
                    else : 
                        data = response.json()
                        logger.info(f"A API {nome_api} foi importada com sucesso! ")
                        imported_apis[nome_api] = data
                        self.imported_data[tipo_dado] = imported_apis
            return self.imported_data
        else : 
            return 'Sem APIs para importar! '
