from src.data_import.data_import import DataImport 
from src.data_ingestion.data_ingestion import DataIngestion
from src.data_extraction.data_extraction import DataExtraction
from config.data_dict import data_source_dict
from config.loggings import logging
def main(): 
    data_sources = data_source_dict()
    importacao = DataImport(data_sources)
    importar = importacao.importar_apis()
    ingestao = DataIngestion(importar)
    injetar = ingestao.injetar_dados()
    extracao = DataExtraction()
    extrair = extracao.extrair_dados()
    print(extrair)
print(main())