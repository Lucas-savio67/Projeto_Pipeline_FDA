regras_limpeza = { 
    'apis': { 
        'FDA_DRUG': { 
            'parte essencial': 'results',
            'tabelas a parte': { 
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