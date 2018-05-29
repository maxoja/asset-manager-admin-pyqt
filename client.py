from TWidget import LoginDialog, UserListView, EditPanel, HierarchyPanel, StepperWidget, CommentPanel, AssetViewWidget, AssetOptionPanel
from TModel import HierarchicalModel
from PyQt5.QtWidgets import QApplication, QDialog, QWidget, QHBoxLayout, QSplitter, QLineEdit, QTextEdit, QVBoxLayout, QFileDialog
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap
import sys
from TConnect import connector, loader


class ManageAssetWindow(QWidget):
    def __init__(self):
        super(ManageAssetWindow, self).__init__()
        self.setWindowTitle("Asset Manager Client")
        self.setMinimumWidth(1000)
        self.setMinimumHeight(600)

        tree = HierarchicalModel()
        tree.add(0, name="root")

        # LEFT WIDGET
        self.hierarchy = HierarchyPanel(tree)

        # RIGHT WIDGET
        self.commentPanel = CommentPanel()
        self.commentPanel.fieldArea.disable()
        self.commentPanel.setMaximumWidth(260)

        # MID TOP WIDGET
        self.stepper = StepperWidget(5, checkpointCover=0.7)
        [self.stepper.setSecondaryText('', i) for i in range(5)]
        self.stepper.setVisible(False)

        # MID MID WIDGET
        self.prevAsset = None
        self.assetView = AssetViewWidget()
        self.assetView.setPhoto(QPixmap('img/cant-show.png'))

        # MID BOTTOM WIDGET
        self.assetOptionPanel = AssetOptionPanel()

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


    def __fetchCommentPanel(self, fileid, version):
        def onreceivecomment(comments):
            self.commentPanel.clearAll()
            self.commentPanel.fieldArea.clearAll()

            for comment in comments:
                splitted = comment['comment'].split('`')
                title = splitted[0]
                details = splitted[1]
                xy = splitted[2]
                self.commentPanel.addComment(title=title, details=details, xy=xy)

            self.commentPanel.fieldArea.enable()

        connector.getCommentList(fileid, version, onreceivecomment)

    def __fetchStepper(self, fid=None):
        def onclickstep(stepid):
            if stepid == self.stepper.numStep-1 :
                self.stepper.setCurrentStep(self.stepper.numStep-2)
                return

            self.stepper.setCurrentStep(stepid)
            versiondata = self.stepper.getData(stepid)
            print("click step", versiondata)
            firebasepath = versiondata['downloadpath']
            fileid = versiondata['fileid']

            loader.download(firebasepath, 'temp.png')
            self.assetView.setPhoto(QPixmap('temp.png'))

            self.__fetchCommentPanel(fileid, str(stepid+1))

        if fid is not None:
            fileid = fid
        else:
            fileid = self.hierarchy.getHighlightedDict()['fileid']

        def onreceive(versionList):
            print("getversion ", versionList)
            self.stepper.setNumberOfCheckpoints(max(2,len(versionList)+1))
            self.stepper.setPrimaryText('+', len(versionList))
            for i, ver in enumerate(versionList):
                ver['fileid'] = fileid
                self.stepper.setPrimaryText(ver['version'], i)
                self.stepper.setData(ver, i)

                if i == len(versionList)-1:
                    loader.download(ver['downloadpath'], 'temp.png')
                    self.assetView.setPhoto(QPixmap('temp.png'))

            self.stepper.setCurrentStep(self.stepper.numStep-2)

        connector.getVersionList(fileid, onreceive, lambda : print("error getversion of",fileid))
        self.__fetchCommentPanel(fileid, str(self.stepper.numStep-1))

        self.stepper.setOnClickCheckpoint(onclickstep)

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

                print(file)
                tree.add(selfid, parentid, name=filename, isfile=isfile, fileid=file['id'])

            self.hierarchy.reconstruct(0)

        def onclickitem(item):
            if item['isfile']:
                self.stepper.setVisible(True)
                self.__fetchStepper()
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_VIEW_ASSET)
            else:
                self.stepper.setVisible(False)
                self.assetView.setPhoto(QPixmap('img/cant-show.png'))
                self.commentPanel.fieldArea.disable()
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_FOLDER)

        self.hierarchy.setOnClickItem(onclickitem)
        connector.getFileList(ongetfiles, lambda: print("error"))

    def __setupOptionPanel(self):
        # DELETE FOLDER
        def onsuccessdeletefolder():
            self.__fetchHierarchy()
            self.stepper.setVisible(False)
            self.assetOptionPanel.setMode(AssetOptionPanel.MODE_NONE)
            self.assetView.setPhoto(QPixmap('cant-show.png'))

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
                self.loadedAsset = filename[0]
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
                self.assetView.setPhoto(self.prevAsset)
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

            if fname == '':
                print("file name cant be empty")
                return

            if fname[-4:] != '.png':
                fname += '.png'

            def onsuccess(fileid):
                print('create file success ', fileid)
                self.assetView.setPhoto(QPixmap(self.loadedAsset))
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_NONE)
                self.stepper.setVisible(True)

                def onaddedversion(uploadpath):
                    loader.upload(uploadpath, self.loadedAsset)
                    self.__fetchStepper(fileid)
                    self.__fetchHierarchy()

                connector.addVersion(fileid, '1', '.png', onaddedversion, lambda x,y:print("erro",x,y), lambda: None)

            item = self.hierarchy.getHighlightedItem()
            itemdict = self.hierarchy.getHighlightedDict()
            path = str(self.hierarchy.model.getNextId()) + '-' + str(item.getId()) + '-' + fname
            connector.addFile(fname, path, onsuccess, lambda x, y: print('erro', x, y), lambda: None)

        def onConfirmUpdate():
            nextversion = self.stepper.numStep

            def onsuccess(uploadpath):
                loader.upload(uploadpath, self.loadedAsset)
                self.__fetchStepper()
                self.stepper.setVisible(True)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_VIEW_ASSET)

            fileid = self.hierarchy.getHighlightedDict()['fileid']
            connector.addVersion(fileid, str(nextversion), '.png', onsuccess, lambda x,y: None, lambda :print('error'))

        def onUpdateAsset():
            filename = QFileDialog.getOpenFileName(self, "Choose image file", "", "Images(*.png)")
            if filename[0]:
                self.loadedAsset = filename[0]
                self.prevAsset = self.assetView.getCurrentOriginalPixmap()

                self.assetView.setPhoto(QPixmap(filename[0]))
                self.stepper.setVisible(False)
                self.assetOptionPanel.setMode(AssetOptionPanel.MODE_CONFIRM_UPDATE)
            else:
                print("no file selected")

        # ADD COMMENT
        def onClickAddComment(title, details):
            if title == '':
                return

            comment = title+'`'+details+'`'+str(self.assetView.currentRegion)
            fileid = self.hierarchy.getHighlightedDict()['fileid']
            version = str(self.stepper.currentStep+1)

            def onsuccess(comment):
                self.__fetchCommentPanel(fileid, version)

            connector.addcomment(fileid, version, comment, onsuccess)

        self.assetOptionPanel.setOnClickDeleteFolder(onDeleteFolder)
        self.assetOptionPanel.setOnClickDeleteAsset(onDeleteAsset)
        self.assetOptionPanel.setOnClickCreateFolder(onCreateFolder)
        self.assetOptionPanel.setOnClickCreate(onCreateAsset)
        self.assetOptionPanel.setOnClickCancel(onCancel)
        self.assetOptionPanel.setOnClickConfirmNewFolder(onConfirmNewFolder)
        self.assetOptionPanel.setOnClickConfirmCreate(onConfirmNewAsset)
        self.assetOptionPanel.setOnClickConfirmUpdate(onConfirmUpdate)
        self.assetOptionPanel.setOnClickUpdate(onUpdateAsset)
        self.commentPanel.setOnClickAdd(onClickAddComment)

        def onclickcomment(comment):
            coor = eval(comment['xy'])
            if len(coor) == 2:
                self.assetView.showRegion(QRect(coor[0], coor[1], coor[0], coor[1]))
            else:
                self.assetView.showRegion(QRect(coor[0], coor[1], coor[2], coor[3]))

        self.commentPanel.setOnClickComment(onclickcomment)


    def __initialize(self):
        loader.init()
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