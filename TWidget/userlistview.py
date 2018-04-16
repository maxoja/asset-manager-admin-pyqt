from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QLayout
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt


class UserListView(QWidget):
    def __init__(self, titleText='User List View', iconPath='', parent=None):
        QWidget.__init__(self, parent)

        self.title = UserListTitle(titleText)
        self.title.setIcon(iconPath)
        self.table = UserListTable()

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.table)

        self.setOnSelectUser(self._defaultSelect)

    def setTitle(self, text):
        self.title.setText(text)

    def addUser(self, userDict):
        self.table.addUser(userDict)

    def removeUser(self, key, value):
        self.table.removeUser(key, value)

    def setOnSelectUser(self, onSelect):
        self.table.setOnSelectUser(onSelect)

    def _defaultSelect(self, userDict):
        print(userDict)


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


class UserListTable(QTableWidget):
    def __init__(self):
        super(UserListTable, self).__init__()
        # self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnCount(2)
        self.keys = ['username', 'password']
        self.setHorizontalHeaderLabels(self.keys)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.itemClicked.connect(self._onClickCell)
        self.setOnSelectUser(self._defaultOnSelectUser)

        header = self.horizontalHeader()
        for i in range(len(self.keys)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def _onClickCell(self, clickedItem):
        result = dict()
        for i in range(self.columnCount()):
            result[self.keys[i]] = self.item(clickedItem.row(), i).text()

        self.onSelectUser(result)

    def _defaultOnSelectUser(self, userDict):
        print(userDict)

    def setOnSelectUser(self, onSelectUser):
        self.onSelectUser = onSelectUser

    def addUser(self, userDict):
        self.setRowCount(self.rowCount()+1)
        latestRowIndex = self.rowCount()-1

        for i, key in zip(range(2),['username', 'password']):
            item = QTableWidgetItem(userDict[key])
            item.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(latestRowIndex, i, item)

    def removeUser(self, key, value):
        keyIndex = self.keys.index(key)
        removingRow = -1

        for i in range(self.rowCount()):
            item = self.item(i, keyIndex)
            if item.text() == value:
                removingRow = i
                break

        if removingRow == -1:
            return False

        self.removeRow(removingRow)
        return True


if __name__ == '__main__':
    import sys
    from qtmodern import styles, windows

    app = QApplication(sys.argv)
    styles.dark(app)

    widget = UserListView(iconPath='img/admin-icon.png')

    #add users
    widget.addUser({
        'username': 'maxoja',
        'password': '123456'})
    widget.addUser({
        'username': 'tawan',
        'password': 'be slow'})
    widget.addUser({
        'username': 'dan',
        'password': 'nicechef'})
    widget.addUser({
        'username': 'drvisit',
        'password': 'senseiKami'})
    widget.addUser({
        'username': 'guy',
        'password': 'genius'})

    #remove users
    widget.removeUser('password', '123456')

    widget.setOnSelectUser(lambda userDict: QMessageBox.warning(None, 'selected user', str(userDict)))

    #change native window component appearance
    # modern = windows.ModernWindow(widget)
    # modern.show()

    widget.show()
    sys.exit(app.exec_())
