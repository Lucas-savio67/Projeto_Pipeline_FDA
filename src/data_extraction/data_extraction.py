import logging
import json
from typing import Any
from mypy_boto3_s3.client import S3Client 
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)
class ExtractionErrors(Exception): 
    pass
class DataExtraction : 
    def __init__(self, client:S3Client, bucket:str) -> None : 
        self.extracted_data : dict[str, dict[str,Any]] = {}
        self.client = client 
        self.bucket= bucket
    def extrair_dados(self) -> dict[str, dict[str,Any]]: 
        conteudo_extraido = {}
        erros = {}
        logger.info("Começando o fluxo de extração dos objetos no bucket S3! ")
        paginator = self.client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket = self.bucket, Prefix='bronze/'): 
            for obj in page.get('Contents', []): 
                try :
                    key = obj['Key']
                    if key.endswith('.json'): 
                            data_api = self.extrair_dados_apis(key)
                            self.extracted_data.setdefault('apis', {})[key] = data_api
                except ExtractionErrors as e : 
                    logger.warning(str(e))
                    erros[key] = {'erro': str(e)}
        apis = self.extracted_data.get('apis', {})
        logger.info("O fluxo de extração terminou! ")
        if erros :
            logger.info(f"Arquivos com erro: {erros}")
        for nome_dado, valor_extraido in self.extracted_data.items(): 
            conteudo_extraido[nome_dado] = list(valor_extraido.keys())
        logger.info(f"Arquivos extraídos com sucesso: {conteudo_extraido}")
        return self.extracted_data
            
    def extrair_dados_apis(self, key:Any) -> dict[str,Any]: 
        try :
            extracted_apis = {}
            response = self.client.get_object(Bucket=self.bucket, Key=key)
            conteudo = response['Body'].read()
            extracted_apis[key] = json.loads(conteudo)
            logger.info(f"Key: {key} extraída com sucesso! ")
            return extracted_apis
            
        except ClientError as e : 
            codigo = e.response['Error']['Code']
            if codigo == 'NoSuchKey':
                raise ExtractionErrors(f'Objeto não existe mais: {key}')
            elif codigo == 'AccessDenied':
                raise ExtractionErrors(f'Sem permissão para acessar: {key}')
            elif codigo == 'NoSuchBucket':
                raise ExtractionErrors(f'Bucket não existe: {self.bucket}')
            else:
                raise ExtractionErrors(f'Erro S3 ({codigo}): {key}')
        except json.JSONDecodeError as e : 
            raise ExtractionErrors(f'JSON inválido para a key: {key}! ')
        
