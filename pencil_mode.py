
from PySide6 import QtGui, QtCore, QtWidgets
from edit_mode import EditMode

class PencilModeCls(EditMode):

    def __init__(self, outer):
        EditMode.__init__(self)
        self.outer = outer
        
    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if modifiers & QtCore.Qt.ControlModifier:
                    self.backupSprite()
                    qp = QtGui.QPainter(self.sprite)
                    qp.setPen(self.foregroundColor)
                    qp.drawLine(self.prev_x, self.prev_y,self.x,self.y)
                    qp.end()
                else:
                    self.backupSprite()
                    self.sprite.setPixel(self.x, self.y,
                                            EditMode.foregroundColor.rgba())
                    self.prev_x = self.x
                    self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.backupSprite()
                self.sprite.setPixel(self.x, self.y,
                                           EditMode.backgroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers & QtCore.Qt.ControlModifier:
            self.prev_x = self.x
            self.prev_y = self.y
        

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if modifiers & QtCore.Qt.ControlModifier:
                    self.restoreSprite()
                    qp = QtGui.QPainter(self.sprite)
                    qp.setPen(self.foregroundColor)
                    qp.drawLine(self.prev_x, self.prev_y,self.x,self.y)
                    qp.end()
                else:
                    self.sprite.setPixel(self.x, self.y,
                                            EditMode.foregroundColor.rgba())
                    self.prev_x = self.x
                    self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                self.backupSprite()
                self.sprite.setPixel(self.x, self.y,
                                           EditMode.backgroundColor.rgba())
                self.prev_x = self.x
                self.prev_y = self.y
                self.outer.repaint()

    def keyPressEvent(self, keyEvent):
        pass

    def displayPixSize(self):
        print(f'PencilModeCls --> pixSize = {self.pixSize}')

