
data_sources_dict = { 
    'apis': { 
        'FDA_DRUG': 
            {'url': 'https://api.fda.gov/drug/event.json', 
            'paginacao': True ,
            'params': { 
                "search": "receivedate:[20230101+TO+20231231]" ,
                'limit': 1000 , 
                'sort': 'receivedate:asc'
            }}
        
    }
}
