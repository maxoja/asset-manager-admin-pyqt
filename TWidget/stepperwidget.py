from PyQt5.QtWidgets import QApplication, QWidget, QLayout, QSizePolicy, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QPaintEvent, QPainter, QPen, QBrush, QColor, QMouseEvent, QTextOption
from PyQt5.QtCore import Qt, QRectF
import sys


def layout_widgets(layout):
    return (layout.itemAt(i) for i in range(layout.count()))


class StepperCheckpoint(QWidget):
    STATE_PASSIVE = 0
    STATE_ACTIVE = 1
    STATE_CURRENT = 2

    def __init__(self, id, area, visualSize, onClick, initState=STATE_PASSIVE):
        QWidget.__init__(self)
        self.id = id
        self.data = None
        self.area = area
        self.visualSize = visualSize
        self.state = initState
        self.onClick = onClick
        self.primaryText = str(id)
        self.secondaryText = "hello"
        self.x = 0
        self.top = self.height()/2 - self.visualSize/2
        self.left = self.x - self.visualSize/2

        self.setMouseTracking(True)

    def setState(self, state):
        assert state in [self.STATE_CURRENT, self.STATE_ACTIVE, self.STATE_PASSIVE]
        self.state = state

    def setOnClick(self, onClick):
        self.onClick = onClick

    def setData(self, data):
        self.data = data

    def getData(self):
        return self.data

    def setPrimaryText(self, text):
        self.primaryText = text

    def getPrimaryText(self):
        return self.primaryText

    def setSecondaryText(self, text):
        self.secondaryText = text

    def getSecondaryText(self):
        return self.secondaryText

    def setDrawParameters(self, x, area, visualSize):
        self.area = area
        self.visualSize = visualSize
        self.x = x

    def paintEvent(self, paintEvent):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.NoPen))

        #DEBUG Bounding Box
        #painter.setBrush(QBrush(Qt.lightGray))
        #painter.drawRect(0,0,self.width(), self.height())

        if self.state == self.STATE_PASSIVE:
            painter.setBrush(QBrush(QColor(0,200,255,30)))
        elif self.state == self.STATE_ACTIVE:
            painter.setBrush(QBrush(QColor(0,200,255,100)))
        elif self.state == self.STATE_CURRENT:
            painter.setBrush(QBrush(QColor(0, 200, 255, 255)))

        self.top = self.height()/2 - self.visualSize/2
        self.left = self.x - self.visualSize/2

        painter.drawPie(self.left, self.top, self.visualSize, self.visualSize, 0, 5760*(16*360))

        painter.setPen(QPen(QColor(0,0,0)))
        painter.drawText(QRectF(self.left, self.top, self.visualSize, self.visualSize), Qt.AlignCenter, self.primaryText)
        painter.drawText(QRectF(self.left-self.visualSize, self.top+self.visualSize, self.visualSize*3, self.visualSize/2), Qt.AlignCenter, self.secondaryText)

    def checkMouse(self, mx, my):
        if (mx < self.left or mx > self.left + self.visualSize) or (my < self.top or my > self.top + self.visualSize):
            return False
        else:
            return True

    def mousePressEvent(self, event):
        if self.checkMouse(event.x(), event.y()):
            # print(self.id)
            self.onClick(self.id)

    # def mouseMoveEvent(self, event):
        # if self.checkMouse(event.x(), event.y()):
            # print("Mouse entered " + str(self.id) + " at (" + str(event.x()) + "," + str(event.y()) + ")")


