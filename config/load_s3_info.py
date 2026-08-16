import logging 
logger = logging.getLogger(__name__)
import os 
from typing import Any
from dotenv import load_dotenv
load_dotenv()
class LoadingErrors(Exception): 
    pass
def load_s3_info() -> dict[str, Any]: 
    information = {'bucket': os.getenv("AWS_BUCKET_NAME"), 
                    'chave_acesso': os.getenv("AWS_ACCESS_KEY_ID") ,
                    'chave_secreta': os.getenv("AWS_SECRET_ACCESS_KEY") ,
                    'região': os.getenv("AWS_REGION")}
    for nome, info in information.items(): 
        if info is None : 
            logger.error(f"Erro, a variável de ambiente {nome} retornou None! ")
            raise LoadingErrors(f"Erro, a variável de ambiente {nome} retornou None! ")
    return information