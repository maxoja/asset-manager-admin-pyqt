from TWidget import LoginDialog, UserListView
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QSplitter
from PyQt5.QtCore import Qt
from qtmodern import styles, windows
import sys


class ManageUserWindow(QWidget):
    def __init__(self):
        super(ManageUserWindow, self).__init__()
        self.setWindowTitle("Asset Manager Admin")

        self.adminListView = UserListView()
        self.adminListView.setTitleText("Admin User List")
        self.adminListView.setIcon("img/admin-icon.png")

        self.creatorListView = UserListView()
        self.creatorListView.setTitleText("Creator User List")
        self.creatorListView.setIcon("img/artist-icon.png")

        self.splitter = QSplitter(Qt.Horizontal)
        self.splitter.addWidget(self.adminListView)
        self.splitter.addWidget(self.creatorListView)

        layout = QHBoxLayout(self)
        layout.addWidget(self.splitter)
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