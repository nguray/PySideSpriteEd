from PySide6 import QtGui, QtCore, QtWidgets
from edit_mode import EditMode


class FillModeCls(EditMode):
    def __init__(self, outer):
        EditMode.__init__(self)
        self.outer = outer

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                self.backupSprite()
                # Get Target Color
                iTargetColor = self.sprite.pixel(self.x, self.y)
                iNewColor = self.foregroundColor.rgba()
                self.floodFill(self.x, self.y, iTargetColor, iNewColor)
                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        pass

    def keyPressEvent(self, e):
        pass

