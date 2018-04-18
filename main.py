from TWidget import LoginDialog, UserListView, EditPanel
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QSplitter, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from qtmodern import styles, windows
import sys


class ManageUserWindow(QWidget):
    def __init__(self):
        super(ManageUserWindow, self).__init__()
        self.setWindowTitle("Asset Manager Admin")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.adminListView = UserListView()
        self.adminListView.setTitleText("Admin User List")
        self.adminListView.setIcon("img/admin-icon.png")

        self.creatorListView = UserListView()
        self.creatorListView.setTitleText("Creator User List")
        self.creatorListView.setIcon("img/artist-icon.png")

        self.editPanel = EditPanel()
        self.editPanel.setFixedWidth(270)
        self.editPanel.addEditRow('Employment ID', QLineEdit)
        self.editPanel.addEditRow('Display Name', QLineEdit)
        self.editPanel.addEditRow('Username', QLineEdit)
        self.editPanel.addEditRow('Password', QLineEdit)
        self.editPanel.addEditRow('Email', QLineEdit)
        self.editPanel.addEditRow('Notes', QTextEdit)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.adminListView)
        self.splitter.addWidget(self.creatorListView)
        # self.splitter.addWidget(self.editPanel)

        layout = QHBoxLayout(self)
        layout.addWidget(self.splitter)
        layout.addWidget(self.editPanel)
        # layout.addWidget(self.adminListView)
        # layout.addWidget(self.creatorListView)


def verification(u, p):
    return u == 'admin' and p == 'password'


app = QApplication(sys.argv)
styles.dark(app)

dialog = LoginDialog()
dialog.setVerification(verification)
mdialog = windows.ModernWindow(dialog)
mdialog.show()
loginResult = dialog.exec_()

if loginResult != QDialog.Accepted:
    sys.exit(app.exec_())

userwin = ManageUserWindow()
_userwin = windows.ModernWindow(userwin)
_userwin.show()
sys.exit(app.exec_())