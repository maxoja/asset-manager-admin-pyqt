from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication, QLineEdit


class AssetOptionPanel(QWidget):
    MODE_NONE = 0
    MODE_NEW_FOLDER = 1
    MODE_VIEW_ASSET = 2
    MODE_FOLDER = 3
    MODE_CONFIRM_CREATE = 4
    MODE_CONFIRM_UPDATE = 5

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.field = QLineEdit()

        self.noneLabel = QLabel("please select a folder/an asset")

        self.createFolderButton = QPushButton("Create New Folder")
        self.onclickcreatefolder = self.__defaultOnClickCreateFolder
        self.createFolderButton.clicked.connect(self.__onClickCreateFolderPlug)

        self.deleteAssetButton = QPushButton("Delete This Asset")
        self.onclickdeleteasset = self.__defaultOnClickDeleteAsset
        self.deleteAssetButton.clicked.connect(self.__onClickDeleteAssetPlug)

        self.deleteFolderButton = QPushButton("Delete This Folder")
        self.onclickdeletefolder = self.__defaultOnClickDeleteFolder
        self.deleteFolderButton.clicked.connect(self.__onClickDeleteFolderPlug)

        self.cancelButton = QPushButton("Cancel")
        self.onclickcancel = self.__defaultOnClickCancel
        self.cancelButton.clicked.connect(self.__onClickCancelPlug)

        self.createButton = QPushButton("Create New Asset")
        self.onclickcreate = self.__defaultOnClickCreate
        self.createButton.clicked.connect(self.__onClickCreatePlug)

        self.updateButton = QPushButton("Update This Asset")
        self.onclickupdate = self.__defaultOnClickUpdate
        self.updateButton.clicked.connect(self.__onClickUpdatePlug)

        self.confirmUpdateButton = QPushButton("Confirm and upload new version")
        self.onclickconfirmupdate = self.__defaultOnClickConfirmUpdate
        self.confirmUpdateButton.clicked.connect(self.__onClickConfirmUpdatePlug)

        self.confirmCreateButton = QPushButton("Confirm and upload new asset")
        self.onclickconfirmcreate = self.__defaultOnClickConfirmCreate
        self.confirmCreateButton.clicked.connect(self.__onClickConfirmCreatePlug)

        self.toggleButton = QPushButton("Toggle Comment")
        self.onclicktogglecomment = self.__defaultOnClickToggle
        self.toggleButton.clicked.connect(self.__onClickTogglePlug)

        self.confirmNewFolderButton = QPushButton("Confirm Create New Folder")
        self.onclickconfirmnewfolder = self.__defaultOnClickConfirmNewFoler
        self.confirmNewFolderButton.clicked.connect(self.__onClickConfirmNewFolderPlug)

        layout = QHBoxLayout(self)

        self.setMode(self.MODE_NONE)

    def getCurrentMode(self):
        return self.currentmode

    def setMode(self, mode):
        assert mode in [ 0, 1, 2, 3, 4, 5]

        self.currentmode = mode

        self.__clearLayout()

        if mode == self.MODE_NONE:
            self.layout().addWidget(self.noneLabel)

        elif mode == self.MODE_NEW_FOLDER:
            self.layout().addWidget(self.field)
            self.layout().addWidget(self.confirmNewFolderButton)
            self.layout().addWidget(self.cancelButton)

        elif mode == self.MODE_VIEW_ASSET:
            self.layout().addWidget(self.updateButton)
            self.layout().addWidget(self.deleteAssetButton)

        elif mode == self.MODE_FOLDER:
            self.layout().addWidget(self.createFolderButton)
            self.layout().addWidget(self.createButton)
            self.layout().addWidget(self.deleteFolderButton)

        elif mode == self.MODE_CONFIRM_CREATE:
            self.layout().addWidget(self.field)
            self.layout().addWidget(self.confirmCreateButton)
            self.layout().addWidget(self.cancelButton)

        elif mode == self.MODE_CONFIRM_UPDATE:
            self.layout().addWidget(self.confirmUpdateButton)
            self.layout().addWidget(self.cancelButton)


    def __clearLayout(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

    # Confirm New Folder
    def setOnClickConfirmNewFolder(self, onclick):
        self.onclickconfirmnewfolder = onclick

    def __defaultOnClickConfirmNewFoler(self, fname):
        print("confirm new folder:", fname)

    def __onClickConfirmNewFolderPlug(self):
        self.onclickconfirmnewfolder(self.field.text())

    # Toggle
    def setOnClickToggle(self, onclick):
        self.onclicktogglecomment = onclick

    def __defaultOnClickToggle(self):
        print("click toggle")

    def __onClickTogglePlug(self):
        self.onclicktogglecomment()

    # Create Folder
    def setOnClickCreateFolder(self, onclick):
        self.onclickcreatefolder = onclick

    def __defaultOnClickCreateFolder(self):
        print("click create folder")

    def __onClickCreateFolderPlug(self):
        self.onclickcreatefolder()

    # Delete Asset
    def setOnClickDeleteAsset(self, onclick):
        self.onclickdeleteasset = onclick

    def __defaultOnClickDeleteAsset(self):
        print("click delete asset")

    def __onClickDeleteAssetPlug(self):
        self.onclickdeleteasset()

    # Delete Folder
    def setOnClickDeleteFolder(self, onclick):
        self.onclickdeleteasset = onclick

    def __defaultOnClickDeleteFolder(self):
        print("click delete asset")

    def __onClickDeleteFolderPlug(self):
        self.onclickdeleteasset()

    # Cancel
    def setOnClickCancel(self, onclick):
        self.onclickcancel = onclick

    def __defaultOnClickCancel(self):
        print("click cancel")

    def __onClickCancelPlug(self):
        self.onclickcancel()

    # Create
    def setOnClickCreate(self, onclick):
        self.onclickcreate = onclick

    def __defaultOnClickCreate(self):
        print("click create")

    def __onClickCreatePlug(self):
        self.onclickcreate()

    # Update
    def setOnClickUpdate(self, onclick):
        self.onclickupdate = onclick

    def __defaultOnClickUpdate(self):
        print("click update")

    def __onClickUpdatePlug(self):
        self.onclickupdate()

    # Confirm Update
    def setOnClickConfirmUpdate(self, onclick):
        self.onclickconfirmupdate = onclick

    def __defaultOnClickConfirmUpdate(self):
        print("click confirm update")

    def __onClickConfirmUpdatePlug(self):
        self.onclickconfirmupdate()

    # Confirm Create
    def setOnClickConfirmCreate(self, onclick):
        self.onclickconfirmcreate = onclick

    def __defaultOnClickConfirmCreate(self, fname):
        print("click confirm create:", fname)

    def __onClickConfirmCreatePlug(self):
        self.onclickconfirmcreate(self.field.text())



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    # window = ImageViewerWindow()
    # window.setGeometry(500, 300, 800, 600)
    # window.show()

    widget = AssetOptionPanel()
    widget.setMode(widget.MODE_FOLDER)
    widget.setMode(widget.MODE_VIEW_ASSET)
    widget.setMode(widget.MODE_NEW_ASSET)
    widget.setMode(widget.MODE_CONFIRM_CREATE)
    widget.setMode(widget.MODE_CONFIRM_UPDATE)
    widget.show()
    sys.exit(app.exec_())