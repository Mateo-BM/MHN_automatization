from tkinter import messagebox
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from txt_formats import txt_formats as txt
from pdfread_MHN import pdfread_MHN
import genInvoiceClass as gen
import pdfplumber
import re
import time
import subprocess
from logger_config import logger
from whatsapp_sender import *

def genInvoiceClass(user_Info, pdf_File,SH_flag):
    
    
    gen.open_signumOne()
    
    # Inicializar variables para el txt
    global extracted_tiv,extracted_mail, extracted_legal_id,extracted_user,extracted_password,extracted_regexlist,extracted_pay_order,extracted_date_range,extracted_total_by_line
    extracted_tiv = {}
    extracted_mail = ""
    extracted_legal_id = ""
    extracted_user = ""
    extracted_password = ""
    extracted_regexlist = ""
    driver = None
    extracted_pay_order = ""
    extracted_date_range = ""
    extracted_total_by_line = []
    # Lista de números a los que se enviarán los archivos
    # Configuración
    phone_numbers = ["+50661695369"]  # Números de destino
    destination_folder = r"C:\Users\Administrator\OneDrive - Universidad Fidélitas\Documentos\CMHN_output_online"
    
    #Inicializar configuraciones de chrome
    
    chrome_options = Options()
    output_folder = r"C:\MHN_output"
    prefs = {
        "download.default_directory": output_folder,   # Carpeta de destino
        "download.prompt_for_download": False,       # No preguntar por descarga
        "download.directory_upgrade": True,          # Actualizar automáticamente el directorio
        "safebrowsing.enabled": True                 # Desactivar advertencias de seguridad
            }
    driver_path = 'C:\PythonScripts\MNH\Resources\chromedriver-win64\chromedriver-win64\chromedriver.exe'
        # Ruta del controlador de Chrome
    chrome_options.add_experimental_option("prefs", prefs)
        
        # Configuración de las opciones del navegador Chrome
    chrome_options.add_argument(f"webdriver.chrome.driver={driver_path}")
    try: 
        # Inicia una instancia del navegador Chrome
        driver = webdriver.Chrome(options=chrome_options)
    
        # Extraer la informacion del txt de la credenciales
        regexlist = txt.readJsonRegex()
        extracted_tiv = txt.get_TIV(user_Info,regexlist)
        extracted_mail = txt.get_Mail(user_Info,regexlist)
        extracted_legal_id = txt.get_ID(user_Info,regexlist)
        extracted_user = txt.get_User(user_Info,regexlist)
        extracted_password = txt.get_Password(user_Info,regexlist)
    
        # Extraer la informacion del PDF
    
        results = process_pdf(pdf_File)
        extracted_pay_order = results ["Pay Order"]
        extracted_date_range = results ["Date Range"]
        extracted_total_by_line = results ["Total by Line"]
    
        formatted_totals = "-".join(f" {total}" for total in extracted_total_by_line)
        if SH_flag:
            logger.info(f"The following data were extracted:\n\n"
                        f"Pay order: {extracted_pay_order}\n"
                        f"Date Range: {extracted_date_range}\n"
                        f"Extracted totals: {formatted_totals}\n")
            gen.mhn_automatization(extracted_tiv,extracted_mail,extracted_legal_id,extracted_user,extracted_password,extracted_pay_order,extracted_date_range,extracted_total_by_line,driver,SH_flag,output_folder,destination_folder,phone_numbers)  
        else:
            user_response= messagebox.askyesno("Please confirm",
            f"The following data were extracted:\n\n"
            f"Pay order: {extracted_pay_order}\n"
            f"Date Range: {extracted_date_range}\n"
            f"Extracted totals: {formatted_totals}\n"
            f"Do you confirm this data?")
    
            if user_response:
                gen.mhn_automatization(extracted_tiv,extracted_mail,extracted_legal_id,extracted_user,extracted_password,extracted_pay_order,extracted_date_range,extracted_total_by_line,driver,SH_flag,output_folder,destination_folder,phone_numbers)
            else:
                messagebox.showinfo("Information", "User clicked No.\nExiting...")
    finally:
        # Asegurarse de cerrar el WebDriver si está inicializado
        if 'driver' in locals():
            driver.quit()          

