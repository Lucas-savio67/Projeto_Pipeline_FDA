import logging
logging.basicConfig(
    level=logging.INFO , 
    format="%(asctime)s - %(levelname)s - %(message)s" , 
    filemode='w' ,
    filename='logs/pipeline.logs'
)