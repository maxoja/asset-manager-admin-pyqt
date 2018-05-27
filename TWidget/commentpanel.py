from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton, QLayout, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit, QTextEdit, QScrollArea
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import sys


class CommentItem(QPushButton):
    def __init__(self, parent=None, **model):
        super(CommentItem, self).__init__(parent)
        self.setMinimumHeight(50)
        self.setMinimumWidth(250)
        self.model = model

        self.setupRepresentation()

        self.onClickComment = self.__defaultOnClick
        self.clicked.connect(self.__onClickPlug)

    def setupRepresentation(self):
        layout = QHBoxLayout(self)

        titleFont = QFont("", 15, QFont.Bold)
        titleLabel = QLabel(self.model['title'])
        titleLabel.setFont(titleFont)

        ownerFont = QFont("", 10, QFont.Thin)
        ownerLabel = QLabel("by:" + self.model['owner'] + " - " + self.model['time'])
        ownerLabel.setFont(ownerFont)

        layout.addWidget(titleLabel)
        layout.addStretch()
        layout.addWidget(ownerLabel)

    def setOnClickComment(self, onClick):
        self.onClickComment = onClick

    def __onClickPlug(self):
        # for w in self.parent().children():
        #     if isinstance(w, CommentItem):
        #         if w is self:
        #             w.setDisabled(True)
        #         else:
        #             w.setEnabled(True)

        self.onClickComment(self.model)

    def __defaultOnClick(self, model):
        print(model)


class CommentPanel(QWidget):
    def __init__(self, parent=None):
        super(CommentPanel, self).__init__(parent)
        self.comments = []
        self.onClickComment = self.__defaultOnClickComment

        titleFont = QFont("", 15, QFont.Bold)
        self.label = QLabel("  Comment")
        self.label.setFont(titleFont)

        areawidget = QWidget()
        scrollarea = QScrollArea()

        self.commentLayout = QVBoxLayout()
        self.commentLayout.setAlignment(Qt.AlignTop)
        self.commentLayout.setSpacing(0)
        self.commentLayout.addStretch(0)
        self.commentLayout.setSizeConstraint(QLayout.SetMinAndMaxSize)
        areawidget.setLayout(self.commentLayout)

        self.fieldArea = AddCommentArea()
        scrollarea.setWidget(areawidget)

        outerlayout = QVBoxLayout()
        outerlayout.addWidget(self.label)
        outerlayout.addWidget(scrollarea)
        outerlayout.addWidget(self.fieldArea)
        outerlayout.setStretch(1, 0)
        outerlayout.setContentsMargins(0, 10, 0, 0)

        self.setLayout(outerlayout)

    def __defaultOnClickComment(self, model):
        print(model)

    def __applyOnClickComment(self):
        for comment in self.comments:
            if isinstance(comment, CommentItem):
                comment.setOnClickComment(self.onClickComment)

    def setOnClickComment(self, onClick):
        self.onClickComment = onClick
        self.__applyOnClickComment()

    def setOnClickAdd(self, onClick):
        self.fieldArea.setOnClickAdd(onClick)

    def addComment(self, **kwargs):
        layout = self.commentLayout

        newComment = CommentItem(**kwargs)
        newComment.setOnClickComment(self.onClickComment)
        self.comments.append(newComment)
        layout.removeItem(layout.itemAt(layout.count()-1))
        layout.addWidget(newComment)
        layout.addStretch(0)
        self.updateGeometry()

    def clearAll(self):
        layout = self.commentLayout
        while layout.count() > 0:
            layout.removeItem(layout.itemAt(layout.count()-1))

        layout.addStretch(0)
        self.comments.clear()


class AddCommentArea(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.setMaximumHeight(150)

        self.titleField = QLineEdit()
        self.titleField.setPlaceholderText("Comment Title")

        self.detailField = QTextEdit()
        self.detailField.setPlaceholderText("Comment Details")

        self.addButton = QPushButton("Add Comment")
        self.addButton.clicked.connect(self.__onclickadd)
        self.onclickadd = self.__defaultOnAdd

        layout = QVBoxLayout(self)
        layout.addWidget(self.titleField)
        layout.addWidget(self.detailField)
        layout.addWidget(self.addButton)

    def __onclickadd(self):
        self.onclickadd(self.titleField.text(), self.detailField.toPlainText())

    def setOnClickAdd(self, onclick):
        self.onclickadd = onclick

    def __defaultOnAdd(self, title, detail):
        print("title=",title,", detail=", detail)

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
    widget.setOnClickComment(onClickItem)
    widget.setMinimumHeight(600)
    widget.show()

    widget.clearAll()
    widget.addComment(title="comment 5", owner="maxoja", time="19:00 5 April")
    widget.addComment(title="comment 6", owner="maxoja", time="19:00 6 April")
    widget.addComment(title="comment 7", owner="maxoja", time="19:00 5 April")
    widget.addComment(title="comment 8", owner="maxoja", time="19:00 6 April")
    widget.addComment(title="comment 9", owner="maxoja", time="19:00 5 April")
    widget.addComment(title="comment 7", owner="maxoja", time="19:00 5 April")
    widget.addComment(title="comment 8", owner="maxoja", time="19:00 6 April")
    widget.addComment(title="comment 9", owner="maxoja", time="19:00 5 April")
    widget.addComment(title="comment 7", owner="maxoja", time="19:00 5 April")
    widget.addComment(title="comment 8", owner="maxoja", time="19:00 6 April")
    widget.addComment(title="comment 9", owner="maxoja", time="19:00 5 April")

    # widget = AddCommentArea()
    # widget.show()

    sys.exit(app.exec_())