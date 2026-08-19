from pathlib import Path
from typing import Any
import re
import logging
import pandas as pd 
logger = logging.getLogger(__name__)
class TransformingErrors(Exception): 
    pass
class DataTransforming: 
    def __init__(self, extracted_data:dict[str, dict[str,Any]], cleaning_rules:dict[str, dict]) -> None: 
        self.extracted_data = extracted_data 
        self.transformed_data:dict[str, dict[str,Any]] = {}
        self.cleaned_apis:dict[str,Any] = {}
        self.cleaning_rules = cleaning_rules
    def transformar_dados(self) -> None : 
        
        if not self.extracted_data: 
            logger.error("Erro, nenhum dado foi extraído! ")
            raise TransformingErrors("Erro, nenhum dado foi extraído! ")
        apis = self.extracted_data.get('apis', {})
        if apis : 
            regras_limpeza_apis = self.cleaning_rules.get('apis', {})
            if not regras_limpeza_apis : 
                logger.warning("Não há regras de limpeza para APIs! ")
            else :
                for nome_api, conteudo_api in apis.items():
                    new_api_data=self.tratar_apis(nome_api, conteudo_api, regras_limpeza_apis)
                self.transformed_data['apis'] = new_api_data
    def tratar_apis(self, nome_api:str, conteudo:Any, regra_limpeza_apis:dict[str, dict]) -> None : 
        nome_novo = self.limpar_nomes(nome_api)
        regras = regra_limpeza_apis.get(nome_novo, {})
        if not regras : 
            logger.warning(f"Nenhuma regra de limpeza foi encontrada para a API {nome_novo}!  ")
            return False
        self.explorar_json(conteudo)
        tabelas_novas = regras.get('tabelas a parte', {})
        if tabelas_novas: 
            for tabela_nova, info_tabela_nova in tabelas_novas.items(): 
                
                tabela_nova = pd.json_normalize(conteudo[0]['results'], record_path=info_tabela_nova['record_path'], meta=info_tabela_nova['meta'])
                print(tabela_nova.head())
        return self.cleaned_apis
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
        return nome.upper()
