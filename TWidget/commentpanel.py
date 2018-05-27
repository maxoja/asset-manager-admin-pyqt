from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QFont
import sys


class CommentItem(QPushButton):
    def __init__(self, parent=None, **model):
        super(CommentItem, self).__init__(parent)
        self.setMinimumHeight(50)
        self.setMinimumWidth(250)
        self.model = model

        self.setupRepresentation()

        self.onClick = self.__defaultOnClick
        self.clicked.connect(self.__onClickPlug)

    def setupRepresentation(self):
        layout = QHBoxLayout(self)

        titleFont = QFont("", 15, QFont.Bold)
        titleLabel = QLabel('"' + self.model['title'] + '"')
        titleLabel.setFont(titleFont)

        ownerFont = QFont("", 10, QFont.Thin)
        ownerLabel = QLabel("by:" + self.model['owner'] + " - " + self.model['time'])
        ownerLabel.setFont(ownerFont)

        layout.addWidget(titleLabel)
        layout.addStretch()
        layout.addWidget(ownerLabel)

    def setOnClick(self, onClick):
        self.onClick = onClick

    def __onClickPlug(self):
        self.onClick(self.model)

    def __defaultOnClick(self, model):
        print(model)


class CommentPanel(QWidget):
    def __init__(self, parent=None):
        super(CommentPanel, self).__init__(parent)
        self.comments = []
        self.onClickComment = self.__defaultOnClickComment

        layout = QVBoxLayout(self)
        layout.setSpacing(0)
        layout.addStretch(0)

    def __defaultOnClickComment(self, model):
        print(model)

    def __applyOnClickComment(self):
        for comment in self.comments:
            if isinstance(comment, CommentItem):
                comment.setOnClick(self.onClickComment)

    def setOnClickComment(self, onClick):
        self.onClickComment = onClick
        self.__applyOnClickComment()

    def addComment(self, **kwargs):
        newComment = CommentItem(**kwargs)
        newComment.setOnClick(self.onClickComment)
        self.comments.append(newComment)
        self.layout().removeItem(self.layout().itemAt(self.layout().count()-1))
        self.layout().addWidget(newComment)
        self.layout().addStretch(0)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    def onClickItem(comment):
        print("hello moon")
        print(comment)
    # widget = CommentItem(title="comment 1", owner="maxoja", time="19:00 1 April")
    # widget.show()
    widget = CommentPanel()
    widget.addComment(title="comment 1", owner="maxoja", time="19:00 1 April")
    widget.addComment(title="comment 2", owner="maxoja", time="19:00 2 April")
    widget.addComment(title="comment 3", owner="maxoja", time="19:00 3 April")
    widget.addComment(title="comment 4", owner="maxoja", time="19:00 4 April")
    widget.addComment(title="comment 5", owner="maxoja", time="19:00 5 April")
    widget.addComment(title="comment 6", owner="maxoja", time="19:00 6 April")
    widget.setOnClickComment(onClickItem)
    widget.show()

    sys.exit(app.exec_())