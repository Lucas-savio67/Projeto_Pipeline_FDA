from src.data_import.data_import import DataImport 
from config.data_dict import data_source_dict
from config.loggings import logging
def main(): 
    data_sources = data_source_dict()
    importacao = DataImport(data_sources)
    importar = importacao.importar_apis()
    print(importar)
print(main())