regras_limpeza = { 
    'apis': { 
        'FDA_DRUG': { 
            'tipo_api': 'lista' ,
            'parte essencial': 'results',
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