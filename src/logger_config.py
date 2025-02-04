import logging
import os
from logging.handlers import RotatingFileHandler

class LoggerConfig:
    LOG_DIR = r"C:\MHN"  # Carpeta donde se guardarán los logs
    LOG_FILE = os.path.join(LOG_DIR, "appMHN.log")  # Ruta del archivo de log

    @staticmethod
    def setup_logger():
        """Configura el logger globalmente."""

        # Crear la carpeta si no existe
        if not os.path.exists(LoggerConfig.LOG_DIR):
            os.makedirs(LoggerConfig.LOG_DIR)

        # Configurar logger
        logger = logging.getLogger("AppLogger")
        logger.setLevel(logging.DEBUG)  # Captura todos los niveles de logs

        # Formato de los logs
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

        # Handler para rotación de logs (máx. 5 MB, 3 copias de respaldo)
        file_handler = RotatingFileHandler(LoggerConfig.LOG_FILE, maxBytes=5*1024*1024, backupCount=3)
        file_handler.setFormatter(formatter)

        # Handler para mostrar logs en consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        # Agregar los handlers al logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        return logger

# Crear el logger globalmente
logger = LoggerConfig.setup_logger()

