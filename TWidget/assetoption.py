from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QApplication


class AssetOptionPanel(QWidget):
    MODE_NONE = 0
    MODE_NEW_ASSET = 1
    MODE_VIEW_ASSET = 2
    MODE_FOLDER = 3
    MODE_CONFIRM_CREATE = 4
    MODE_CONFIRM_UPDATE = 5

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.noneLabel = QLabel("please select a folder/an asset")

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

        layout = QHBoxLayout(self)

        self.setMode(self.MODE_NONE)

    def setMode(self, mode):
        assert mode in [ 0, 1, 2, 3, 4, 5]

        self.__clearLayout()

        if mode == self.MODE_NONE:
            self.layout().addWidget(self.noneLabel)

        elif mode == self.MODE_NEW_ASSET:
            self.layout().addWidget(self.confirmCreateButton)
            self.layout().addWidget(self.cancelButton)

        elif mode == self.MODE_VIEW_ASSET:
            self.layout().addWidget(self.updateButton)

        elif mode == self.MODE_FOLDER:
            self.layout().addWidget(self.createButton)

        elif mode == self.MODE_CONFIRM_CREATE:
            self.layout().addWidget(self.confirmCreateButton)
            self.layout().addWidget(self.cancelButton)

        elif mode == self.MODE_CONFIRM_UPDATE:
            self.layout().addWidget(self.confirmUpdateButton)
            self.layout().addWidget(self.cancelButton)


    def __clearLayout(self):
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().setParent(None)

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

    def __defaultOnClickConfirmCreate(self):
        print("click confirm create")

    def __onClickConfirmCreatePlug(self):
        self.onclickconfirmcreate()



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