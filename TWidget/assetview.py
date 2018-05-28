import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QWidget


class AssetViewWidget(QtWidgets.QGraphicsView):
    photoClicked = QtCore.pyqtSignal(QtCore.QPoint)

    def __init__(self, parent=None):
        super(AssetViewWidget, self).__init__(parent)
        self._zoom = 0
        self._empty = True
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(30, 30, 30)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)

    def hasPhoto(self):
        return not self._empty

    def fitInView(self, scale=True):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        if not rect.isNull():
            self.setSceneRect(rect)
            if self.hasPhoto():
                unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
                self.scale(1 / unity.width(), 1 / unity.height())
                viewrect = self.viewport().rect()
                scenerect = self.transform().mapRect(rect)
                factor = min(viewrect.width() / scenerect.width(),
                             viewrect.height() / scenerect.height())
                self.scale(factor, factor)
            self._zoom = 0

    def getCurrentOriginalPixmap(self):
        return self.originalPixmap

    def setPhoto(self, pixmap=None):
        self._zoom = 0
        self.originalPixmap = pixmap

        if pixmap and not pixmap.isNull():
            self._empty = False
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
            self._photo.setPixmap(pixmap)
        else:
            self._empty = True
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())

        self.fitInView()

    def wheelEvent(self, event):
        if self.hasPhoto():
            if event.angleDelta().y() > 0:
                factor = 1.25
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom == 0:
                self.fitInView()
            else:
                self._zoom = 0

    def toggleDragMode(self):
        if self.dragMode() == QtWidgets.QGraphicsView.ScrollHandDrag:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        elif not self._photo.pixmap().isNull():
            self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def mousePressEvent(self, event):
        if self._photo.isUnderMouse():
            self.photoClicked.emit(QtCore.QPoint(event.pos()))
        super(AssetViewWidget, self).mousePressEvent(event)

    def showRegion(self, rect):
        if not isinstance(rect, QtCore.QRect):
            assert False

        newpix = QtGui.QPixmap(self.originalPixmap)

        # brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        pen = QtGui.QPen(QtGui.QColor(255,0,0), 3)

        painter = QtGui.QPainter(newpix)
        # painter.setBrush(brush)
        painter.setPen(pen)
        painter.drawLine(rect.left(), rect.top(), rect.right(), rect.top() )
        painter.drawLine(rect.right(), rect.top(), rect.right(), rect.bottom())
        painter.drawLine(rect.right(), rect.bottom(), rect.left(), rect.bottom())
        painter.drawLine(rect.left(), rect.bottom(), rect.left(), rect.top())
        painter.end()
        self._photo.setPixmap(newpix)

# class ImageViewerWindow(QtWidgets.QWidget):
#     def __init__(self):
#         super(ImageViewerWindow, self).__init__()
#         self.viewer = PhotoViewer(self)
#         # 'Load image' button
#         self.btnLoad = QtWidgets.QToolButton(self)
#         self.btnLoad.setText('Load image')
#         self.btnLoad.clicked.connect(self.loadImage)
#         # Button to change from drag/pan to getting pixel info
#         self.btnPixInfo = QtWidgets.QToolButton(self)
#         self.btnPixInfo.setText('Enter pixel info mode')
#         self.btnPixInfo.clicked.connect(self.pixInfo)
#         self.editPixInfo = QtWidgets.QLineEdit(self)
#         self.editPixInfo.setReadOnly(True)
#         self.viewer.photoClicked.connect(self.photoClicked)
#         # Arrange layout
#         VBlayout = QtWidgets.QVBoxLayout(self)
#         VBlayout.addWidget(self.viewer)
#         HBlayout = QtWidgets.QHBoxLayout()
#         HBlayout.setAlignment(QtCore.Qt.AlignLeft)
#         HBlayout.addWidget(self.btnLoad)
#         HBlayout.addWidget(self.btnPixInfo)
#         HBlayout.addWidget(self.editPixInfo)
#         VBlayout.addLayout(HBlayout)
#
#     def loadImage(self):
#         fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open image file.","","Images (*.png *.bmp *.jpg *.jpeg)")
#         if fileName[0]:
#             self.viewer.setPhoto(QtGui.QPixmap(fileName[0]))
#         else:
#             return
#
#     def pixInfo(self):
#         self.viewer.toggleDragMode()
#
#     def photoClicked(self, pos):
#         if self.viewer.dragMode()  == QtWidgets.QGraphicsView.NoDrag:
#             self.editPixInfo.setText('%d, %d' % (pos.x(), pos.y()))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    # window = ImageViewerWindow()
    # window.setGeometry(500, 300, 800, 600)
    # window.show()

    widget = AssetViewWidget()
    image = QtGui.QPixmap("img/admin-icon.png")
    widget.setPhoto(image)
    widget.showRegion(QtCore.QRect(50,50,150,100))
    widget.show()
    sys.exit(app.exec_())