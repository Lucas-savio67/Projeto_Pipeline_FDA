from pathlib import Path
from typing import Any
import re
import logging
import pandas as pd 
logger = logging.getLogger(__name__)
class StructuringErrors(Exception): 
    pass
class DataStructuring: 
    def __init__(self, extracted_data:dict[str, dict[str,Any]], cleaning_rules:dict[str, dict]) -> None: 
        self.extracted_data = extracted_data 
        self.transformed_data:dict[str, dict[str,Any]] = {}
        self.api_tables:dict[str,Any] = {}
        self.cleaning_rules = cleaning_rules
    def estruturar_apis(self) -> dict[str, Any]: 
        errors = {}
        apis = self.extracted_data.get('apis' , {})
        if not apis : 
            logger.error('Nenhuma API foi extraída! ')
            raise StructuringErrors("Nenhuma API foi extraída! ")
        regras_limpeza_apis = self.cleaning_rules.get('apis', {})
        if not regras_limpeza_apis: 
            logger.error('Erro, não há regra de limpeza para APIs! ')
            raise StructuringErrors("Erro, não há regra de limpeza para APIs! ")
        logger.info("Iniciando o fluxo de estruturação de APIs! ")
        for nome_api,conteudo_api in apis.items(): 
            nome_novo = self.limpar_nomes(nome_api)
            regra_api = regras_limpeza_apis.get(nome_novo, {})
            if not regra_api: 
                logger.warning(f"A API {nome_api} não possui regra de limpeza! ")
            else:
                conteudo_obtido = self. obter_conteudo(conteudo_api, regra_api)
                tabela_principal = self.estruturar_tabela_principal(conteudo_obtido, regra_api)
                tabelas_novas =self.criar_tabelas_novas(conteudo_obtido, regra_api)
                if tabelas_novas[1]: 
                    errors[nome_novo] = tabelas_novas[1]
                elif tabela_principal[1]:
                    errors[nome_novo] = tabela_principal[1]
                self.api_tables[nome_novo] = [tabela_principal[0],tabelas_novas[0]]    
        if errors: 
            logger.info(f"Erros de estruturação: {errors}")
        estruturados = []
        for tabelas in self.api_tables.values(): 
            for tabela in tabelas : 
                for nome_tabela in tabela : 
                    estruturados.append(nome_tabela)
        logger.info(f"Tabelas totais estruturadas com sucesso: {estruturados}")
        return self.api_tables
    def obter_conteudo(self, conteudo_api:Any, registros:dict[str,Any]) -> list | dict: 
        local_registros = registros.get("local_registros")
        if isinstance(conteudo_api, list): 
            if len(conteudo_api) == 1 : 
                return conteudo_api[0]
            else : 
                resultados_emendados = [registro for pagina in conteudo_api for registro in pagina.get(local_registros , [])]
                return {**conteudo_api[0], local_registros:resultados_emendados}
    def estruturar_tabela_principal(self, conteudo_api:Any, regra:dict[str,Any]) -> dict[str,Any]: 
        table_errors = {}
        logger.info("Començando o fluxo de estruturação da tabela principal! ")
        main_table = {}
        local_registros = regra.get('local_registros' , {})
        nome_tabela = regra.get('nome_tabela_principal', {})
        if not nome_tabela or not local_registros : 
            logger.warning('Erro, verifique se a tabela principal possui nome ou o local dos registros especificado! ')
            raise StructuringErrors("Erro, verifique se a tabela principal possui nome ou o local dos registros especificado! ")
        try :
            df = pd.json_normalize(conteudo_api[local_registros])
            logger.info(f"A tabela {nome_tabela} foi transformada em um DataFrame com sucesso! ")
            main_table[nome_tabela] = df 
        except KeyError as e : 
            logger.warning(f"Erro: {e} ao estruturar a tabela principal! ")
            table_errors[nome_tabela] = {'erro': str(e)}
        if table_errors : 
            logger.info(f'Erros de estruturação da tabela principal: {table_errors}')
        logger.info(f'Tabelas principais estruturadas com sucesso: {list(main_table.keys())}')
        return main_table, table_errors
    def criar_tabelas_novas(self, conteudo_api:Any, regra:dict[str,Any]) -> dict[str,Any]: 
        table_errors = {}
        new_tables = {} 
        local_registros = regra.get('local_registros' , {})
        tabelas_a_parte = regra.get('tabelas_a_parte' , {})
        if not tabelas_a_parte  or not local_registros : 
            logger.warning('Erro, verifique se as informações das tabelas a parte existem ou o local dos registros especificado! ')
            raise StructuringErrors("Erro, verifique se as informações das tabelas a parte existem ou o local dos registros especificado! ")
        logger.info("Iniciando o fluxo de estruturação de tabelas alheias! ")
        for nome_tabela, info_tabela in tabelas_a_parte.items(): 
            try :
                df = pd.json_normalize(conteudo_api[local_registros] , record_path=info_tabela['record_path'] , meta = info_tabela['meta'])
                new_tables[nome_tabela] = df 
                logger.info(f'A tabela {nome_tabela} foi estruturada com sucesso! ')
            except KeyError as e : 
                logger.warning(f"Erro: {e} ao estruturar a tabela {nome_tabela}! ")
                table_errors[nome_tabela] = {'erro': str(e)}
        if table_errors : 
            logger.info(f"Erros de estruturação de tabelas alheias: {table_errors}")
        logger.info(f"Tabela alheias estruturadas com êxito: {list(new_tables.keys())}")

        return new_tables , table_errors

    def explorar_json(self , obj:Any, identacao=0) -> None : 
        prefixo = identacao * ' '
        if isinstance(obj, dict): 
            for chave,valor in obj.items(): 
                print(f'{prefixo}.{chave} -> {type(valor)}')
                self.explorar_json(valor, identacao+1)
        elif isinstance(obj, list):
            print(f'{prefixo}{type(obj)} -> objeto dentro: {type(obj[0])}')
            self.explorar_json(obj[0], identacao+1)
            
    def limpar_nomes(self,key:str) -> str : 
        nome = Path(key).stem 
        nome = nome.strip().lower()
        nome = re.sub(r'[^a-z0-9_-]', '_', nome)
        return nome.upper()
