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
def test_success_separate_table_structuring(): 
    api = {'meta': 'metadata','results': [{'safetyreportid': 'id' ,'results_1':'result' , 'drug': [{'drug_1': 'drugs'}] , 'reaction': [{'reaction_1': 'reactions'}]}]}
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

    estruturar = estruturacao.criar_tabelas_novas(api , regra_api)
    assert estruturar[0] == {}
    assert set(estruturar[1].keys()) == {'reaction', 'drug'}
    assert estruturar[1]['reaction']['erro'] == "'patient'"
    assert estruturar[1]['drug']['erro'] == "'patient'"
def test_obter_conteudo(): 
    api = [{'meta': 'metadata','results': [{'safetyreportid': 'id' ,'results_1':'result' , 'drug': [{'drug_1': 'drugs'}] , 'reaction': [{'reaction_1': 'reactions'}]}]}]
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
    conteudo = estruturacao.obter_conteudo(api, regra_api) 
    assert conteudo == api[0]