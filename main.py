import boto3
from src.data_import.data_import import DataImport 
from src.data_ingestion.data_ingestion import DataIngestion
from src.data_extraction.data_extraction import DataExtraction
from config.data_dict import data_source_dict
from config.loggings import logging
from config.load_s3_info import load_s3_info, LoadingErrors
def main(): 
    try :
        info_s3 = load_s3_info()
        s3_client = boto3.client('s3', 
                            aws_access_key_id=info_s3['chave_acesso'], 
                            aws_secret_access_key=info_s3['chave_secreta'], 
                            region_name=info_s3['região'])
        data_sources = data_source_dict()
        importacao = DataImport(data_sources, s3_client, info_s3['bucket'])
        importar = importacao.importar_apis()
        ingestao = DataIngestion(importar)
        injetar = ingestao.injetar_dados()
        extracao = DataExtraction(s3_client, info_s3['bucket'])
        extrair = extracao.extrair_dados()
        print(extrair)
    except LoadingErrors as e : 
        return e
print(main())