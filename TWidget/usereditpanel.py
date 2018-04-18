from PyQt5.QtWidgets import QFrame, QWidget, QVBoxLayout, QTextEdit
from PyQt5.QtWidgets import QFormLayout, QPushButton, QLayout, QBoxLayout, QLineEdit, QHBoxLayout
from PyQt5.QtCore import Qt


class EditPanel(QWidget):
    def __init__(self, parent=None):
        super(EditPanel, self).__init__(parent)
        self.additionalData = None

        self.updateButton = QPushButton('Update')
        self.updateButton.setMinimumHeight(50)
        self.updateButton.clicked.connect(self.__onClickUpdate)
        self.onClickUpdate = self.__defaultOnClick

        self.deleteButton = QPushButton('Delete')
        self.deleteButton.setStyleSheet('background-color:"red"; color:"white"')
        self.deleteButton.clicked.connect(self.__onClickDelete)
        self.onClickDelete = self.__defaultOnClick
        deleteLayout = QHBoxLayout()
        deleteLayout.addStretch()
        deleteLayout.addWidget(self.deleteButton)

        self.editFrame = EditFrame()
        self.editFrame.layout().addLayout(deleteLayout)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.addWidget(self.editFrame)
        layout.addWidget(self.updateButton)

    def addEditRow(self, key, widgetType):
        self.editFrame.addEditRow(key, widgetType)

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
