from src.data_structuring.data_structuring import DataStructuring,StructuringErrors 
from typing import Any
import pandas as pd 
def test_success_main_table_structuring(): 
    extracted_data = {'apis': {'FDA_DRUG': {'data': [1,2,3] , 'status': 'success'}}}
    cleaning_rules = { 
    'apis': { 
        'FDA_DRUG': { 
            'nome_tabela_principal': 'eventos' , 
            'tipo_api': 'lista' ,
            'parte_essencial': 'results',
            'tabelas_a_parte': { 
                'reaction': { 
                    'record_path': ['patient', 'reaction'], 
                    'meta': ['safetyreportid']
                } , 
                'drug': { 
                    'record_path': ['patient','drug'] ,
                    'meta': ['safetyreportid'] 
                } ,

                }
            } 
        }
    }
    api = [{'results' :[{'id': '1'}]}]
    regra_api = cleaning_rules['apis']['FDA_DRUG']
    estruturacao =DataStructuring(extracted_data, cleaning_rules)
    estruturar = estruturacao.estruturar_tabela_principal(api,regra_api) 
    assert estruturar["eventos"].to_dict(orient="records") == [
        {"id": "1"}
    ]
