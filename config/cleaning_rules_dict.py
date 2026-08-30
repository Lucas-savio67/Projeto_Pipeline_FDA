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
