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
        self.api_tables:dict[str,Any] = {}
        self.cleaning_rules = cleaning_rules



    def transformar_dados(self) -> None : 
        
        if not self.extracted_data: 
            logger.error("Erro, nenhum dado foi extraído! ")
            raise TransformingErrors("Erro, nenhum dado foi extraído! ")
        apis = self.extracted_data.get('apis', {})
        if not apis : 
            logger.warning("Nenhuma API foi extraída! ")
        else: 
            tratamento_apis =self.tratar_apis(apis)
            if not tratamento_apis: 
                logger.warning("Nenhuma regra de limpeza para APIs foi encontrada! ")

            


    def tratar_apis(self, apis:dict[str,Any]) -> dict[str, Any]: 

        regras_limpeza_apis = self.cleaning_rules.get('apis', {})
        if not regras_limpeza_apis: 
            return False
        for nome_api,conteudo_api in apis.items(): 
            nome_novo = self.limpar_nomes(nome_api)
            regra_api = regras_limpeza_apis.get(nome_novo, {})
            if not regra_api: 
                logger.warning(f"A API {nome_api} não possui regra de limpeza! ")
            else:
                tabelas_novas =self.criar_tabelas_novas(conteudo_api, regra_api)
                self.api_tables[nome_novo] = tabelas_novas
        return self.api_tables
    def limpar_tabela_principal(self, conteudo_api:Any, regra:dict[str,Any]) -> dict[str,Any]: 
        nome_tabela_principal = regra.get('nome_tabela_principal', {})
        if not nome_tabela_principal : 
            raise TransformingErrors("Erro, a regra para transformação da tabela principal não foi encontrada! ")
        main_table = {}
        df = pd.json_normalize(conteudo_api)
        main_table[nome_tabela_principal] = df 
        return main_table
    def criar_tabelas_novas(self, conteudo_api:Any, regra:dict[str,Any]) -> dict[str,Any]: 
        new_tables = {}
        tabelas_novas = regra.get('tabelas_a_parte')
        if not tabelas_novas: 
            return False 
        tipo_api = regra.get('tipo_api' ,{})
        parte_essencial = regra.get('parte essencial')
        for nome_tabela_nova, info_tabela_nova in tabelas_novas.items(): 
            if tipo_api == 'lista': 
                df = pd.json_normalize(conteudo_api[0][parte_essencial], record_path=info_tabela_nova['record_path'], meta=info_tabela_nova['meta'])
                new_tables[nome_tabela_nova] = df
        return new_tables


        
    def explorar_json(self , obj:Any, identacao=0) -> None : 
        prefixo = identacao * ' '
        if isinstance(obj, dict): 
            for chave,valor in obj.items(): 
                print(f'{prefixo}.{chave} -> {type(valor)}')
                self.explorar_json(valor, identacao+1)
        elif isinstance(obj, list):
            print(f'{prefixo}{type(obj[0])}')
            self.explorar_json(obj[0], identacao+1)



    def limpar_nomes(self,key:str) -> str : 
        nome = Path(key).stem 
        nome = nome.strip().lower()
        nome = re.sub(r'[^a-z0-9_-]', '_', nome)
        return nome.upper()
