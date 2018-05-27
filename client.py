from TWidget import LoginDialog, UserListView, EditPanel, HierarchyPanel
from TModel import HierarchicalModel
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QSplitter, QLineEdit, QTextEdit
from PyQt5.QtCore import Qt
from qtmodern import styles, windows
import sys
from TConnect import connector


class ManageAssetWindow(QWidget):
    def __init__(self):
        super(ManageAssetWindow, self).__init__()
        self.setWindowTitle("Asset Manager Client")
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)

        tree = HierarchicalModel()
        tree.add(0, name="root") \
            .add(1, 0, name="3D models", tip="you can set tooltip text\nby passing tip value of item") \
            .add(2, 1, name="Weapons") \
            .add(3, 2, name="Guns") \
            .add(4, 2, name="Melees") \
            .add(5, 2, name="Bombs") \
            .add(24, 1, name="Furnitures") \
            .add(25, 1, name="Instruments") \
            .add(26, 1, name="Zombies") \
            .add(6, 1, name="Vehicles") \
            .add(7, 6, name="Boats") \
            .add(8, 6, name="Bikes") \
            .add(9, 1, name="Trees") \
            .add(10, 0, name="Sprite Sheets") \
            .add(11, 10, name="Characters") \
            .add(12, 10, name="Buildings") \
            .add(13, 10, name="Map-Tiles") \
            .add(14, 10, name="Buttons") \
            .add(15, 10, name="Obstacles") \
            .add(16, 10, name="Magics") \
            .add(17, 10, name="Bullets&Rockets") \
            .add(18, 10, name="Lights") \
            .add(19, 10, name="Effects") \
            .add(20, 10, name="Titles") \
            .add(21, 10, name="9-Patches") \
            .add(22, 10, name="HUD") \
            .add(23, 10, name="Bars")

        self.hierarchy = HierarchyPanel(tree)

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
        layout.addWidget(self.hierarchy)
        layout.addWidget(self.splitter)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

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

dialog = LoginDialog()
dialog.show()
loginResult = dialog.exec_()

if loginResult != QDialog.Accepted:
    sys.exit(app.exec_())

userwin = ManageAssetWindow()
userwin.show()

sys.exit(app.exec_())