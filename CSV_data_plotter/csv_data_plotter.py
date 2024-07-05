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

        # IMG fondo
        fondo = QLabel(self)
        fondo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ruta_script = os.path.dirname(os.path.abspath(__file__))  
        ruta_imagen = os.path.join(ruta_script, 'assets/IMG_fondo.PNG') 
        pixmap = QPixmap(ruta_imagen)  
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio)
        fondo.setPixmap(pixmap)
        layout.addWidget(fondo)
        self.setLayout(layout)

        # TÍTULO
        titulo_label = QLabel('CSV Data Plotter Analyzer', self)
        titulo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        titulo_label.setFont(QFont('Arial', 20, QFont.Weight.Bold))  
        layout.addWidget(titulo_label, Qt.AlignmentFlag.AlignHCenter)

        # input de archivo CSV de datos
        input_label = QLabel('Upload CSV file with data', self)
        layout.addWidget(input_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.ruta_input = QLineEdit(self)
        self.ruta_input.setAlignment(Qt.AlignmentFlag.AlignLeft)  
        layout.addWidget(self.ruta_input)

        # Layout horizontal para los botones
        layout_botones = QHBoxLayout()

        # Botón para subir el archivo CSV
        btn_subir_csv = QPushButton('Subir CSV', self)
        btn_subir_csv.clicked.connect(self.abrir_dialogo_csv)
        btn_subir_csv.setStyleSheet("padding: 5px 20px;") 
        layout_botones.addWidget(btn_subir_csv)

        # Espacio entre los botones
        layout_botones.addSpacing(10)

        # Botón para cargar los datos del archivo
        btn_cargar_datos = QPushButton('Cargar Datos', self)
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

        # Agregar layout de botones al layout principal
        layout.addLayout(layout_botones)
        layout.addLayout(self.layout_tablas)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

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
        file_name =  self.ruta_to_input
        if file_name:
            self.ruta_input = file_name  # Almacenar la ruta del archivo seleccionado

            # Crear tabla y cargar datos desde CSV
            tabla = QTableWidget()
            tabla.setColumnCount(3)
            tabla.setHorizontalHeaderLabels(['ID', 'Valor', 'Timestamp'])

            with open(file_name, 'r', newline='') as csv_file:
                csv_reader = csv.reader(csv_file)
                next(csv_reader)  # Saltar la cabecera si la hay
                data = list(csv_reader)

            tabla.setRowCount(len(data))

            for row, (id_, valor, timestamp) in enumerate(data):
                tabla.setItem(row, 0, QTableWidgetItem(id_))
                tabla.setItem(row, 1, QTableWidgetItem(valor))
                tabla.setItem(row, 2, QTableWidgetItem(timestamp))

            self.layout_tablas.addWidget(tabla)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())