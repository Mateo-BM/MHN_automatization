from logger_config import logger
import os
from genInvoiceClass import genInvoiceClass
def serviceHandler ():
    try:
        SH_flag = True
        logger.info("Automation Mode: Executing invoices by Alexa instruction....")  
        # De forma quemada pasar el .txt de las credenciales y el TIV (En OneDrive para hacerlo mas accesible por medio de telefono)
        credential_txt = r"C:\Users\Administrator\OneDrive - Universidad Fidélitas\THEODORO\Factura\Factura.txt"
        with open(credential_txt, 'r') as file:
            lines = file.readlines()
            
        # Obtener todos los archivos .csv en la carpeta de salida (En OneDrive para hacerlo mas accesible por medio de telefono)
        DaemonTask_folder = r"C:\Users\Administrator\OneDrive - Universidad Fidélitas\THEODORO\Factura\DaemonTaskMHN_folder"
        pdf_files = [f for f in os.listdir(DaemonTask_folder) if f.endswith('.pdf')]
        
        if not pdf_files:
            logger.error("No CSV files to process.",exc_info=True)
            return
        
        # Leer y combinar cada archivo CSV
        for file in pdf_files:
            file_path = os.path.join(DaemonTask_folder, file)
            genInvoiceClass(lines,file_path,SH_flag)
            
    except Exception as e:
        logger.error("An error occurred in the process",exc_info=True)
        
    finally:
        logger.info("=== Application completed ===")
        