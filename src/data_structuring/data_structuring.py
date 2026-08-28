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



    def estruturar_dados(self) -> None : 
        if not isinstance(self.extracted_data, dict) or not isinstance(self.cleaning_rules, dict): 
            logger.error('Erro, verifique se os dados extraído ou as regras de limpeza são dicionários! ')
            raise StructuringErrors("Erro, verifique se os dados extraído ou as regras de limpeza são dicionários! ")
        if not self.extracted_data: 
            logger.error("Erro, nenhum dado foi extraído! ")
            raise StructuringErrors("Erro, nenhum dado foi extraído! ")
        apis = self.extracted_data.get('apis', {})
        if not isinstance(apis, dict):
            raise StructuringErrors("O campo 'apis' deve ser um dicionário! ")
        if not apis : 
            logger.warning("Nenhuma API foi extraída! ")
            return {}
        else: 
            try :
                estruturacao_apis =self.estruturar_apis(apis)
                if not estruturacao_apis: 
                    logger.warning("Nenhuma regra de limpeza para APIs foi encontrada! ")
                else: 
                    return estruturacao_apis
            except (KeyError, IndexError, TypeError, ValueError) as e: 
                logger.warning(f'Erro na hora de estruturar as APIs, {str(e)}')
                raise StructuringErrors(f"Erro na hora de estruturar as APIs, {str(e)}")
    def estruturar_apis(self, apis:dict[str,Any]) -> dict[str, Any]: 
        regras_limpeza_apis = self.cleaning_rules.get('apis', {})
        if not regras_limpeza_apis: 
            return False
        for nome_api,conteudo_api in apis.items(): 
            try:
                nome_novo = self.limpar_nomes(nome_api)
                regra_api = regras_limpeza_apis.get(nome_novo, {})
                if not regra_api: 
                    logger.warning(f"A API {nome_api} não possui regra de limpeza! ")
                    continue
                tabelas_novas =self.criar_tabelas_novas(conteudo_api, regra_api)
                tabela_principal = self.estruturar_tabela_principal(conteudo_api, regra_api)
                self.api_tables[nome_novo] = [tabela_principal,tabelas_novas]
            except (KeyError, IndexError, TypeError, ValueError) as e:
                logger.warning(f"Erro ao estruturar a API {nome_api}: {e}")
                raise StructuringErrors(
                    f"Erro na estrutura da API {nome_api}: {e}"
                ) from e
        return self.api_tables
    def estruturar_tabela_principal(self, conteudo_api:Any, regra:dict[str,Any]) -> dict[str,Any]: 
        nome_tabela_principal = regra.get('nome_tabela_principal', {})
        parte_essencial = regra.get('parte essencial', {})
        tipo_api = regra.get('tipo_api', {})
        if not nome_tabela_principal : 
            raise StructuringErrors("Erro, a regra para transformação da tabela principal não foi encontrada! ")
        main_table = {}
        try :
            if tipo_api == 'lista': 
                dados = self._obter_conteudo(conteudo_api)[parte_essencial]
                df = pd.json_normalize(dados)
                main_table[nome_tabela_principal] = df 
        except (KeyError, IndexError, TypeError, ValueError) as e: 
            logger.warning(f'Erro {e} ao estruturar a tabela {nome_tabela_principal}')
            raise StructuringErrors(
                f"Erro ao estruturar a tabela {nome_tabela_principal}: {e}"
            ) from e
        return main_table
    def criar_tabelas_novas(self, conteudo_api:Any, regra:dict[str,Any]) -> dict[str,Any]: 
        new_tables = {}
        tabelas_novas = regra.get('tabelas_a_parte')
        if not tabelas_novas: 
            return False 
        tipo_api = regra.get('tipo_api' ,{})
        parte_essencial = regra.get('parte essencial')
        if not isinstance(tabelas_novas, dict):
            raise StructuringErrors("'tabelas_a_parte' deve ser um dicionário! ")
        for nome_tabela_nova, info_tabela_nova in tabelas_novas.items(): 
            if tipo_api == 'lista': 
                try:
                    if not isinstance(info_tabela_nova, dict):
                        raise TypeError("a configuração da tabela deve ser um dicionário")
                    df = pd.json_normalize(
                        self._obter_conteudo(conteudo_api)[parte_essencial],
                        record_path=info_tabela_nova['record_path'],
                        meta=info_tabela_nova['meta']
                    )
                    new_tables[nome_tabela_nova] = df
                except (KeyError, IndexError, TypeError, ValueError) as e:
                    raise StructuringErrors(
                        f"Erro ao estruturar a tabela {nome_tabela_nova}: {e}"
                    ) from e
        return new_tables

    def _obter_conteudo(self, conteudo_api: Any) -> dict[str, Any]:
        if not isinstance(conteudo_api, dict) or not conteudo_api:
            raise TypeError("o conteúdo da API deve ser um dicionário não vazio")
        conteudo = next(iter(conteudo_api.values()))
        if not isinstance(conteudo, dict):
            raise TypeError("o conteúdo interno da API deve ser um dicionário")
        return conteudo
    def explorar_json(self , obj:Any, identacao=0) -> None : 
        prefixo = identacao * ' '
        if isinstance(obj, dict): 
            for chave,valor in obj.items(): 
                print(f'{prefixo}.{chave} -> {type(valor)}')
                self.explorar_json(valor, identacao+1)
        elif isinstance(obj, list):
            if not obj:
                print(f'{prefixo}lista vazia')
                return
            print(f'{prefixo}{type(obj[0])}')
            self.explorar_json(obj[0], identacao+1)
    def limpar_nomes(self,key:str) -> str : 
        if not isinstance(key, str): 
            logger.warning('Erro, a key não é uma string! ')
            raise StructuringErrors("Erro, a key não é uma string! ")
        nome = Path(key).stem 
        nome = nome.strip().lower()
        nome = re.sub(r'[^a-z0-9_-]', '_', nome)
        return nome.upper()
