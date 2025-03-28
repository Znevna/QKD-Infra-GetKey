# This work has been implemented by Alin-Bogdan Popa and Bogdan-Calin Ciobanu,
# under the supervision of prof. Pantelimon George Popescu, within the Quantum
# Team in the Computer Science and Engineering department,Faculty of Automatic 
# Control and Computers, National University of Science and Technology 
# POLITEHNICA Bucharest (C) 2024. In any type of usage of this code or released
# software, this notice shall be preserved without any changes.


import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QFileDialog,
    QComboBox, QVBoxLayout, QHBoxLayout, QTextEdit
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame

from copy import deepcopy
import qkdgkt

from dotenv import load_dotenv
import os

load_dotenv()

LOCATION_NAMES = qkdgkt.qkd_get_location_names()
LOCATIONS = qkdgkt.qkd_get_locations()

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Layouts
        main_layout = QVBoxLayout()
        form_layout = QVBoxLayout()
        button_layout = QHBoxLayout()
        about_layout = QVBoxLayout()

        # File browse fields
        self.cert_label = QLabel('Cert:')
        self.cert_field = QLineEdit()
        self.cert_button = QPushButton('Browse')
        self.cert_button.clicked.connect(lambda: self.browse_file(self.cert_field))

        self.key_label = QLabel('Key:')
        self.key_field = QLineEdit()
        self.key_button = QPushButton('Browse')
        self.key_button.clicked.connect(lambda: self.browse_file(self.key_field))

        self.cacert_label = QLabel('CACert:')
        self.cacert_field = QLineEdit()
        self.cacert_button = QPushButton('Browse')
        self.cacert_button.clicked.connect(lambda: self.browse_file(self.cacert_field))

        # Toggle for "Request/Response"
        self.request_response_label = QLabel('Request/Response:')
        self.request_response_dropdown = QComboBox()
        self.request_response_dropdown.addItems(['Request', 'Response'])
        self.request_response_dropdown.currentIndexChanged.connect(self.toggle_id_field)
        form_layout.addWidget(self.request_response_label)
        form_layout.addWidget(self.request_response_dropdown)

        # ID field
        self.id_label = QLabel('ID:')
        self.id_field = QLineEdit()
        form_layout.addWidget(self.id_label)
        form_layout.addWidget(self.id_field)
        self.id_label.hide()
        self.id_field.hide()

        # Password field
        self.password_label = QLabel('Password:')
        self.password_field = QLineEdit()
        self.password_field.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_field)

        # Dropdowns
        self.source_label = QLabel('Source:')
        self.source_dropdown = QComboBox()
        self.source_dropdown.addItem(os.getenv("LOCATION", "ADD_LOCATION"))
        self.source_dropdown.currentIndexChanged.connect(self.update_destination)

        self.destination_label = QLabel('Destination:')
        self.destination_dropdown = QComboBox()

        # Submit Button
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit_action)

        # Clear Button
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear_action)

        # Add widgets to form layout
        form_layout.addWidget(self.cert_label)
        form_layout.addWidget(self.cert_field)
        form_layout.addWidget(self.cert_button)

        form_layout.addWidget(self.key_label)
        form_layout.addWidget(self.key_field)
        form_layout.addWidget(self.key_button)

        form_layout.addWidget(self.cacert_label)
        form_layout.addWidget(self.cacert_field)
        form_layout.addWidget(self.cacert_button)

        form_layout.addWidget(self.source_label)
        form_layout.addWidget(self.source_dropdown)

        form_layout.addWidget(self.destination_label)
        form_layout.addWidget(self.destination_dropdown)

        # Add submit button to button layout
        button_layout.addStretch(1)
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.submit_button)

        # About layout - add about text and logo
        about_label = QLabel('QKD Get Key Tool')
        # make about_label bold
        font = about_label.font()
        font.setBold(True)
        about_label.setFont(font)
        about_layout.addWidget(about_label)
        about_logo_layout = QHBoxLayout()
        about_label_by = QLabel('© 2024 National University of Science and Technology POLITEHNICA Bucharest')
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        about_layout.addWidget(self.line)

        about_label_logo = QLabel()
        pixmap = QPixmap('Logo.png').scaled(60,60, Qt.KeepAspectRatio)
        about_label_logo.setPixmap(pixmap)
        about_logo_layout.addWidget(about_label_logo)
        about_logo_layout.addWidget(about_label_by)
        about_layout.addLayout(about_logo_layout)
        
        self.line2 = QFrame()
        self.line2.setFrameShape(QFrame.HLine)
        self.line2.setFrameShadow(QFrame.Sunken)
        about_layout.addWidget(self.line2)
        
        # add clickable link to the Quantum Team website
        about_label_website = QLabel('<a href="https://quantum.upb.ro/">Visit Website</a>')
        about_label_website.setOpenExternalLinks(True)
        about_layout.addWidget(about_label_website)
        about_label_github = QLabel('<a href="https://github.com/QuantumUPB/QKD-Infra-GetKey">GitHub Repository</a>')
        about_label_github.setOpenExternalLinks(True)
        about_layout.addWidget(about_label_github)
        
        # Add form and button layout to main layout
        main_layout.addLayout(form_layout)
        main_layout.addLayout(button_layout)

        self.result_textbox = QTextEdit()
        self.result_textbox.setReadOnly(True)
        main_layout.addWidget(self.result_textbox)

        main_layout.addLayout(about_layout)

        # Set main layout
        self.setLayout(main_layout)

        # Set window properties
        self.setWindowTitle('QKD Get Key Tool')
        self.setGeometry(300, 300, 400, 200)

        # Initialize the destination dropdown
        self.update_destination()

    def clear_action(self):
        self.result_textbox.clear()

    def toggle_id_field(self):
        if self.request_response_dropdown.currentText() == 'Request':
            self.id_label.hide()
            self.id_field.hide()
        else:
            self.id_label.show()
            self.id_field.show()

    def browse_file(self, field):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File", "", "All Files (*);;Text Files (*.txt)", options=options)
        if file_name:
            field.setText(file_name)

    def update_destination(self):
        source = self.source_dropdown.currentText()
        options = deepcopy(LOCATION_NAMES)
        options.remove(source)

        self.destination_dropdown.clear()
        self.destination_dropdown.addItems(options)

    def get_destination_endpoint(self):
        destination = self.destination_dropdown.currentText()
        return next((loc['endpoint'] for loc in LOCATIONS if loc['name'] == destination), None)
        
    def get_source_endpoint(self):
        source = self.source_dropdown.currentText()
        source_base_url = next((loc['ipport'] for loc in LOCATIONS if loc['name'] == source), None)
        if os.environ.get("ADD_KME", "") != "":
            source_base_url += "/" + source + "/" + os.getenv("CONSUMER", "ADD_CONSUMER")
        return source_base_url

    def submit_action(self):
        cert_path = self.cert_field.text()
        key_path = self.key_field.text()
        cacert_path = self.cacert_field.text()
        source = self.get_source_endpoint()
        destination = self.get_destination_endpoint()
        pem_password = self.password_field.text()
        req_type = self.request_response_dropdown.currentText()
        id = self.id_field.text()
        
        if req_type == 'Request':
            result = qkdgkt.qkd_get_key_custom_params(destination, source, cert_path, key_path, cacert_path, pem_password, 'Request')
        else:
            result = qkdgkt.qkd_get_key_custom_params(destination, source, cert_path, key_path, cacert_path, pem_password, 'Response', id)

        self.result_textbox.setPlainText(result)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())
