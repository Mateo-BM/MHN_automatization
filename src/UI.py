import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from genInvoiceClass import genInvoiceClass
from ServiceHandler import serviceHandler
import re
import sys

# test = True
if len(sys.argv) > 1 and sys.argv[1].lower() == "true":
        # lógica para manejar facturas sin asistencia de usuario
        serviceHandler()
else:
    # Lógica para el modo manual
    def seleccionar_archivo():
        # Seleccionar un archivo .xls
        archivo = filedialog.askopenfilename(
            title="Select PDF file",
            filetypes=[("PDF files", "*.pdf")]
        )
        if archivo:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, archivo)
        
    def seleccionar_txt():
        # Seleccionar un archivo .txt
        txtfile = filedialog.askopenfilename(
            title="Select txt file",
            filetypes=[("Text files", "*.txt")]
        )
        if txtfile:
            file_txt.delete(0, tk.END)
            file_txt.insert(0, txtfile)

    def extraer_datos():
        # Obtener valores ingresados
        pdf_File = file_entry.get()
        txt_file_path = file_txt.get()
        with open(txt_file_path, 'r') as file:
            lines = file.readlines()

    
        if not pdf_File:
            messagebox.showerror("Error", "Please select a PDF file.")
            return
    
        if not txt_file_path:
            messagebox.showerror("Error", "Please select a TXT file.")
            return

        try:
            SH_flag = False
            genInvoiceClass(lines,pdf_File,SH_flag)
        

        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while processing the file:\n{e}")
        
        

    # Crear la ventana principal
    window = tk.Tk()
    window.title("ATV - Tool to generate invoice's")
    window.geometry("400x400")


    # Botón para seleccionar archivo
    tk.Label(window, text="PDF file:").pack(pady=5)
    file_entry = tk.Entry(window, width=40)
    file_entry.pack(pady=5)
    file_button = tk.Button(window, text="Select", command=seleccionar_archivo)
    file_button.pack(pady=5)

    # Botón para seleccionar archivo
    tk.Label(window, text="Text file:").pack(pady=5)
    file_txt = tk.Entry(window, width=40)
    file_txt.pack(pady=5)
    file_button_txt = tk.Button(window, text="Select", command=seleccionar_txt)
    file_button_txt.pack(pady=5)

    # Botón para procesar datos
    start_button = tk.Button(window, text="Start automatization", command=extraer_datos)
    start_button.pack(pady=20)

    # Iniciar el bucle principal de la ventana
    window.mainloop()