def mhn_automatization(tiv,mail,legal_id,user,password,pay_order,date_range,total_by_line,driver,SH_flag,output_folder,destination_folder,phone_numbers):
    wait = WebDriverWait(driver, 10)
    i = None  # Inicializa una variable para contar las iteraciones
    success = False  # Inicializa una variable para indicar el éxito de la operación
    error_indices = []  # Inicializa una lista para almacenar los índices donde ocurrieron errores

    driver.implicitly_wait(5)
    # Espera implícita

    url = 'https://atv.hacienda.go.cr/ATV/Login.aspx'
    driver.get(url)
    # Abre la URL en el navegador

    wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_cuMensajes_panel')))
    # Espera explícita hasta que el elemento de inicio de sesión esté presente
    
    button_Accept  = driver.find_element(By.ID, 'ContentPlaceHolder1_cuMensajes_btnAceptarMensaje')
    driver.execute_script("arguments[0].click();", button_Accept)
    # Hace clic en el botón de inicio de sesión

    input_usuario = driver.find_element(By.ID, 'ContentPlaceHolder1_txtIdentificacion')
    input_contrasena = driver.find_element(By.ID, 'ContentPlaceHolder1_txtContrasena')
    # Encuentra los elementos de entrada de usuario y contraseña

    input_usuario.clear()
    input_usuario.send_keys(user)
    input_contrasena.clear()
    input_contrasena.send_keys(password)
    # Ingresa el usuario y la contraseña

    time.sleep(2)  # Espera un tiempo

    button_submit = driver.find_element(By.ID, 'ContentPlaceHolder1_btnIngresar')
    driver.execute_script("arguments[0].click();", button_submit)
    # Hace clic en el botón de inicio de sesión
    
    time.sleep(2)  # Espera un tiempo
    
    # Iterar a través de los tres campos
    for i in range(1, 4):  # Para los tres campos
        # Construir los IDs
        if i == 1:
            label_id = f"ContentPlaceHolder1_cuSolicitarTIV_lblPrimerCampo"
            input_id = f"ContentPlaceHolder1_cuSolicitarTIV_TxtPrimerCampo"
        elif i ==2:
            label_id = f"ContentPlaceHolder1_cuSolicitarTIV_lblSegundoCampo"
            input_id = f"ContentPlaceHolder1_cuSolicitarTIV_TxtSegundoCampo"
        elif i ==3:
            label_id = f"ContentPlaceHolder1_cuSolicitarTIV_lblTercercampo"
            input_id = f"ContentPlaceHolder1_cuSolicitarTIV_TxtTercerCampo"
            
    
        # Extraer texto del label
        label_element = driver.find_element(By.ID, label_id)
        label_text = label_element.text.strip()
    
        # Comparar con el diccionario
        if label_text in tiv:
            # Obtener el valor asociado
            value_to_enter = tiv[label_text]
        
            # Encontrar el campo de texto y enviar el valor
            input_element = driver.find_element(By.ID, input_id)
            input_element.clear()  # Limpiar el campo antes de escribir
            input_element.send_keys(value_to_enter)
        
            # print(f"Para el label '{label_text}', se ingresó el valor '{value_to_enter}' en el campo '{input_id}'.")
            #Limpiar las variables label e input
            label_id = ''
            input_id = ''
        else:
            if SH_flag:
                
                logger.error("Error in finding TIV","The text {label_text} is not found in the dictionary..")
            else:
                messagebox.showerror("Error in finding TIV","The text {label_text} is not found in the dictionary..")
                logger.error("Error in finding TIV","The text {label_text} is not found in the dictionary..")
            
            
    button_Continue = driver.find_element(By.ID, 'ContentPlaceHolder1_btnContinuar')
    driver.execute_script("arguments[0].click();", button_Continue)
    # Hace clic en el botón de continuar
    
        # Esperar a que el botón hamburguesa esté presente y buscarlo por el atributo 'title'
    hamburger_button = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Oculta o muestra las opciones del menú']")))

    # Verificar si el menú hamburguesa está visible
    if hamburger_button.is_displayed():
        # Hacer clic en el menú hamburguesa para expandirlo
        hamburger_button.click()
    
    wait.until(EC.presence_of_element_located((By.ID, 'Ul1')))
    
    # Localiza el menú desplegable principal
    voucher = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Comprobantes Electrónicos')]")))
    voucher.click()
    
    # Espera y selecciona "Herramienta Gratuita"
    herramienta_gratuita = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Herramienta Gratuita')]")))
    herramienta_gratuita.click()
    
    # Selecciona finalmente "Facturar"
    free_tool = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Facturar')]")))
    free_tool.click()
    
    document_type = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_26_DDL_TIPOFACT')))
    document_type.click
    
    select_element = Select(document_type)
    # Seleccionar la opción por el valor del atributo 'value'
    select_element.select_by_value("01-Factura electrónica")
    try:
    # En el caso de haber una factura creada como borrador, este va a eliminarla 
        draftInvoice_button = wait.until(EC.presence_of_element_located((By.ID, 'closeBtn')))

    # Verificar si el pop up del draft está visible
        if draftInvoice_button.is_displayed():
            
            driver.execute_script("arguments[0].click();", draftInvoice_button)
            # Hacer click en el boton 'Eliminar documento'
            deleteInvoice_button = wait.until(EC.presence_of_element_located((By.ID, 'eliminar')))
            driver.execute_script("arguments[0].click();", deleteInvoice_button)
            # Hacer click en pop up en el boton 'Si'
            acceptDelete_button = wait.until(EC.presence_of_element_located((By.ID, 'AceptarBtn')))
            driver.execute_script("arguments[0].click();", acceptDelete_button)
            # Hacer click en el pop up en el boton 'Cerrar'
            close_button = wait.until(EC.presence_of_element_located((By.ID, 'closeBtn')))
            driver.execute_script("arguments[0].click();", close_button)
    except:
        print("There is no draft invoice. Continuing with the flow.")
        logger.info("There is no draft invoice. Continuing with the flow")
    # Ckick en drop down de 'tipo de identificación'
    identification_type = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_15_DDL_IDENTIFICACION')))
    identification_type.click
    
    select_element_it = Select(identification_type)
    # Seleccionar la opción por el valor del atributo 'JN-Jurídica Nacional'
    select_element_it.select_by_value("JN-Jurídica Nacional")
    
    # Seleccionar la casilla de 'Número de identificación'
    Identification_number = driver.find_element(By.ID, 'CASILLA_16_TXT')
    Identification_number.clear()
    Identification_number.send_keys(legal_id)
    
    
    
    # Click en la casilla de 'Nombre'
    receiver_name = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_17_TXT')))
    receiver_name.clear()
    receiver_name.send_keys("Trigger")
    time.sleep(2)  # Espera un tiempo
    # # Escribir algunas letras para que se accione la busque de la cedula juridica
    
    # Rellenar la casilla de correo electronico
    e_mail = driver.find_element(By.ID, 'CASILLA_25_TXT')
    e_mail.clear()
    e_mail.send_keys(mail)
    
    # Click en drop down de 'Condición de la Venta'
    sale_condition = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_30_DDL_CONDVENTA')))
    sale_condition.click
    
    select_element_sc = Select(sale_condition)
    # Seleccionar la opción por el valor del atributo '01-Contado'
    select_element_sc.select_by_value("01-Contado")
    
    # Seleccionar el check box 'Transferencia – depósito bancario'
    checkbox_bankDeposit = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='checkbox' and @value='04']")))
    if not checkbox_bankDeposit.is_selected():
        checkbox_bankDeposit.click()
    
    # Click en drop down de 'Condición de la Venta'
    money_type = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_34_DDL_MONEDA')))
    money_type.click
    
    select_element_mt = Select(money_type)
    # Seleccionar la opción por el valor del atributo '01-Contado'
    select_element_mt.select_by_value("1-CRC-Colón costarricense")
    
    # Seleccionar el boton 'Guardar encabezado'
    header_button = wait.until(EC.presence_of_element_located((By.ID, 'guardarEncabezado')))
    driver.execute_script("arguments[0].scrollIntoView(true);", header_button)

    driver.execute_script("arguments[0].click();", header_button)
    
    time.sleep(1) # Espera un tiempo
    
    # Click en el botón que se despliega luego de oprimir 'Guardar encabezado'
    popUp_button = wait.until(EC.presence_of_element_located((By.ID, 'closeBtn')))
    driver.execute_script("arguments[0].click();", popUp_button)
    
    for each_total in total_by_line:
        time.sleep(1)
        #--------------------------------#
        ##### Datos Detalle factura #####
        #--------------------------------#
    
        # Click en drop down de 'Código Bien / Servicio CAByS:'
        cabys_service = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_362_DDL_CODIGOHACIENDA')))
        cabys_service.click
    
        select_element_cs = Select(cabys_service)
        # Seleccionar la opción por el valor del atributo '6511900009900-6511900009900-Servicios de transporte'
        select_element_cs.select_by_value("6511900009900-6511900009900-Servicios de transporte terrestre de carga, n.c.p.")
    
        # Click en drop down de 'Tipo de Código'
        code_type = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_36_DDL_TIPOCODIGO')))
        code_type.click
    
        select_element_ct = Select(code_type)
        # Seleccionar la opción por el valor del atributo '3-Código del producto asignado por la industria'
        select_element_ct.select_by_value("3-Código del producto asignado por la industria")
    
        # Rellenar la casilla de 'Código'
        code_detail = driver.find_element(By.ID, 'codigo')
        code_detail.clear()
        code_detail.send_keys(pay_order)
    
        # Rellenar la casilla de 'Descripción de la Linea'
        description_detail = driver.find_element(By.ID, 'descripcion')
        description_detail.clear()
        driver.execute_script("arguments[0].value = arguments[1];", description_detail, date_range)
    
        # Click en drop down de 'Unidad de Medida'
        measure_detail = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_39_DDL_UNIDADMEDIDA')))
        measure_detail.click
    
        select_element_md = Select(measure_detail)
        # Seleccionar la opción por el valor del atributo '3-Código del producto asignado por la industria'
        select_element_md.select_by_value("1-Sp-Servicios Profesionales")
    
        # Rellenar la casilla de 'Descripción de la Linea'
        amountLine_detail = driver.find_element(By.ID, 'cantidadLinea')
        amountLine_detail.clear()
        amountLine_detail.send_keys("1") # revisar si se puede poner como int directamente
    
        # Rellenar la casilla de 'Precio Unitario'
        price_unit = driver.find_element(By.ID, 'precioUnitario')
        price_unit.clear()
        driver.execute_script("arguments[0].value = arguments[1];", price_unit, each_total)
    
        #--------------------------------#
        ##### Impuestos y Exoneraciones ##### 
        #--------------------------------#
    
        # Click en drop down de 'Tipo impuesto'
        tax_type = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_451_DDL_IMPUESTOSEXCEPCIONES')))
        tax_type.click
    
        select_element_tt = Select(tax_type)
        # Seleccionar la opción por el valor del atributo '3-Código del producto asignado por la industria'
        select_element_tt.select_by_value("01-Impuesto al Valor Agregado")
        
        # Click en drop down de 'Código Tarifa'
        rate_code = wait.until(EC.presence_of_element_located((By.ID, 'CASILLA_4511_DDL_CODIGOTARIFA')))
        driver.execute_script("arguments[0].scrollIntoView(true);", rate_code)
        rate_code.click
    
        select_element_rc = Select(rate_code)
        # Seleccionar la opción por el valor del atributo '08-Tarifa general 13%'
        select_element_rc.select_by_value("08-Tarifa general 13%")
        
        # Click en el botón 'Guardar impuesto'
        button_save_tax = wait.until(EC.presence_of_element_located((By.ID, 'GuardarImpuesto')))
        driver.execute_script("arguments[0].click();", button_save_tax)
        
        # Click en el botón 'Guardar impuesto'
        button_save_line = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Guardar Linea']")))
        driver.execute_script("arguments[0].click();", button_save_line)
        
        # Click en el botón que se despliega luego de oprimir 'Guardar linea'
        popUp_button = wait.until(EC.presence_of_element_located((By.ID, 'closeBtn')))
        driver.execute_script("arguments[0].click();", popUp_button)
        
    # Click en el botón que valida todo lo anterior 'Validar y firmar'
    button_validate= wait.until(EC.presence_of_element_located((By.ID, 'validar')))
    driver.execute_script("arguments[0].click();", button_validate)
    
    # Click en el botón que se despliega luego de oprimir 'Validar y firmar'
    popUp_validate_button = wait.until(EC.presence_of_element_located((By.ID, 'AceptarBtn')))
    driver.execute_script("arguments[0].click();", popUp_validate_button)
    
    # Click en el botón que se despliega luego de oprimir 'Sí'
    popUp_finish_button = wait.until(EC.presence_of_element_located((By.ID, 'closeBtn')))
    driver.execute_script("arguments[0].click();", popUp_finish_button)
    
    # Click en el botón 'Salir' que cierra la sesion de MHN 
    closeSesion_button = wait.until(EC.presence_of_element_located((By.ID, 'ContentPlaceHolder1_lblSalir')))
    driver.execute_script("arguments[0].click();", closeSesion_button)
    if SH_flag:
        logger.info("************** End of automatization, the process has been successfully completed **************")
        ## Enviar los resultados del folder MHN_output
        whatsapp_sender(phone_numbers, output_folder, destination_folder)
    else:
        messagebox.showinfo("End of automatization", "The process has been successfully completed")
        logger.info("************** End of automatization, the process has been successfully completed **************")
        ## Enviar los resultados del folder MHN_output
        whatsapp_sender(phone_numbers, output_folder, destination_folder)
def process_pdf(file_path):
    
    # Procesa un PDF y utiliza las funciones de búsqueda para extraer la información necesaria.
    
    with pdfplumber.open(file_path) as pdf:
        # Inicializar variables para el PDF
        pay_order = None
        date_range = None
        total_by_line = []
        

        for page in pdf.pages:
            text = page.extract_text()
            tables = page.extract_tables()

            if not pay_order:
                pay_order = pdfread_MHN.get_payorder(text)

            if not date_range:
                date_range = pdfread_MHN.get_date_range(text)

            total_by_line.extend(pdfread_MHN.get_total_prices(tables))

        return {
            "Pay Order": pay_order,
            "Date Range": date_range,
            "Total by Line": total_by_line
        }
        
def open_signumOne():
        
    # Ruta fija de la aplicación
    app_path = r"C:\Program Files\SignumOne-KS\SignumOne-KS.exe"

    # Abrir la aplicación
    try:
        subprocess.Popen(app_path)  # Lanza la aplicación sin bloquear el script
        logger.info(f"Application successfully started since {app_path}")
    except FileNotFoundError:
        logger.error(f"The application was not found in the path: {app_path}")
    except Exception as e:
        logger.error(f"An error occurred while trying to start the application: {e}")







