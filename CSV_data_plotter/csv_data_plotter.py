######################################################################################################################################
#                                                                                                                                    #
#                           CSV DATA PLOTTER ANALYZER V1                                                                             # 
#                                    05/07/2024                                                                                      #
#                            By Daniel Gutiérrez Torres                                                                            #
#                                                                                                                                    #    
######################################################################################################################################

import csv
import sys
import os
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox, QVBoxLayout, QWidget, QSizePolicy, QTableWidget, QTableWidgetItem, QSpacerItem, QScrollArea, QMessageBox
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
from statistics import mean, stdev
import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import Alignment

class Ventana(QWidget):

    def __init__(self):
        super().__init__()

        # equivalencias ID <-> parámetro
        self.ID_TO_PARAM = {
            1: 'engine_temp_value',
            2: 'Batery_volt_value',
            3: 'brake1_temp_value',
            4: 'brake2_temp_value',
            5: 'brake3_temp_value',
            6: 'brake4_temp_value',
            7: 'gear_value',
            8: 'speed_value',
        }

        self.graficas = {} 

        self.initUI()

    def initUI(self):

        # Configuración de la ventana
        self.setGeometry(50, 50, 1100, 500) 
        self.setWindowTitle('CSV data plotter analyzer')

        # PLANTILLA
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 60)
        self.setLayout(layout)

        # TÍTULO
        titulo_label = QLabel('CSV Data Plotter Analyzer', self)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        titulo_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))  
        layout.addWidget(titulo_label, Qt.AlignmentFlag.AlignHCenter)

        # Spacer para añadir espacio debajo de los botones
        spacer1 = QSpacerItem(0, 25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addItem(spacer1)

        # INPUT CSV
        input_ruta = QHBoxLayout()

        input_ruta.addSpacing(120)

        # Crear y añadir el QLabel
        input_label = QLabel('Upload CSV:', self)
        input_label.setStyleSheet("QLabel { font-size: 14px; }")
        input_ruta.addWidget(input_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Crear y añadir el QLineEdit
        self.ruta_input = QLineEdit(self)
        self.ruta_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        input_ruta.addWidget(self.ruta_input)

        # Crear y añadir el QPushButton
        btn_subir_csv = QPushButton('Subir CSV', self)
        btn_subir_csv.clicked.connect(self.abrir_dialogo_csv)
        btn_subir_csv.setStyleSheet("padding: 5px 20px;")
        input_ruta.addWidget(btn_subir_csv)

        input_ruta.addSpacing(50)

        # Añadir el layout horizontal al layout principal
        layout.addLayout(input_ruta)

        # Spacer para añadir espacio debajo de los botones
        spacer2 = QSpacerItem(0, 15, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addItem(spacer2)

        #BOTONES
        # Layout horizontal para los botones
        layout_botones = QHBoxLayout()

        # Espacio entre los botones 
        layout_botones.addSpacing(170)

        # Botón para cargar los datos del archivo
        btn_cargar_datos = QPushButton('Visualize Data', self)
        btn_cargar_datos.clicked.connect(self.cargar_datos)
        btn_cargar_datos.setStyleSheet("QPushButton { padding: 8px 20px; font-size: 14px; }" "QPushButton:checked { font-weight: bold; }") 
        layout_botones.addWidget(btn_cargar_datos)

        # Espacio entre los botones
        layout_botones.addSpacing(50)

        # Botón para subir datos a Google Drive
        btn_drive_upload = QPushButton('Upload to Google Drive', self)
        btn_drive_upload.clicked.connect(self.upload_google_drive)
        btn_drive_upload.setStyleSheet("QPushButton { padding: 8px 20px; font-size: 14px; }") 
        layout_botones.addWidget(btn_drive_upload)

        # Espacio entre los botones
        layout_botones.addSpacing(50)

        # Botón para generar informe en Excel
        btn_pdf = QPushButton('Generate Excel', self)
        btn_pdf.clicked.connect(self.generate_excel_report)
        btn_pdf.setStyleSheet("QPushButton { padding: 8px 20px; font-size: 14px; }")  
        layout_botones.addWidget(btn_pdf)

        # Espacio entre los botones
        layout_botones.addSpacing(50)

        # Botón para generar informe en PDF
        btn_pdf = QPushButton('Generate PDF', self)
        btn_pdf.clicked.connect(self.generate_pdf_report)
        btn_pdf.setStyleSheet("QPushButton { padding: 8px 20px; font-size: 14px; }")  
        layout_botones.addWidget(btn_pdf)

        # Espacio entre los botones
        layout_botones.addSpacing(120)

        # Añadir el layout horizontal de los botones al layout principal
        layout.addLayout(layout_botones)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Spacer para añadir espacio debajo de los botones
        spacer3 = QSpacerItem(0, 25, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        layout.addItem(spacer3)

        #OUTPUT GRÁFICAS Y TABLAS

        # Widget scrollable para las tablas
        self.scroll_content = QWidget()
        self.layout_tablas = QVBoxLayout(self.scroll_content)
        
        # Crear un área de scroll
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setFixedHeight(620)
        self.scroll_area.hide()

        # Agregar el área de scroll al layout principal
        layout.addWidget(self.scroll_area)

        # IMG fondo
        self.backgroundLogo = QLabel(self)
        self.backgroundLogo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_script = os.path.dirname(os.path.abspath(__file__))  
        ruta_imagen = os.path.join(ruta_script, 'assets/IMG_fondo.PNG') 
        pixmap = QPixmap(ruta_imagen)  
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
        self.backgroundLogo.setPixmap(pixmap)
        layout.addWidget(self.backgroundLogo)

    ruta_to_input = ""

    def abrir_dialogo_csv(self):
        # Abrir un diálogo para seleccionar archivo CSV
        archivo_csv, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "Archivos CSV (*.csv)")
        
        if archivo_csv:
            self.ruta_to_input = archivo_csv
            self.ruta_input.setText(archivo_csv)
            #print(f"Ruta del archivo seleccionado: {self.ruta_input}")

    def generate_excel_report(self):
        if self.ruta_to_input is None:
            return  # O podrías optar por lanzar una excepción si lo prefieres

        # Leer el archivo CSV
        self.csv_data = pd.read_csv(self.ruta_to_input, header=None, names=['ID', 'Value', 'Timestamp'])

        with pd.ExcelWriter('output.xlsx', engine='openpyxl') as writer:
            # Bandera para verificar si se añadió al menos una hoja
            sheet_added = False
            
            for param_id, param_name in self.ID_TO_PARAM.items():
                # Filtrar los datos por ID
                df_filtered = self.csv_data[self.csv_data['ID'] == param_id]
                if not df_filtered.empty:
                    # Renombrar la columna 'Value' a nombre del parámetro
                    df_filtered = df_filtered[['Value', 'Timestamp']]
                    df_filtered.rename(columns={'Value': param_name}, inplace=True)
                    # Escribir en la hoja correspondiente
                    df_filtered.to_excel(writer, sheet_name=param_name, index=False)
                    sheet_added = True
            
            # Si no se ha añadido ninguna hoja, agregar una hoja predeterminada
            if not sheet_added:
                pd.DataFrame({'Message': ['No data available for the given parameters']}).to_excel(writer, sheet_name='No Data', index=False)

        # Abrir el archivo de nuevo para modificar el estilo
        workbook = load_workbook('output.xlsx')
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]
            for row in sheet.iter_rows():
                for cell in row:
                    cell.alignment = Alignment(horizontal='center', vertical='center')

        workbook.save('output.xlsx')
        
    def upload_google_drive(self, nombre):
        return
    
    def generate_pdf_report(self, nombre):
        return

    def cargar_datos(self):
        file_name = self.ruta_to_input

        # Limpiar el layout existente antes de agregar nuevos elementos
        for i in reversed(range(self.layout_tablas.count())):
            widget = self.layout_tablas.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Crear una lista de IDs que queremos mostrar
        ids_a_mostrar = [1, 2, 3, 4, 5, 6, 7]

        # Crear un diccionario para almacenar los datos por ID
        datos_por_id = {id_: [] for id_ in ids_a_mostrar}

        if file_name:
            with open(file_name, 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Saltar la cabecera si la hay
                for line in csv_reader:
                    if len(line) >= 3:  # Asegurar que la línea tenga al menos 3 elementos (ID, Valor, Timestamp)
                        id_ = int(line[0])  # Suponiendo que el ID está en la primera columna y es un entero
                        valor = line[1]
                        timestamp = line[2]
                        if id_ in datos_por_id:
                            datos_por_id[id_].append((timestamp, valor))

            # Recorrer los IDs y crear una tabla para cada uno
            for id_ in ids_a_mostrar:
                titulo = QLabel(self.archivos_csv[id_ - 1])  # Usar el nombre del archivo correspondiente
                titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
                titulo.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")
                self.layout_tablas.addWidget(titulo)

                h_layout = QHBoxLayout()  # Crear un layout horizontal para la tabla y la gráfica

                tabla = QTableWidget()
                tabla.setColumnCount(2)
                tabla.setHorizontalHeaderLabels(['Timestamp', 'Valor'])

                data = datos_por_id[id_]

                tabla.setRowCount(len(data))

                for row, (timestamp, valor) in enumerate(data):
                    item_timestamp = QTableWidgetItem(timestamp)
                    item_valor = QTableWidgetItem(valor)

                    # Centrar el texto de las celdas
                    item_timestamp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item_valor.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    tabla.setItem(row, 0, item_timestamp)
                    tabla.setItem(row, 1, item_valor)

                # Ajustar el ancho de la columna 'Timestamp'
                tabla.setColumnWidth(0, 200)

                # Establecer el alto y ancho de la tabla
                altura_tabla = 450
                ancho_tabla = 342

                tabla.setFixedHeight(altura_tabla)
                tabla.setFixedWidth(ancho_tabla)

                # Agregar la tabla al layout horizontal
                h_layout.addWidget(tabla)

                # GRÁfICA
                # Crear la gráfica asociada
                x_data = [timestamp for timestamp, _ in data]
                y_data = [float(valor) for _, valor in data]

                fig = Figure(figsize=(4, 3))
                ax = fig.add_subplot(111)
                ax.plot(x_data, y_data, marker='o')

                ax.set_xlabel('Time')
                ax.set_ylabel('Value')

                canvas = FigureCanvas(fig)
                h_layout.addWidget(canvas)

                # Agregar el layout horizontal al layout principal vertical
                self.layout_tablas.addLayout(h_layout)

        else:
            # Crear etiqueta de título
            titulo = QLabel("No data to display")
            titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            titulo.setStyleSheet("font-size: 11pt; font-weight: bold; margin: 10px;")
            self.layout_tablas.addWidget(titulo)

        # Mostrar el QScrollArea después de cargar los datos
        self.scroll_area.show()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())