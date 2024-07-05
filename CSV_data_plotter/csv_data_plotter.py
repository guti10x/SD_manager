


import sys
import os
from PyQt6.QtWidgets import QApplication, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QCheckBox
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt

class MiVentana(QWidget):

    # data 
    archivos_csv = [
        "Accel_pedal",
        "Battery_volt",
        "Brake_pedal",
        "Engine_temp",
        "Gear",
        "RPM",
        "Speed"
    ]

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Configuración de la ventana
        self.setGeometry(50, 50, 1100, 400) 
        self.setWindowTitle('Interfaz con Imagen de Fondo')

        # PLANTILLA
        layout = QVBoxLayout()

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

        # input de archivo cssv de datos
        input_label = QLabel('Upload CSV file with data', self)
        layout.addWidget(input_label, alignment=Qt.AlignmentFlag.AlignLeft)

        self.ruta_input = QLineEdit(self)
        self.ruta_input.setAlignment(Qt.AlignmentFlag.AlignCenter)  
        layout.addWidget(self.ruta_input)

        # Botón para subir el archivo CSV
        btn_subir_csv = QPushButton('Subir CSV', self)
        btn_subir_csv.clicked.connect(self.abrir_dialogo_csv)
        layout.addWidget(btn_subir_csv)

        # Lista de nombres de archivos CSV sin la extensión
        archivos_csv = [
            "Accel_pedal",
            "Battery_volt",
            "Brake_pedal",
            "Engine_temp",
            "Gear",
            "RPM",
            "Speed"
        ]
        
        # Crear y agregar checkboxes al layout vertical
        for nombre_csv in archivos_csv:
            checkbox = QCheckBox(nombre_csv, self)
            checkbox.setChecked(True)  # Opcional: establecer inicialmente seleccionados
            layout.addWidget(checkbox)

        self.setLayout(layout)
       

        

    def abrir_dialogo_csv(self):
        # Abrir un diálogo para seleccionar archivo CSV
        archivo_csv, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo CSV", "", "Archivos CSV (*.csv)")
        if archivo_csv:
            self.ruta_input.setText(archivo_csv) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MiVentana()
    ventana.show()
    sys.exit(app.exec())