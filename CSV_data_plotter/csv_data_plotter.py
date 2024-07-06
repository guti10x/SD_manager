######################################################################################################################################
#                                                                                                                                    #
#                           CSV DATA PLOTTER ANALYZER V1                                                                             # 
#                                    05/07/2024                                                                                      #
#                            By Daniel Gutiérrez Torres                                                                              #
#                                                                                                                                    #    
######################################################################################################################################

import csv
import sys
import os
from turtle import pd
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QSizePolicy
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QTableWidget, QTableWidgetItem, QWidget, QPushButton, QFileDialog, QSpacerItem


class Ventana(QWidget):

    def __init__(self):
        super().__init__()

        # Lista de nombres de archivos CSV sin la extensión
        self.archivos_csv = [
            "Accel_pedal",
            "Battery_volt",
            "Brake_pedal",
            "Engine_temp",
            "Gear",
            "RPM",
            "Speed"
        ]

        self.graficas = {} 

        self.initUI()

    def initUI(self):

        # Configuración de la ventana
        self.setGeometry(50, 50, 1100, 400) 
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

        # Crear un layout horizontal para la fila con el QLabel, QLineEdit y QPushButton
        layout_fila = QHBoxLayout()

        # Crear y añadir el QLabel
        input_label = QLabel('Upload CSV:', self)
        layout_fila.addWidget(input_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Crear y añadir el QLineEdit
        self.ruta_input = QLineEdit(self)
        self.ruta_input.setAlignment(Qt.AlignmentFlag.AlignLeft)
        layout_fila.addWidget(self.ruta_input)

        # Crear y añadir el QPushButton
        btn_subir_csv = QPushButton('Subir CSV', self)
        btn_subir_csv.clicked.connect(self.abrir_dialogo_csv)
        btn_subir_csv.setStyleSheet("padding: 5px 20px;")
        layout_fila.addWidget(btn_subir_csv)

        # Añadir el layout horizontal al layout principal
        layout.addLayout(layout_fila)

        # Layout horizontal para los botones
        layout_botones = QHBoxLayout()

       

        # Espacio entre los botones
        # layout_botones.addSpacing(70)

        # Botón para cargar los datos del archivo
        btn_cargar_datos = QPushButton('visualize data', self)
        btn_cargar_datos.clicked.connect(self.cargar_datos)
        btn_cargar_datos.setStyleSheet("padding: 5px 20px;") 
        layout_botones.addWidget(btn_cargar_datos)

        # Botón para cargar los datos del archivo
        btn_cargar_datos = QPushButton('Upload to Google Drive', self)
        btn_cargar_datos.clicked.connect(self.cargar_datos)
        btn_cargar_datos.setStyleSheet("padding: 5px 20px;") 
        layout_botones.addWidget(btn_cargar_datos)

        # Añadir espacio flexible después de los botones para empujarlos a la izquierda
        layout_botones.addStretch(1)

        # Añadir el layout horizontal de los botones al layout principal
        layout.addLayout(layout_botones)

        # Crear layout horizontal
        layout_horizontal = QHBoxLayout()

        # Iterar sobre los archivos csv y agregar checkboxes directamente
        for nombre_csv in self.archivos_csv:
            checkbox = QCheckBox(nombre_csv, self)
            checkbox.setChecked(True) 
            layout_horizontal.addWidget(checkbox)
        
        layout.addLayout(layout_horizontal)
        self.show()

        # Layout vertical para las tablas
        self.layout_tablas = QVBoxLayout()

        layout.addLayout(self.layout_tablas)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        # IMG fondo
        fondo = QLabel(self)
        fondo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_script = os.path.dirname(os.path.abspath(__file__))  
        ruta_imagen = os.path.join(ruta_script, 'assets/IMG_fondo.PNG') 
        pixmap = QPixmap(ruta_imagen)  
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
        fondo.setPixmap(pixmap)
        layout.addWidget(fondo)

    ruta_to_input = ""

    def abrir_dialogo_csv(self):
        # Abrir un diálogo para seleccionar archivo CSV
        archivo_csv, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "Archivos CSV (*.csv)")
        
        if archivo_csv:
            self.ruta_to_input = archivo_csv
            self.ruta_input.setText(archivo_csv)
            print(f"Ruta del archivo seleccionado: {self.ruta_input}")

    def crear_grafica(self, nombre):
        return
    
    def cargar_datos(self):
        file_name = self.ruta_to_input

        # Crear etiqueta de título
        titulo = QLabel("Engine Temperture")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 16pt; font-weight: bold; margin: 10px;")

        if file_name:
            self.ruta_input = file_name  # Almacenar la ruta del archivo seleccionado

            # Crear tabla y cargar datos desde CSV
            tabla = QTableWidget()
            tabla.setColumnCount(2)
            tabla.setHorizontalHeaderLabels(['Timestamp', 'Valor'])

            with open(file_name, 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Saltar la cabecera si la hay
                data = list(csv_reader)

            tabla.setRowCount(len(data))

            for row, line in enumerate(data):
                if len(line) >= 3:
                    valor = line[1]
                    timestamp = line[2]
                    item_timestamp = QTableWidgetItem(timestamp)
                    item_valor = QTableWidgetItem(valor)

                    # Centrar el texto de las celdas
                    item_timestamp.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                    item_valor.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

                    tabla.setItem(row, 0, item_timestamp)
                    tabla.setItem(row, 1, item_valor)

            # Ajustar el ancho de la columna 'Timestamp'
            tabla.setColumnWidth(0, 200)  # Ajusta este valor según sea necesario

            # Establecer el alto y ancho de la tabla
            altura_tabla = 300  # Ajusta esta altura según tus necesidades
            ancho_tabla = 350

            tabla.setFixedHeight(altura_tabla)
            tabla.setFixedWidth(ancho_tabla)

        else:
            # Crear etiqueta de título
            titulo = QLabel("No data to display")
            titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            titulo.setStyleSheet("font-size: 11pt; font-weight: bold; margin: 10px;")
        self.layout_tablas.addWidget(titulo)
        self.layout_tablas.addWidget(tabla)
       


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())