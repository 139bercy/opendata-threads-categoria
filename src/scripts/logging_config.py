import os
import logging
from datetime import datetime

# Vérification et création du répertoire de logs
def configure_logging(log_directory, log_file_name):
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
        
    # Configuration du logging
    timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
    log_file = os.path.join(log_directory, f"{log_file_name}_{timestamp}.log")
    logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')