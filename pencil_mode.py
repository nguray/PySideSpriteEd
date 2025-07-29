
from PySide6 import QtGui, QtCore, QtWidgets
from edit_mode import EditMode
from rect import Rect 

class PointHandle:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.rect = Rect(0,0,0,0) 

class PencilModeCls(EditMode):

    def __init__(self, outer):
        EditMode.__init__(self)
        self.outer = outer
        self.init_mode()

    def init_mode(self):
        self.prev_x = -1
        self.prev_y = -1
        self.polygon = []
        self.polygonHandle = None
    
    def drawPolygonHandle(self, qp: QtGui.QPainter, pt: PointHandle):
        left = pt.x * EditMode.pixSize + 1
        top  = pt.y * EditMode.pixSize + 1
        right = left + EditMode.pixSize - 1
        bottom = top + EditMode.pixSize - 1
        x = int((left + right) / 2)
        y = int((top + bottom) / 2)
        s = self.pixSize/2 - 2
        pt.rect = Rect(x-s, y-s, x+s, y+s)
        r = 255-self.foregroundColor.red()
        g = 255-self.foregroundColor.green()
        b = 255-self.foregroundColor.blue()
        qp.setPen(QtGui.QColor(r, g, b, 255))
        qp.setBrush(QtGui.QColor(0, 0, 0, 0))
        qp.drawRect(pt.rect.left, pt.rect.top, pt.rect.width(), pt.rect.height())

    def drawPolygon(self, qp: QtGui.QPainter):
        lp = len(self.polygon)
        if lp>1:
            prev_pt = self.polygon[0]
            for i in range(1,lp):
                pt = self.polygon[i]
                qp.setPen(self.foregroundColor)
                qp.drawLine(prev_pt.x, prev_pt.y, pt.x,pt.y)
                prev_pt = pt
            for pt in self.polygon:
                self.drawPolygonHandle(qp, pt)

            

    def hitPolygonHandle(self,x: int,y: int)->PointHandle:
        for pt in self.polygon:
            if pt.rect.contains(x,y):
                return pt
        return None

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        mousePos -= QtCore.QPoint(EditMode.origin_x,EditMode.origin_y)
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:

                self.polygonHandle = self.hitPolygonHandle(mousePos.x(), mousePos.y())
                if self.polygonHandle is None:
                    if modifiers & QtCore.Qt.ControlModifier:
                        if len(self.polygon)==0:
                            self.backupSprite()
                            self.polygon.append(PointHandle(self.prev_x, self.prev_y))
                            self.polygon.append(PointHandle(self.x, self.y))
                            # Store previous draw pixel
                            self.prev_x = self.x
                            self.prev_y = self.y
                        else:
                            self.restoreSprite()
                            if self.x!=self.prev_x or self.y!=self.prev_y:
                                self.polygon.append(PointHandle(self.x, self.y))
                                # Store previous draw pixel
                                self.prev_x = self.x
                                self.prev_y = self.y
                        self.polygonHandle = self.polygon[-1]
                        # Updated sprite
                        qp = QtGui.QPainter(self.sprite)
                        qp.setPen(self.foregroundColor)
                        self.drawPolygon(qp)
                        qp.end()
                    else:
                        self.polygon = []
                        self.backupSprite()
                        self.sprite.setPixel(self.x, self.y,
                                                EditMode.foregroundColor.rgba())
                        # Store previous draw pixel
                        self.prev_x = self.x
                        self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                pass

    def mouseReleaseEvent(self, mouseEvent):
        pass

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        mousePos -= QtCore.QPoint(EditMode.origin_x,EditMode.origin_y)
        self.x, self.y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.InSprite(self.x, self.y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if self.polygonHandle!=None:
                    self.restoreSprite()
                    # Update last point
                    self.polygonHandle.x = self.x
                    self.polygonHandle.y = self.y
                    # Updated sprite
                    qp = QtGui.QPainter(self.sprite)
                    self.drawPolygon(qp)
                    qp.end()
                else:
                    if modifiers & QtCore.Qt.ControlModifier:
                        if self.x!=self.prev_x or self.y!=self.prev_y:
                            self.restoreSprite()
                            self.polygon.append(PointHandle(self.x, self.y))
                            # Store previous draw pixel
                            self.prev_x = self.x
                            self.prev_y = self.y
                            # Updated sprite
                            qp = QtGui.QPainter(self.sprite)
                            self.drawPolygon(qp)
                            qp.end()
                    else:
                        if self.x!=self.prev_x or self.y!=self.prev_y:
                            # Updated sprite
                            self.sprite.setPixel(self.x, self.y,
                                                EditMode.foregroundColor.rgba())
                            # Store previous draw pixel
                            self.prev_x = self.x
                            self.prev_y = self.y
                self.outer.repaint()
            elif mouseEvent.buttons() == QtCore.Qt.RightButton:
                pass

    def keyPressEvent(self, keyEvent):
        if keyEvent.key() == QtCore.Qt.Key_Return or keyEvent.key() == QtCore.Qt.Key_Enter:
            if len(self.polygon)>0:
                pt = self.polygon[-1]
                self.prev_x = pt.x
                self.prev_y = pt.x
                self.polygon = []
                self.polygonHandle = None
                self.outer.repaint()

    def displayPixSize(self):
        print(f'PencilModeCls --> pixSize = {self.pixSize}')

