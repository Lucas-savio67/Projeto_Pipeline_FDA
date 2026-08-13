from src.data_import.data_import import DataImport 
from config.data_dict import data_sources_dict
from config.loggings import logging
def main(): 
    importacao = DataImport(data_sources_dict)
    importar = importacao.importar_apis()
    print(importar)
print(main())