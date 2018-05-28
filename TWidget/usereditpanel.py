from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout, QTextEdit, QLabel
from PyQt5.QtWidgets import QFormLayout, QPushButton, QLineEdit, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class UserListTitle(QWidget):
    def __init__(self, text, iconSize=26, parent=None):
        super(UserListTitle, self).__init__(parent)

        self.iconSize = iconSize
        self.iconWidget = QLabel()
        self.label = QLabel(text)

        layout = QHBoxLayout(self)
        layout.addWidget(self.iconWidget)
        layout.addWidget(self.label)
        layout.setAlignment(Qt.AlignLeft)
        layout.setContentsMargins(iconSize/3, 0, 0, 0)

    def setIcon(self, path):
        if path == '' or path == None:
            return

        pixmap = QPixmap(path)
        pixmap = pixmap.scaledToHeight(self.iconSize)
        self.iconWidget.setPixmap(pixmap)

    def setText(self, text):
        self.label.setText(text)


class EditPanel(QWidget):
    def __init__(self, parent=None):
        super(EditPanel, self).__init__(parent)
        self.additionalData = None

        self.title = UserListTitle("Edit Panel")
        self.title.setIcon("img/edit-icon.png")

        self.updateButton = QPushButton('Update')
        self.updateButton.setMinimumHeight(50)
        self.updateButton.clicked.connect(self.__onClickUpdate)
        self.onClickUpdate = self.__defaultOnClick

        self.newAdminButton = QPushButton('New Admin')
        self.newAdminButton.clicked.connect(self.__onClickNewAdmin)
        self.onClickNewAdmin = self.__defaultOnClick

        self.newCreatorButton = QPushButton('New Creator')
        self.newCreatorButton.clicked.connect(self.__onClickNewCreator)
        self.onClickNewCreator = self.__defaultOnClick

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.setStyleSheet('background-color:"red"; color:"white"')
        self.deleteButton.clicked.connect(self.__onClickDelete)
        self.onClickDelete = self.__defaultOnClick

        buttonBoxLayout = QHBoxLayout()
        buttonBoxLayout.addStretch()
        buttonBoxLayout.addWidget(self.newAdminButton)
        buttonBoxLayout.addWidget(self.newCreatorButton)
        buttonBoxLayout.addWidget(self.deleteButton)

        self.editFrame = EditFrame()
        self.editFrame.layout().addLayout(buttonBoxLayout)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.addWidget(self.title)
        layout.addWidget(self.editFrame)
        layout.addWidget(self.updateButton)

    def addEditRow(self, key, widgetType):
        self.editFrame.addEditRow(key, widgetType)

    def setEditValue(self, key, value):
        self.editFrame.setEditValue(key, value)

    def getEditValue(self, key):
        return self.editFrame.getEditValue(key)

    def getEditValueDict(self):
        return self.editFrame.getEditValueDict()

    def setAdditionalData(self, data):
        self.additionalData = data

    def getAdditionalData(self):
        return self.additionalData

    def setOnClickUpdate(self, onClick):
        self.onClickUpdate = onClick

    def setOnClickDelete(self, onClick):
        self.onClickDelete = onClick

    def setOnClickNewCreator(self, onClick):
        self.onClickNewCreator = onClick

    def __onClickNewCreator(self):
        self.onClickNewCreator(self.editFrame.getEditValueDict(), self.additionalData)

    def setOnClickNewAdmin(self, onClick):
        self.onClickNewAdmin = onClick

    def __onClickNewAdmin(self):
        self.onClickNewAdmin(self.editFrame.getEditValueDict(), self.additionalData)

    def __onClickUpdate(self):
        self.onClickUpdate(self.editFrame.getEditValueDict(), self.additionalData)

    def __onClickDelete(self):
        self.onClickDelete(self.editFrame.getEditValueDict(), self.additionalData)

    def __defaultOnClick(self, dictValues, additionalData):
        print(dictValues, additionalData)


class EditFrame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.setFrameStyle(QFrame.Sunken | QFrame.Box)

        self.editWidgets = dict()

        self.form = QFormLayout()

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setDirection(QVBoxLayout.Down)
        layout.addLayout(self.form)
        layout.addStretch()

    def addEditRow(self, key, WidgetType):
        widget = WidgetType()
        self.editWidgets[key] = widget
        self.form.addRow(key, widget)

    def getEditValue(self, key):
        widget = self.editWidgets[key]
        if isinstance(widget, QLineEdit):
            return widget.text()
        else:
            return widget.toPlainText()

    def setEditValue(self, key, value):
        self.editWidgets[key].setText(value)

    def getEditValueDict(self):
        return {key: self.getEditValue(key) for key in self.editWidgets}


if __name__ == '__main__':
    import sys
    from PyQt5.QtWidgets import QApplication
    from qtmodern import styles, windows

    app = QApplication(sys.argv)
    styles.dark(app)

    widget = EditPanel()
    widget.addEditRow('Employment ID', QLineEdit)
    widget.addEditRow('Display Name', QLineEdit)
    widget.addEditRow('Username', QLineEdit)
    widget.addEditRow('Password', QLineEdit)
    widget.addEditRow('Email', QLineEdit)
    widget.addEditRow('Notes', QTextEdit)

    # mwidget = windows.ModernWindow(widget)
    # mwidget.show()
    widget.show()

    sys.exit(app.exec_())
