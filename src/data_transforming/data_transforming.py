from pathlib import Path
from typing import Any
import re
import logging 
logger = logging.getLogger(__name__)
class TransformingErrors(Exception): 
    pass
class DataTransforming: 
    def __init__(self, extracted_data:dict[str, dict[str,Any]]) -> None: 
        self.extracted_data = extracted_data 
        self.transformed_data:dict[str, dict[str,Any]] = {}
    def transformar_dados(self) -> None : 
        if not self.extracted_data: 
            logger.error("Erro, nenhum dado foi extraído! ")
            raise TransformingErrors("Erro, nenhum dado foi extraído! ")
        apis = self.extracted_data.get('apis', {})
        if apis : 
            for nome_api, conteudo_api in apis.items():
                self.tratar_apis(nome_api, conteudo_api)

    def tratar_apis(self, nome_api:str, conteudo:Any) -> None : 
        cleaned_apis = {}
        self.explorar_json(conteudo)
        nome_novo =self.limpar_nomes(nome_api)
        
    
    def explorar_json(self , obj:Any, identacao=0) -> None : 
        prefixo = identacao * ' '
        if isinstance(obj, dict): 
            for chave,valor in obj.items(): 
                print(f'{prefixo}.{chave} -> {type(valor)}')
                self.explorar_json(valor, identacao+1)
        elif isinstance(obj, list):
            print(f'{prefixo}{type(obj[0])}')
            self.explorar_json(obj[0], identacao+1)
    def limpar_nomes(self,key:str) -> None : 
        nome = Path(key).stem 
        nome = nome.strip().lower()
        nome = re.sub(r'[^a-z0-9_-]', '_', nome)
        return nome
