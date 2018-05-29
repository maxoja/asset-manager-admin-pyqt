# from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QLayout
# from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView
# from PyQt5.QtGui import QPixmap, QImage, QPainter, QBrush, QColor
# from PyQt5.QtCore import Qt, QRectF, QRect
#
#
# class LoadingFilter(QLabel):
#     def __init__(self, parent=None):
#         super(LoadingFilter, self).__init__(parent)
#         self.setFixedSize(10000, 10000)
#         self.loading = False
#         self.hideLoading()
#
#     def showLoading(self):
#         print(555)
#         self.loading = True
#         self.setAttribute(Qt.WA_TransparentForMouseEvents, False)
#         self.update()
#
#     def hideLoading(self):
#         self.loading = False
#         self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
#         self.update()
#
#     def paintEvent(self, a0):
#         print(666)
#         painter = QPainter(self)
#         if self.loading:
#             brush = QBrush(QColor(0, 0, 0, 150))
#         else:
#             brush = QBrush(QColor(0, 0, 0, 0))
#         painter.setBrush(brush)
#         painter.drawRect(QRect(-100, -100, self.width(), self.height()))
#         painter.end()
#
# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)
#
#     # widget = CommentItem(title="comment 1", owner="maxoja", time="19:00 1 April")
#     # widget.show()
#     widget = LoadingFilter()
#     widget.show()
#
#     sys.exit(app.exec_())
