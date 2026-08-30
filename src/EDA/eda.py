import logging 
logger = logging.getLogger(__name__)
import pandas as pd
import json 
from pathlib import Path 
<<<<<<< HEAD
from typing import Any
=======
>>>>>>> data_transforming
class EDAErrors(Exception): 
    pass
class EDA: 
    def __init__(self, tabelas:dict[str,list[dict[str,pd.DataFrame]]]) -> None : 
        self.tabelas = tabelas 
<<<<<<< HEAD
    def fazer_eda_tabelas(self) -> dict[str,dict[str, dict]]: 
=======
    def fazer_eda_tabelas(self) -> str: 
>>>>>>> data_transforming
        output_file = Path('eda_data.json')
        output_file.touch(exist_ok=True)
        if not self.tabelas: 
            logger.error('Erro, nenhuma tabela encontrada! ')
            raise EDAErrors("Erro, nenhuma tabela encontrada! ")
        
        eda_info = {}
        eda_tables_dict = {}
        for nome, tabelas in self.tabelas.items(): 
<<<<<<< HEAD
            logger.info(f"Começando o EDA de tabelas referentes a {nome}... ")
            for conteudo in tabelas : 
                for nome_tabela, df in conteudo.items(): 
                    logger.info(f'Fazendo o EDA da tabela: {nome_tabela}... ')
                    qtd_nulos = int(df.isna().sum().sum())
                    qtd_duplicatas = int(df.duplicated().sum())
                    pct_nulos = float(qtd_nulos / len(df) * 100) 
                    pct_duplicatas = float(qtd_duplicatas / len(df) * 100)
                    tamanho_df = len(df) 
                    colunas =  df.columns.to_list()
                    informacao_essencial = df.dtypes.astype(str).to_dict()
                    eda_info[nome_tabela] = { 
                        'qtd_nulos': qtd_nulos , 
                        'qtd_duplicatas': qtd_duplicatas , 
                        'pct_nulos': pct_nulos , 
                        'pct_duplicatas': pct_duplicatas , 
                        'tamanho_df': tamanho_df , 
                        'colunas': colunas , 
                        'info_essencial' : informacao_essencial
                    }
            eda_tables_dict[nome] = eda_info
            with open(output_file ,'w', encoding='utf-8') as f : 
                json.dump(eda_tables_dict , f, ensure_ascii=False, indent=4) 
            logger.info(f'Infomações de EDA referentes a {nome} foram carregadas no arquivo eda_data com sucesso! ')
        return eda_tables_dict
=======
            
            logger.info(f"Começando o EDA de tabelas referentes a {nome}... ")
            for conteudo in tabelas : 
                for nome_tabela, df in conteudo.items(): 
                    try :
                        logger.info(f'Fazendo o EDA da tabela: {nome_tabela}... ')
                        qtd_nulos = int(df.isna().sum().sum())
                    #qtd_duplicatas = df.duplicated().sum() 
                        pct_nulos =float(qtd_nulos / len(df) * 100)
                    #pct_duplicatas = qtd_duplicatas / len(df) * 100 
                        tamanho_df = int(len(df)) 
                        colunas =  df.columns.to_list()
                    
                        eda_info[nome_tabela] = { 
                        'qtd_nulos': qtd_nulos , 
                        'qtd_duplicatas': 10 , 
                        'pct_nulos': pct_nulos , 
                        'pct_duplicatas': 10 , 
                        'tamanho_df': tamanho_df , 
                        'colunas': {coluna: str(df[coluna].dtype) for coluna in colunas}, 
                        
                        }
                    except TypeError as e : 
                        logger.error(f"Erro {str(e)}, tipo não serializável! ")
                        raise EDAErrors(f"Erro {str(e)}, tipo não serializável! ")
            eda_tables_dict[nome] = eda_info
            with open('eda_data.json' ,'w', encoding='utf-8') as f : 
                json.dump(eda_tables_dict , f, ensure_ascii=False, indent=4) 
            logger.info(f'Infomações de EDA referentes a {nome} foram carregadas no arquivo eda_data com sucesso! ')
>>>>>>> data_transforming