class StepperWidget(QWidget):
    def __init__(self, numStep, parent=None, marginY=5, checkpointCover=0.5):
        QWidget.__init__(self, parent)

        self.numStep = numStep
        self.marginY = marginY
        self.checkpointCover = checkpointCover
        self.checkpoints = dict()
        self.currentStep = 0

        self.__calculateCheckpointArea()
        self.__calculateCheckpointVisualSize()
        self.__calculateBridgeLength()
        self.__setProperMargin()

        self.setMinimumSize(200, 50)

        # print('width:', self.width())
        # print('area:', self.checkpointArea)
        # print('visual:', self.checkpointVisualSize)
        # print('bridge:', self.bridgeLength)

        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)

        for i in range(numStep):
            self.checkpoints[i] = StepperCheckpoint(i, self.checkpointArea, self.checkpointVisualSize, self.__onClickCheckpoint)
            layout.addWidget(self.checkpoints[i])

        self.setLayout(layout)
        self.setCurrentStep(0)

    def setCurrentStep(self, currentStep):
        self.currentStep = currentStep

        for i, checkpoint in self.checkpoints.items():
            if i < currentStep:
                # print('---')
                checkpoint.setState(StepperCheckpoint.STATE_ACTIVE)
            elif i == currentStep:
                checkpoint.setState(StepperCheckpoint.STATE_CURRENT)
            elif i > currentStep:
                checkpoint.setState(StepperCheckpoint.STATE_PASSIVE)

        self.update()

    def setOnClickCheckpoint(self, onClick):
        for checkpoint in self.checkpoints.values():
            checkpoint.setOnClick(onClick)

    def setData(self, data, id):
        self.checkpoints[id].setData(data)

    def getData(self, id):
        return self.checkpoins[id].getData()

    def setPrimaryText(self, text, id):
        self.checkpoints[id].setPrimaryText(text)

    def getPrimaryText(self, id):
        return self.checkpoints[id].getPrimaryText()

    def setSecondaryText(self, text, id):
        self.checkpoints[id].setSecondaryText(text)

    def getSecondaryText(self, id):
        return self.checkpoints[id].getSecondaryText()

    def __calculateCheckpointArea(self):
        checkpointArea = self.width()/(self.numStep+1)

        if checkpointArea + 2*self.marginY > self.height():
            checkpointArea = self.height() - 2*self.marginY

        self.checkpointArea = checkpointArea

    def __calculateCheckpointVisualSize(self):
        self.checkpointVisualSize = self.checkpointCover * self.checkpointArea

    def __calculateBridgeLength(self):
        w, area, visual, step = self.width(), self.checkpointArea, self.checkpointVisualSize, self.numStep
        self.bridgeLength = ((w - area) - visual*(step-1) - area)/(step-1)

    def __setProperMargin(self):
        self.setContentsMargins(self.checkpointArea / 2, self.marginY, self.checkpointArea / 2, self.marginY)

    def __onClickCheckpoint(self, id):
        self.setCurrentStep(id)

    def paintEvent(self, paintEvent):
        self.__calculateCheckpointArea()
        self.__calculateCheckpointVisualSize()
        self.__calculateBridgeLength()
        self.__setProperMargin()

        # print()
        # print('width:', self.width())
        # print('area:', self.checkpointArea)
        # print('visual:', self.checkpointVisualSize)
        # print('bridge:', self.bridgeLength)

        # for checkpoint in self.checkpoints.values():
        #     checkpoint.setDrawParameters(self.checkpointArea, self
        #     checkpoint.setDrawParameters(self.checkpointArea, self.checkpointVisualSize)

        checkpointX = []
        t = (self.width()-self.checkpointArea)/self.numStep + 1
        halfVisual = self.checkpointVisualSize/2
        edgeArea = self.checkpointArea/2

        painter = QPainter(self)
        for i in range(self.numStep-1):
            x1 = self.checkpointArea + halfVisual + i*(self.checkpointVisualSize + self.bridgeLength)
            x2 = x1 + self.bridgeLength
            y = self.height()/2
            painter.drawLine(x1, y, x2, y)

            checkpointX.append(x1 - edgeArea - i*t - halfVisual)
        checkpointX.append(x2 - edgeArea - (self.numStep-1)*t + halfVisual)

        for checkpoint, x in zip(self.checkpoints.values(), checkpointX):
            checkpoint.setDrawParameters(x, self.checkpointArea, self.checkpointVisualSize)

        # painter.drawLine(0, 0, self.width(), self.height())
        # painter.drawLine(self.checkpointArea/2, 0, self.checkpointArea/2, self.height())
        # painter.drawLine(self.width() - self.checkpointArea/2, 0, self.width()-self.checkpointArea/2, self.height())



if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    # layout = QVBoxLayout()
    # widget = StepperWidget(5,parent=window)
    # layout.addWidget(widget)
    # layout.setContentsMargins(0,0,0,0)
    # window.setLayout(layout)
    window = StepperWidget(4)
    window.setCurrentStep(2)
    window.setPrimaryText('v1.0', 0)
    window.setPrimaryText('v1.1', 1)
    window.setPrimaryText('v1.2', 2)
    window.setPrimaryText('v1.3', 3)
    window.setSecondaryText('release', 0)
    window.setSecondaryText('debug', 1)
    window.setSecondaryText('refact', 2)
    window.setSecondaryText('update', 3)
    window.show()

    sys.exit(app.exec_())
