import requests 
import logging 
from typing import Any
logger = logging.getLogger(__name__)
class ImportingErrors(Exception): 
    pass
class DataImport: 
    def __init__(self, data_dict:dict[str, Any]) -> None: 
        self.data = data_dict 
        self.imported_data:dict[str, Any] = {}
    def importar_apis(self) -> dict[str,Any] : 
        if not self.data : 
            logger.error("Erro fatal, o dicionário de fontes está vazio! ")
            raise ImportingErrors("Erro fatal, o dicionário de fontes está vazio! ")
        imported_apis = {}
        apis_errors = {}
        apis = self.data.get('apis', [])
        logger.info("O fluxo de importação das APIs começou! ")
        for nome_api, info_api in apis.items(): 
            try :
                paginacao = info_api.get('paginacao', False)
                if paginacao :
                    data = self.importar_com_paginacao(nome_api, info_api)
                else : 
                    data = self.importar_dados_apis_generico(nome_api, info_api)
                imported_apis[nome_api] = data
            except ImportingErrors as e : 
                logger.warning(str(e))
                apis_errors[nome_api] = {str(e)}
            except ValueError as e : 
                logger.warning(str(e))
                apis_errors[nome_api] = {'erro': str(e)}
            except TimeoutError as e : 
                logger.warning(str(e))
                apis_errors[nome_api] = {'erro': str(e)}
        if apis_errors : 
            logger.info(f"APIs com erro {apis_errors}")
        logger.info(f"APIs importadas com sucesso: {list(imported_apis.keys())}")
        logger.info("O fluxo de importação das APIs terminou! ")
        self.imported_data['apis'] = imported_apis
        return self.imported_data
    def importar_com_paginacao(self, nome_api:str, info_api:dict[str,Any]) -> list[Any]:
        resultados = []
        url = info_api['url']
        params = info_api.get('params', None)
        headers = info_api.get('headers', None)
        max_paginas = info_api.get('max_paginas', None)
        api_key = params.get('api_key') if params else None
        n_paginas = 0
        try :
            while url:
                if max_paginas is not None and n_paginas >= max_paginas : 
                    logger.info(f"Maximo de páginas alcançado, páginas retornadas: {max_paginas} para a API {nome_api}! ")
                    break
                logger.info(f"[{nome_api}] buscando página, url: {url}")
                request_params = params if params else {'api_key': api_key}
                response = requests.get(url, params=request_params, headers=headers, timeout=10)
                if response.status_code != 200:
                    raise ImportingErrors(f"status code: {response.status_code}")
                try :
                    data = response.json()
                except ValueError : 
                    raise ValueError(f"Erro, a API {nome_api} falhou, JSON inválido! ")
                resultados.append(data)
                n_paginas+=1
                url = self._extrair_proximo_link(response)
                params = None  
        except requests.exceptions.Timeout : 
            raise TimeoutError(f"Erro, a API {nome_api} falhou, tempo máximo excedido! ")
        return resultados

    def _extrair_proximo_link(self, response) -> str | None:
        link_header = response.headers.get('Link')
        if not link_header:
            return None

    
        for parte in link_header.split(','):
            if 'rel="next"' in parte:
            
                inicio = parte.find('<') + 1
                fim = parte.find('>')
                if inicio > 0 and fim > inicio:
                    return parte[inicio:fim].strip()

        return None
    def importar_dados_apis_generico(self, nome_api:str, info_api:dict[str,Any]) -> dict[str, Any] : 
        params = info_api.get('params', None)
        try :
            response = requests.get(url=info_api['url'], params=params,timeout=10)
            if response.status_code != 200 : 
                raise ImportingErrors(f'Erro, a API {nome_api} falhou, status code: {response.status_code}')
            try :
                data = response.json()
                return data
            except ValueError : 
                raise ValueError(f'Erro, a api {nome_api} falhou, JSON inválido! ')
        except requests.exceptions.Timeout: 
            raise TimeoutError(f"Erro, a API {nome_api} falhou, tempo máximo excedido! ")
        
        
            
