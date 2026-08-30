from src.data_structuring.data_structuring import DataStructuring,StructuringErrors 
from typing import Any
import pandas as pd 
def test_success_main_structuring(): 
    api = {'meta': 'metadata','results': [{'results_1':'result'}]}
    regras_limpeza = { 
    'apis': { 
        'FDA_DRUG': { 
            'nome_tabela_principal': 'eventos' , 
            'local_registros': 'results',
            'tabelas_a_parte': { 
                'reaction': { 
                    'record_path': ['patient', 'reaction'], 
                    'meta': ['safetyreportid']
                } , 
                'drug': { 
                    'record_path': ['patient','drug'] ,
                    'meta': ['safetyreportid'] 
                }

                }
            } 
        }
    }
    regra_api = regras_limpeza['apis']['FDA_DRUG']
    estruturacao = DataStructuring(api ,regras_limpeza ) 
    estruturar = estruturacao.estruturar_tabela_principal(api , regra_api)

    assert list(estruturar[0].keys()) == ['eventos']
    assert estruturar[0]['eventos'].to_dict(orient='records') == [{'results_1': 'result'}]
    assert estruturar[1] == {}