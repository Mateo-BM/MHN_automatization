import re
import pdfplumber
from txt_formats import txt_formats as txt


    # pdf_path = "C:/Users/Administrator/Downloads/OrdenPagoGrupoTLACR00029362EN251.pdf"
class pdfread_MHN:
    global regexlist
    regexlist = txt.readJsonRegex()

    def get_payorder(text):
        # Buscar "Orden de Pago"
        match_orden = re.search(regexlist["PDF MNH"]["regex_orden_pago"], text)
        
        return  match_orden.group(1)
    
    def get_date_range(text):
        # Buscar "Rango de Fechas"
            
        match_rango = re.search(regexlist["PDF MNH"]["regex_rango_fechas"], text)

        return match_rango.group(0)
    
    def get_total_prices(tables):
        total_prices = []
        # Buscar precios en la columna "Total a Pagar"
            
        for table in tables:
            if "Total a Pagar" in table[0]:
                headers = table[0]  # La primera fila contiene los encabezados
                index = 1
            else:
                headers = table[1]  # La segunda fila contiene los encabezados
                index = 2
            total_idx = headers.index("Total a Pagar")  # Índice de la columna "Total a Pagar"
            for row in table[index:]:  # Iterar sobre las filas, omitir encabezados
                price = row[total_idx].strip()
                if re.match(regexlist["PDF MNH"]["regex_precio_total"], price):  # Validar con regex
                    total_prices.append(price)
            
        return total_prices

# # Imprimir resultados
# print("Orden de Pago:", payment_order)
# print("Rango de Fechas:", date_range)
# print("Precios Totales (Total a Pagar):", total_prices)
