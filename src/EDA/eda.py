import logging 
logger = logging.getLogger(__name__)
import pandas as pd
import json 
from pathlib import Path 
class EDAErrors(Exception): 
    pass
class EDA: 
    def __init__(self, tabelas:dict[str,list[dict[str,pd.DataFrame]]]) -> None : 
        self.tabelas = tabelas 
    def fazer_eda_tabelas(self) -> str: 
        output_file = Path('eda_data.json')
        output_file.touch(exist_ok=True)
        if not self.tabelas: 
            logger.error('Erro, nenhuma tabela encontrada! ')
            raise EDAErrors("Erro, nenhuma tabela encontrada! ")
        
        eda_info = {}
        eda_tables_dict = {}
        for nome, tabelas in self.tabelas.items(): 
            logger.info(f"Começando o EDA de tabelas referentes a {nome}... ")
            for conteudo in tabelas : 
                for nome_tabela, df in conteudo.items(): 
                    logger.info(f'Fazendo o EDA da tabela: {nome_tabela}... ')
                    qtd_nulos = df.isna().sum().sum() 
                    qtd_duplicatas = df.duplicated().sum() 
                    pct_nulos = qtd_nulos / len(df) * 100 
                    pct_duplicatas = qtd_duplicatas / len(df) * 100 
                    tamanho_df = len(df) 
                    colunas =  df.columns
                    informacao_essencial = df.info() 
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
            with open('eda_data.json' ,'w', encoding='utf-8') as f : 
                json.dumps(eda_tables_dict , f, ensure_ascii=False, indent=4) 
            logger.info(f'Infomações de EDA referentes a {nome} foram carregadas no arquivo eda_data com sucesso! ')