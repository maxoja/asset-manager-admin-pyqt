from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget, QTableWidgetItem, QHeaderView


class UserListView(QWidget):
    def __init__(self, titleText='User List View', parent=None):
        QWidget.__init__(self, parent)

        self.title = UserListTitle(titleText)
        self.table = UserListTable()

        layout = QVBoxLayout(self)
        layout.addWidget(self.title)
        layout.addWidget(self.table)

    def setTitle(self, text):
        self.title.setText(text)

    def addUser(self, userDict):
        self.table.addUser(userDict)

    def removeUser(self, key, value):
        self.table.removeUser(key, value)


class UserListTitle(QLabel):
    def __init__(self, text, parent=None):
        super(UserListTitle, self).__init__(text, parent)


class UserListTable(QTableWidget):
    def __init__(self):
        super(UserListTable, self).__init__()
        self.setColumnCount(2)
        self.keys = ['username', 'password']
        self.setHorizontalHeaderLabels(self.keys)

        header = self.horizontalHeader()
        for i in range(len(self.keys)):
            header.setSectionResizeMode(i, QHeaderView.Stretch)

    def addUser(self, userDict):
        self.setRowCount(self.rowCount()+1)
        latestRowIndex = self.rowCount()-1

        for i, key in zip(range(2),['username', 'password']):
            self.setItem(latestRowIndex, i, QTableWidgetItem(userDict[key]))

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
    app = QApplication(sys.argv)

    widget = UserListView()

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

    widget.show()
    sys.exit(app.exec_())
