from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QWidget, QFormLayout

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Admin Login")
        self.setMinimumWidth(300)

        self.verification = lambda user, password: user == '' and password == ''

        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)

        self.buttonLogin = QPushButton('Authenticate')
        self.buttonLogin.clicked.connect(self.handleLogin)

        layout = QVBoxLayout(self)
        form = QFormLayout()
        form.addRow('Username', self.textName)
        form.addRow('Password', self.textPass)
        form.addWidget(self.buttonLogin)
        layout.addLayout(form)
        layout.addWidget(self.buttonLogin)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

    def setVerification(self, verification):
        self.verification = verification

    def handleLogin(self):
        if self.verification(self.textName.text(), self.textPass.text()):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Invalid username or password')


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    def verification(u, p):
        return u == 'tawan' and p == 'tham'

    dialog = LoginDialog()
    dialog.setVerification(verification)
    dialog.show()
    loginResult = dialog.exec_()

    if loginResult != QDialog.Accepted:
        sys.exit(app.exec_())

    q = QWidget()
    q.show()
    sys.exit(app.exec_())
