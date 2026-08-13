from src.data_import.data_import import DataImport 
from config.data_dict import data_sources_dict
def main(): 
    importacao = DataImport(data_sources_dict)
    importar = importacao.importar_dados()
    print(importar)
print(main())