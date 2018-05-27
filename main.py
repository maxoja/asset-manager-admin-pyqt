from TWidget import LoginDialog, UserListView, EditPanel
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QSplitter, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from qtmodern import styles, windows
import sys
from TConnect import connector


class ManageUserWindow(QWidget):
    def __init__(self):
        super(ManageUserWindow, self).__init__()
        self.setWindowTitle("Asset Manager Admin")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        self.adminListView = UserListView()
        self.adminListView.setTitleText("Admin User List")
        self.adminListView.setIcon("img/admin-icon.png")
        self.adminListView.setOnSelectUser(self.__onClickAdmin)

        self.creatorListView = UserListView(keys=['id', 'name', 'email'])
        self.creatorListView.setTitleText("Creator User List")
        self.creatorListView.setIcon("img/artist-icon.png")
        self.creatorListView.setOnSelectUser(self.__onClickCreator)

        self.editPanel = EditPanel()
        self.editPanel.setFixedWidth(300)
        self.editPanel.addEditRow('Display Name', QLineEdit)
        self.editPanel.addEditRow('Email', QLineEdit)

        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.adminListView)
        self.splitter.addWidget(self.creatorListView)
        # self.splitter.addWidget(self.editPanel)

        layout = QHBoxLayout(self)
        layout.addWidget(self.splitter)
        layout.addWidget(self.editPanel)
        # layout.addWidget(self.adminListView)
        # layout.addWidget(self.creatorListView)

        self.__initialize()

    def __onClickCreator(self, creator):
        print("__onClickCreator called")
        self.editPanel.setEditValue('Display Name', creator['name'])
        self.editPanel.setEditValue('Email', creator['email'])
        self.editPanel.setAdditionalData(creator)

    def __onClickAdmin(self, admin):
        print("__onClickAdmin called")

    def __initialize(self):
        def onreceive(result):
            for k, v in result.items():
                v['id'] = k
                self.creatorListView.addUser(v)
                print(k, v)

        def onerror():
            print('get creator list error occurred')

        connector.getCreatorList(onreceive, onerror)


app = QApplication(sys.argv)
styles.dark(app)

dialog = LoginDialog()
mdialog = windows.ModernWindow(dialog)
mdialog.show()
loginResult = dialog.exec_()

if loginResult != QDialog.Accepted:
    sys.exit(app.exec_())

userwin = ManageUserWindow()
_userwin = windows.ModernWindow(userwin)
_userwin.show()

sys.exit(app.exec_())