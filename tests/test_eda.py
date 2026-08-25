import pandas as pd
from src.eda.eda import EDA, EDAErrors 
from unittest.mock import mock_open, patch
def test_success_eda(): 
    data = {'FDA_DRUG': [{'tabela_1': pd.DataFrame({'coluna_1': ['linha_1', 'linha_2', 'linha_3']})}]}
    eda = EDA(data) 
    with patch('pathlib.Path.touch'), patch('builtins.open', mock_open()) as m_open, patch('json.dump') as m_dump:
        resultado = eda.fazer_eda_tabelas()
    m_open.assert_called()
    m_dump.assert_called()
    assert resultado == {'FDA_DRUG': {'tabela_1':{'qtd_nulos': 0  ,
                                                'qtd_duplicatas': 0 , 
                                                'pct_nulos': 0 ,
                                                'pct_duplicatas': 0 , 
                                                'tamanho_df': 3 , 
                                                'colunas': ['coluna_1'] , 
                                                'info_essencial': { 
                                                    'coluna_1': 'str'
                                                }}}}