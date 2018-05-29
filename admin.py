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

        self.adminListView = UserListView(keys=['id', 'name', 'email', 'username', 'password'])
        self.adminListView.setTitleText("Admin User List")
        self.adminListView.setIcon("img/admin-icon.png")
        self.adminListView.setOnSelectUser(self.__onClickAdmin)

        self.creatorListView = UserListView(keys=['id', 'name', 'email', 'username', 'password'])
        self.creatorListView.setTitleText("Creator User List")
        self.creatorListView.setIcon("img/artist-icon.png")
        self.creatorListView.setOnSelectUser(self.__onClickCreator)

        self.editPanel = EditPanel()
        self.editPanel.setFixedWidth(300)
        self.editPanel.addEditRow('Display Name', QLineEdit)
        self.editPanel.addEditRow('Email', QLineEdit)
        self.editPanel.addEditRow('Username', QLineEdit)
        self.editPanel.addEditRow('Password', QLineEdit)

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
        self.editPanel.setEditValue('Username', creator['username'])
        self.editPanel.setEditValue('Password', creator['password'])
        creator['type'] = 'creator'
        self.editPanel.setAdditionalData(creator)

    def __onClickAdmin(self, admin):
        print("__onClickAdmin called")
        self.editPanel.setEditValue('Display Name', admin['name'])
        self.editPanel.setEditValue('Email', admin['email'])
        self.editPanel.setEditValue('Username', admin['username'])
        self.editPanel.setEditValue('Password', admin['password'])
        admin['type'] = 'admin'
        self.editPanel.setAdditionalData(admin)

    def __fetchAdminList(self):
        def onreceive(result):
            # self.creatorListView.hideLoading()
            self.adminListView.clearAll()
            for k, v in result.items():
                v['id'] = k
                self.adminListView.addUser(v)
                print(k, v)

        def onerror():
            # self.creatorListView.hideLoading()
            print('get creator list error occurred')

        connector.getAdminList(onreceive, onerror)

    def __fetchCreatorList(self):
        def onreceive(result):
            # self.creatorListView.hideLoading()
            self.creatorListView.clearAll()

            for k, v in result.items():
                v['id'] = k
                self.creatorListView.addUser(v)
                print(k, v)

        def onerror():
            # self.creatorListView.hideLoading()
            print('get creator list error occurred')

        # self.creatorListView.showLoading()
        connector.getCreatorList(onreceive, onerror)

    def __initialize(self):
        self.__fetchAdminList()
        self.__fetchCreatorList()

        def onclickupdate(editdict, data):
            if 'id' not in data:
                return

            data['username'] = editdict['Username']
            data['name'] = editdict['Display Name']
            data['email'] = editdict['Email']
            data['password'] = editdict['Password']

            def onupdatesuccess():
                type = data['type']
                self.editPanel.setEditValue('Display Name', '')
                self.editPanel.setEditValue('Email', '')
                self.editPanel.setEditValue('Password', '')
                self.editPanel.setEditValue('Username', '')
                self.editPanel.setAdditionalData({})

                if type == 'creator':
                    self.__fetchCreatorList()
                if type == 'admin':
                    self.__fetchAdminList()

            connector.editUser(data['id'],data['name'],data['username'],data['password'],data['email'], onupdatesuccess, lambda: print("error update"))

        def onclicknewadmin(editdict, data):
            def onsuccess():
                self.editPanel.setEditValue('Display Name', '')
                self.editPanel.setEditValue('Email', '')
                self.editPanel.setEditValue('Password', '')
                self.editPanel.setEditValue('Username', '')
                self.editPanel.setAdditionalData({})

                self.__fetchAdminList()

            connector.createAdmin(editdict['Display Name'],editdict['Username'], editdict['Password'], editdict['Email'], onsuccess, lambda x,y: None, lambda : None )

        def onclicknewcreator(editdict, data):
            def onsuccess():
                self.editPanel.setEditValue('Display Name', '')
                self.editPanel.setEditValue('Email', '')
                self.editPanel.setEditValue('Password', '')
                self.editPanel.setEditValue('Username', '')
                self.editPanel.setAdditionalData({})

                self.__fetchCreatorList()

            connector.createCreator(editdict['Display Name'], editdict['Username'], editdict['Password'], editdict['Email'], onsuccess, lambda x, y: None, lambda: None)

        def onclickdelete(editdict, data):
            if self.editPanel.getEditValue('Display Name') == '':
                return
            if self.editPanel.getEditValue('Username') == '':
                return
            if self.editPanel.getEditValue('Password') == '':
                return
            if self.editPanel.getEditValue('Email') == '':
                return
            if self.editPanel.getAdditionalData() == None:
                return
            if 'id' not in self.editPanel.getAdditionalData():
                return

            def onsuccess():
                type = self.editPanel.getAdditionalData()['type']
                self.editPanel.setEditValue('Display Name', '')
                self.editPanel.setEditValue('Email', '')
                self.editPanel.setEditValue('Password', '')
                self.editPanel.setEditValue('Username', '')
                self.editPanel.setAdditionalData({})

                if type == 'creator':
                    self.__fetchCreatorList()
                else:
                    self.__fetchAdminList()

            connector.deleteUser(self.editPanel.getAdditionalData()['id'], onsuccess, lambda : print('error'))

        self.editPanel.setOnClickUpdate(onclickupdate)
        self.editPanel.setOnClickNewAdmin(onclicknewadmin)
        self.editPanel.setOnClickNewCreator(onclicknewcreator)
        self.editPanel.setOnClickDelete(onclickdelete)


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