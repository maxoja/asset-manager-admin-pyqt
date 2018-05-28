from TWidget import LoginDialog, UserListView, EditPanel, HierarchyPanel, StepperWidget, CommentPanel, AssetViewWidget, AssetOptionPanel
from TModel import HierarchicalModel
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QSplitter, QLineEdit, QTextEdit, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
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
            .add(6, 1, name="Furnitures") \
            .add(7, 1, name="Instruments") \
            .add(8, 1, name="Zombies")

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
        self.prevAsset = None
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

    def __fetchHierarchy(self):
        def ongetfiles(files):
            print(files)

            tree = self.hierarchy.model
            if isinstance(tree, HierarchicalModel):

                for i in tree.getIds():
                    tree.removeById(i)

            tree.add(0, name="root")

            for file in files:
                allpath = file['path']
                splittedpath = allpath.split('-')
                selfid = int(splittedpath[0])
                parentid = int(splittedpath[1])
                filename = splittedpath[2]
                isfile = '.' in filename

                tree.add(selfid, parentid, name=filename, isfile=isfile, fileid=file['id'])
                print(file)

            self.hierarchy.reconstruct(0)

        def onclickitem(item):
            if item['isfile']:
                self.stepper.setVisible(True)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_VIEW_ASSET)
            else:
                self.stepper.setVisible(False)
                self.assetView.setPhoto(None)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_FOLDER)

        self.hierarchy.setOnClickItem(onclickitem)
        connector.getFileList(ongetfiles, lambda: print("error"))

    def __setupOptionPanel(self):
        # DELETE FOLDER
        def onsuccessdeletefolder():
            self.__fetchHierarchy()

        def onDeleteFolder():
            model = self.hierarchy.model
            clickeditem = self.hierarchy.getHighlightedItem()
            itemdict = model.getItemOf(clickeditem.getId())
            if itemdict['isfile']:
                print('delete folder : current is not a folder')
            else:
                if model.hasChildren(clickeditem.getId()):
                    print('delete folder : the folder is not empty')
                else:
                    connector.deleteFile(itemdict['fileid'], onsuccessdeletefolder, lambda: None)

        # DELETE ASSET
        def onsuccessdeleteasset():
            self.__fetchHierarchy()

        def onDeleteAsset():
            model = self.hierarchy.model
            clickeditem = self.hierarchy.getHighlightedItem()
            itemid = clickeditem.getId()
            itemdict = model.getItemOf(itemid)
            if itemdict['isfile']:
                print(itemdict)
                connector.deleteFile(itemdict['fileid'], onsuccessdeleteasset, lambda: None)
            else:
                print('delete asset : the current is not an asset')

        # CREATE NEW FOLDER
        def onCreateFolder():
            self.assetOptionPanel.setMode(AssetOptionPanel.MODE_NEW_FOLDER)

        # CREATE NEW ASSET
        def onCreateAsset():
            filename = QFileDialog.getOpenFileName(self, "Choose image file", "", "Images(*.png)")
            if filename[0]:
                self.prevAsset = self.assetView.getCurrentOriginalPixmap()

                self.assetView.setPhoto(QPixmap(filename[0]))
                self.stepper.setVisible(False)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_CONFIRM_CREATE)
            else:
                print("no file selected")

        # CANCEL NEW FOLDER
        def onCancel():
            if self.assetOptionPanel.getCurrentMode() == AssetOptionPanel.MODE_NEW_FOLDER:
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_FOLDER)

            elif self.assetOptionPanel.getCurrentMode() == AssetOptionPanel.MODE_CONFIRM_CREATE:
                self.stepper.setVisible(True)
                self.assetView.setPhoto(self.prevAsset)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_FOLDER)

            elif self.assetOptionPanel.getCurrentMode() == AssetOptionPanel.MODE_CONFIRM_UPDATE:
                self.stepper.setVisible(True)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_VIEW_ASSET)

        # CANCEL NEW ASSET
        def onCancelCreateAsset():
            self.assetOptionPanel.setMode(AssetOptionPanel.MODE_VIEW_ASSET)

        # CONFIRM NEW FOLDER():
        def onConfirmNewFolder(fname):
            fname = fname.replace('-', '')
            fname = fname.replace('.', '')

            if fname == '':
                print("folder name cant be empty")
                return

            def onsuccess(result):
                print('create folder success ', result)
                self.assetView.setPhoto(None)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_NONE)
                self.__fetchHierarchy()

            item = self.hierarchy.getHighlightedItem()
            itemdict = self.hierarchy.getHighlightedDict()
            path = str(self.hierarchy.model.getNextId()) + '-' + str(item.getId()) + '-' + fname
            connector.addFile(fname, path, onsuccess, lambda x, y: print('erro', x, y), lambda: None)

        # CONFIRM NEW ASSET
        def onConfirmNewAsset(fname):
            fname = fname.replace('-', '')
            fname = fname.replace('.', '')

            if fname == '':
                print("file name cant be empty")
                return

            def onsuccess(result):
                print('create file success ', result)
                self.assetView.setPhoto(None)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_NONE)
                self.__fetchHierarchy()

            item = self.hierarchy.getHighlightedItem()
            itemdict = self.hierarchy.getHighlightedDict()
            path = str(self.hierarchy.model.getNextId()) + '-' + str(item.getId()) + '-' + fname
            connector.addFile(fname, path, onsuccess, lambda x, y: print('erro', x, y), lambda: None)

        self.assetOptionPanel.setOnClickDeleteFolder(onDeleteFolder)
        self.assetOptionPanel.setOnClickDeleteAsset(onDeleteAsset)
        self.assetOptionPanel.setOnClickCreateFolder(onCreateFolder)
        self.assetOptionPanel.setOnClickCreate(onCreateAsset)
        self.assetOptionPanel.setOnClickCancel(onCancel)
        self.assetOptionPanel.setOnClickConfirmNewFolder(onConfirmNewFolder)
        self.assetOptionPanel.setOnClickConfirmCreate(onConfirmNewAsset)


    def __initialize(self):
        self.__fetchHierarchy()
        self.__setupOptionPanel()

app = QApplication(sys.argv)

dialog = LoginDialog()
dialog.setWindowTitle("Asset Manager Client Login")
dialog.show()
loginResult = dialog.exec_()

if loginResult != QDialog.Accepted:
    sys.exit(app.exec_())

userwin = ManageAssetWindow()
userwin.show()

sys.exit(app.exec_())