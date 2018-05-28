from TWidget import LoginDialog, UserListView, EditPanel, HierarchyPanel, StepperWidget, CommentPanel, AssetViewWidget, AssetOptionPanel
from TModel import HierarchicalModel
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QSplitter, QLineEdit, QTextEdit, QVBoxLayout
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from qtmodern import styles, windows
import sys
from TConnect import connector


class ManageAssetWindow(QWidget):
    def __init__(self):
        super(ManageAssetWindow, self).__init__()
        self.setWindowTitle("Asset Manager Client")
        self.setMinimumWidth(1000)
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

        # LEFT WIDGET
        self.hierarchy = HierarchyPanel(tree)

        # RIGHT WIDGET
        self.commentPanel = CommentPanel()
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.addComment(title="comment 1", owner="maxoja", time="8:52 PM 27/05/18")
        self.commentPanel.setMaximumWidth(260)

        # MID TOP WIDGET
        self.stepper = StepperWidget(5, checkpointCover=0.7)
        [self.stepper.setSecondaryText('', i) for i in range(5)]

        # MID MID WIDGET
        self.assetView = AssetViewWidget()
        self.assetView.setPhoto(QPixmap('img/admin-icon.png'))
        # self.assetView = UserListView(keys=['id', 'name', 'email'])
        # self.assetView.setTitleText("Creator User List")
        # self.assetView.setIcon("img/artist-icon.png")
        # self.assetView.setOnSelectUser(self.__onClickCreator)

        # MID BOTTOM WIDGET
        self.assetOptionPanel = AssetOptionPanel()
        # self.assetOptionPanel = UserListView(keys=['id', 'name', 'email'])
        # self.assetOptionPanel.setTitleText("Creator User List")
        # self.assetOptionPanel.setIcon("img/artist-icon.png")
        # self.assetOptionPanel.setOnSelectUser(self.__onClickCreator)

        # MID LOWER LAYOUT
        midwidget = QWidget()
        midlayout = QVBoxLayout()
        midlayout.addWidget(self.assetView)
        midlayout.addWidget(self.assetOptionPanel)
        midlayout.setContentsMargins(0, 0, 0, 0)
        midwidget.setLayout(midlayout)

        # MID SPLITTER
        self.splitter = QSplitter(Qt.Vertical)
        self.splitter.addWidget(self.stepper)
        self.splitter.addWidget(midwidget)

        # OUTER LAYOUT
        layout = QHBoxLayout(self)
        layout.addWidget(self.hierarchy)
        layout.addWidget(self.splitter)
        layout.addWidget(self.commentPanel)
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
        pass


app = QApplication(sys.argv)

dialog = LoginDialog()
dialog.show()
loginResult = dialog.exec_()

if loginResult != QDialog.Accepted:
    sys.exit(app.exec_())

userwin = ManageAssetWindow()
userwin.show()

sys.exit(app.exec_())