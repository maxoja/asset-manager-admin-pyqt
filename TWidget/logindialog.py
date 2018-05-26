from PyQt5.QtWidgets import QDialog, QApplication, QLineEdit, QPushButton, QLabel, QDesktopWidget
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QWidget, QFormLayout, QLayout
from PyQt5.QtCore import Qt, QPoint
from qtmodern import styles, windows

class LoginDialog(QDialog):
    def __init__(self, parent=None):
        QDialog.__init__(self, parent)
        self.setWindowTitle("Asset Manager Admin Login")
        self.setFixedWidth(300)
        self.setMaximumHeight(150)
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.move(centerPoint.x()-self.width()/2, centerPoint.y()-self.height()/2)

        self.verification = lambda user, password: user == '' and password == ''

        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.textPass.setEchoMode(QLineEdit.Password)

        self.buttonLogin = QPushButton('Authenticate')
        self.buttonLogin.clicked.connect(self.__handleLogin)

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

    def __handleLogin(self):
        if self.verification(self.textName.text(), self.textPass.text()):
            self.accept()
            self.close()
        else:
            warningDialog = InvalidDialog()
            mwarning = windows.ModernWindow(warningDialog)
            mwarning.show()
            warningDialog.exec_()

class InvalidDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.setWindowTitle("Auth Error")
        self.setFixedSize(180, 70)
        centerPoint = QDesktopWidget().availableGeometry().center()
        self.move(centerPoint.x()+250-self.width()/2, centerPoint.y()-self.height()/2)

        self.warningLabel = QLabel('Invalid username or password')
        self.okButton = QPushButton('Ok')
        self.okButton.clicked.connect(self.onClick)

        layout = QVBoxLayout(self)
        layout.addWidget(self.warningLabel)
        layout.addWidget(self.okButton)
        layout.setAlignment(Qt.AlignCenter)

    def onClick(self):
        self.accept()
        self.close()


if __name__ == '__main__':
    import sys
    from qtmodern import styles, windows

    app = QApplication(sys.argv)
    styles.dark(app)

    def verification(u, p):
        return u == 'tawan' and p == 'tham'

    dialog = LoginDialog()
    dialog.setVerification(verification)
    mdialog = windows.ModernWindow(dialog)
    mdialog.show()
    loginResult = dialog.exec_()

    if loginResult != QDialog.Accepted:
        sys.exit(app.exec_())

    q = QWidget()
    q.show()
    sys.exit(app.exec_())
