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
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox, QVBoxLayout, QWidget, QSizePolicy, QTableWidget, QTableWidgetItem, QSpacerItem, QScrollArea
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt


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
        btn_cargar_datos= QPushButton('visualize data', self)
        btn_cargar_datos.clicked.connect(self.cargar_datos)
        btn_cargar_datos.setStyleSheet("padding: 5px 20px;") 
        layout_botones.addWidget(btn_cargar_datos)

        # Botón para cargar los datos del archivo
        btn_drive_upload = QPushButton('Upload to Google Drive', self)
        btn_drive_upload.clicked.connect(self.cargar_datos)
        btn_drive_upload.setStyleSheet("padding: 5px 20px;") 
        layout_botones.addWidget(btn_drive_upload)

        # Añadir espacio flexible después de los botones para empujarlos a la izquierda
        layout_botones.addStretch(1)

        # Añadir el layout horizontal de los botones al layout principal
        layout.addLayout(layout_botones)

        # Crear layout horizontal
        #layout_horizontal = QHBoxLayout()
        # Iterar sobre los archivos csv y agregar checkboxes directamente
        #for nombre_csv in self.archivos_csv:
            #checkbox = QCheckBox(nombre_csv, self)
            #checkbox.setChecked(True) 
            #layout_horizontal.addWidget(checkbox)
        #layout.addLayout(layout_horizontal)

       

        # Widget scrollable para las tablas
        self.scroll_content = QWidget()
        self.layout_tablas = QVBoxLayout(self.scroll_content)
        
        # Crear un área de scroll y configurar el contenido
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_area.setFixedHeight(600)
        self.scroll_area.hide()

        # Agregar el área de scroll al layout principal
        layout.addWidget(self.scroll_area)

        spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        layout.addItem(spacer)

        # Botón para cerrar scroll de datos
        self.btn_close_data = QPushButton('Close', self)
        self.btn_close_data.clicked.connect(self.close_data)
        self.btn_close_data.setFixedSize(100, 30)  
        self.btn_close_data.setStyleSheet("padding: 5px 20px;") 
        self.btn_close_data.hide()
        layout.addWidget(self.btn_close_data, alignment=Qt.AlignmentFlag.AlignRight)

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
            print(f"Ruta del archivo seleccionado: {self.ruta_input}")

    def crear_grafica(self, nombre):
        return
    
    def close_data(self, nombre):
        self.scroll_area.hide()
        self.btn_close_data.hide()
    
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
                altura_tabla = 300
                ancho_tabla = 350

                tabla.setFixedHeight(altura_tabla)
                tabla.setFixedWidth(ancho_tabla)

                # Agregar la tabla al layout
                self.layout_tablas.addWidget(tabla)

        else:
            # Crear etiqueta de título
            titulo = QLabel("No hay datos para mostrar")
            titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
            titulo.setStyleSheet("font-size: 11pt; font-weight: bold; margin: 10px;")
            self.layout_tablas.addWidget(titulo)

        # Mostrar el QScrollArea después de cargar los datos
        self.scroll_area.show()
        self.btn_close_data.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = Ventana()
    ventana.show()
    sys.exit(app.exec())