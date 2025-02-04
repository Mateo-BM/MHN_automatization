import re
import json
import os
class txt_formats:
    
    
    def readJsonRegex():
        
        try: 
            with open ("Regex.json", "r") as read_file:
                data = json.load(read_file)
        
                return data
    
        except:
            print("Something is wrong with the reading of the Json file")


    def get_TIV (txt_Info,regexlist):
        
        for i, line in enumerate(txt_Info):
            line = line.strip()
            # Extraer el diccionario TIV
            if re.match(regexlist["Txt"]["search_TIV"], line):  # Detectar la fila del encabezado
                headers = line.split()
                values = txt_Info[i + 1].strip().split()
                tiv = dict(zip(headers, values))
        
        return tiv

    def get_Mail (txt_Info,regexlist):
        for i, line in enumerate(txt_Info):
            line = line.strip()
    
            if line.startswith(regexlist["Txt"]["search_Mail"]):
                mail = txt_Info[i + 1].strip()
            
                return mail

    def get_ID (txt_Info,regexlist):
        for i, line in enumerate(txt_Info):
            line = line.strip()

            if line.startswith(regexlist["Txt"]["search_Id"]):
                legal_id = txt_Info[i + 1].strip()
        
                return legal_id

    def get_User (txt_Info,regexlist):
        for i, line in enumerate(txt_Info):
            line = line.strip()
        
            if line.startswith(regexlist["Txt"]["Search_User"]):
                user = txt_Info[i + 1].strip()
                return user

    def get_Password (txt_Info,regexlist):
        for i, line in enumerate(txt_Info):
            line = line.strip()
        
            if line.startswith(regexlist["Txt"]["Search_Password"]):
                password = txt_Info[i + 1].strip()
        
                return password


