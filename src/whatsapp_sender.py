import os
import shutil
import pywhatkit as kit
import pyautogui
from datetime import datetime
import time

def whatsapp_sender(phone_numbers, source_folder, destination_folder):
    """
    Sends a WhatsApp message notifying that the files were generated.
    and copies the files to another folder.
    """
    try:
        # Obtener lista de archivos en la carpeta de salida
        files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
        
        if not files:
            print("No files to notify.")
            return
        
        # Enviar mensaje por WhatsApp a cada número
        for number in phone_numbers:
            message = "\n".join([f"Invoice {file} were generated" for file in files])
            
            # Obtener la hora actual para enviar el mensaje inmediatamente
            now = datetime.now()
            hour, minute = now.hour, now.minute + 1  # Enviar en el siguiente minuto
            
            kit.sendwhatmsg(number, message, hour, minute, wait_time=10)
            
            # Esperar un momento para asegurar que la ventana está lista
            time.sleep(5)
            
            # Simular presionar 'Enter' para enviar el mensaje
            pyautogui.press('enter')
            
            print(f"Mensaje enviado a {number}")
        
        # Mover archivos a la carpeta destino
        for file in files:
            shutil.move(os.path.join(source_folder, file), os.path.join(destination_folder, file))
        print("Archivos movidos correctamente.")
    
    except Exception as e:
        print(f"Error: {e}")

