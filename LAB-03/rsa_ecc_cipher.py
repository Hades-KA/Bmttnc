import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from ui.rsa_ecc import Ui_MainWindow
import requests

class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect RSA buttons
        self.ui.pushButton_3.clicked.connect(self.call_api_rsa_gen_keys)
        self.ui.pushButton_7.clicked.connect(self.call_api_rsa_sign)
        self.ui.pushButton_6.clicked.connect(self.call_api_rsa_verify)

        # Connect ECC buttons
        self.ui.pushButton_3.clicked.connect(self.call_api_ecc_gen_keys)
        self.ui.pushButton_5.clicked.connect(self.call_api_ecc_sign)
        self.ui.pushButton_4.clicked.connect(self.call_api_ecc_verify)

    # RSA API calls
    def call_api_rsa_gen_keys(self):
        url = "http://127.0.0.1:5000/api/rsa/generate_keys"
        self.handle_api_request(url, "RSA keys generated successfully!")

    def call_api_rsa_sign(self):
        url = "http://127.0.0.1:5000/api/rsa/sign"
        payload = {"message": self.ui.textEdit_6.toPlainText()}
        self.handle_api_request(url, "Signed Successfully", self.ui.textEdit_5, "signature", payload)

    def call_api_rsa_verify(self):
        url = "http://127.0.0.1:5000/api/rsa/verify"
        payload = {
            "message": self.ui.textEdit_6.toPlainText(),
            "signature": self.ui.textEdit_5.toPlainText()
        }
        self.handle_verification_request(url, payload)

    # ECC API calls
    def call_api_ecc_gen_keys(self):
        url = "http://127.0.0.1:5000/api/ecc/generate_keys"
        self.handle_api_request(url, "ECC keys generated successfully!")

    def call_api_ecc_sign(self):
        url = "http://127.0.0.1:5000/api/ecc/sign"
        payload = {"message": self.ui.textEdit_4.toPlainText()}
        self.handle_api_request(url, "Signed Successfully", self.ui.textEdit_3, "signature", payload)

    def call_api_ecc_verify(self):
        url = "http://127.0.0.1:5000/api/ecc/verify"
        payload = {
            "message": self.ui.textEdit_4.toPlainText(),
            "signature": self.ui.textEdit_3.toPlainText()
        }
        self.handle_verification_request(url, payload)

    # Helper methods
    def handle_api_request(self, url, success_message, output_widget=None, output_key=None, payload=None):
        try:
            response = requests.post(url, json=payload) if payload else requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if output_widget and output_key:
                    output_widget.setText(data[output_key])
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText(success_message)
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    def handle_verification_request(self, url, payload):
        try:
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                data = response.json()
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Verified Successfully" if data["is_verified"] else "Verification Failed")
                msg.exec_()
            else:
                print("Error while calling API")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
