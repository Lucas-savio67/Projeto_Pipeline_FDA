import os 
from dotenv import load_dotenv 
load_dotenv()
def data_source_dict():
    data_sources_dict = { 
        'apis': { 
            'FDA_DRUG': 
                {'url': 'https://api.fda.gov/drug/event.json', 
                'paginacao': True ,
                'params': { 
                    "search": "receivedate:[20230101 TO 20231231]" ,
                    'limit': 1000 , 
                    'sort': 'receivedate:asc' , 
                    'api_key': os.getenv("API_KEY_FDA")
                } ,
                'max_paginas': 3}
        
        }
    }
    return data_sources_dict
