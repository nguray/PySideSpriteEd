
from PySide6 import QtGui, QtCore, QtWidgets
from edit_mode import EditMode
from selectrect import SelectRect
from rect import Rect


class EllipseModeCls(EditMode):

    def __init__(self, outer):
        EditMode.__init__(self)
        self.outer = outer
        self.initEllipse()

    def initEllipse(self):
        self.live_rect = SelectRect()
        self.start_x = 0
        self.start_y = 0
        self.f_move = False
        self.hit_corner = None
        self.top_left_handle = Rect(0,0,0,0)
        self.top_right_handle = Rect(0,0,0,0)
        self.bottom_left_handle = Rect(0,0,0,0)
        self.bottom_right_handle = Rect(0,0,0,0)

    def drawLiveRect(self, qp):
        """
        """
        x1,y1,x2,y2 = self.live_rect.getNormalize()
        #print("x1 : %2d, x2 : %2d" % (x1, x2))
        if x1!=x2 and y1!=y2:
            wx1, wy1 = self.pixToMouseCoord(x1, y1)
            wx2, wy2 = self.pixToMouseCoord(x2,y2)
            qp.fillRect(wx1,wy1,wx2-wx1,wy2-wy1,QtGui.QBrush(QtGui.QColor(0,0,255,25)))

            qp.setCompositionMode(QtGui.QPainter.CompositionMode_Xor)

            # Draw Frame
            pen = QtGui.QPen(QtGui.QColor(50, 50, 200), 1, QtCore.Qt.SolidLine)
            qp.setPen(pen)
            qp.drawLine(wx1, wy1, wx2, wy1)
            qp.drawLine(wx2, wy1, wx2, wy2)
            qp.drawLine(wx2, wy2, wx1, wy2)
            qp.drawLine(wx1, wy2, wx1, wy1)

            # Draw corners handle
            s = int(self.pixSize / 3)
            s = 4 if s<4 else s
            self.top_left_handle = Rect(wx1-s,wy1-s,wx1+s,wy1+s)
            qp.fillRect(self.top_left_handle.left,self.top_left_handle.top,
                        self.top_left_handle.width(),self.top_left_handle.height(),
                        QtGui.QBrush(QtGui.QColor(150,150,200)))            
            self.top_right_handle = Rect(wx2-s,wy1-s,wx2+s,wy1+s)
            qp.fillRect(self.top_right_handle.left,self.top_right_handle.top,
                        self.top_right_handle.width(),self.top_right_handle.height(),
                        QtGui.QBrush(QtGui.QColor(150,150,200)))            
            self.bottom_left_handle = Rect(wx1-s,wy2-s,wx1+s,wy2+s)
            qp.fillRect(self.bottom_left_handle.left,self.bottom_left_handle.top,
                        self.bottom_left_handle.width(),self.bottom_left_handle.height(),
                        QtGui.QBrush(QtGui.QColor(150,150,200)))            
            self.bottom_right_handle = Rect(wx2-s,wy2-s,wx2+s,wy2+s)
            qp.fillRect(self.bottom_right_handle.left,self.bottom_right_handle.top,
                        self.bottom_right_handle.width(),self.bottom_right_handle.height(),
                        QtGui.QBrush(QtGui.QColor(150,150,200)))            
            
    def hitCorner(self,x,y):
        if self.top_left_handle.contains(x,y):
            return self.live_rect.TopLeft
        elif self.top_right_handle.contains(x,y):
            return self.live_rect.TopRight
        elif self.bottom_left_handle.contains(x,y):
            return self.live_rect.BottomLeft
        elif self.bottom_right_handle.contains(x,y):
            return self.live_rect.BottomRight
        else:
            return None

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        mousePos -= QtCore.QPoint(EditMode.origin_x,EditMode.origin_y)
        x, y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        if self.InSprite(x, y):
            if self.live_rect.isEmpty():
                self.backupSprite()
                self.live_rect.setTopLeft(x,y)
                self.live_rect.setBottomRight(x,y)
            else:
                self.hit_corner = self.hitCorner(mousePos.x(),mousePos.y())
                if self.hit_corner is None:
                    if self.live_rect.contains(x,y):
                        self.live_rect.backup()
                        self.start_x = x
                        self.start_y = y
                        self.f_move = True
                    else:
                        self.backupSprite()
                        self.live_rect.setTopLeft(x,y)
                        self.live_rect.setBottomRight(x,y)

            self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        self.hit_corner = None
        self.f_move = False
        self.live_rect.normalize()

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        mousePos -= QtCore.QPoint(EditMode.origin_x,EditMode.origin_y)
        x, y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.InSprite(x, y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:
                if self.f_move:
                    dx = x - self.start_x
                    dy = y - self.start_y
                    #if (dx!=0) or (dy!=0):
                    self.live_rect.restore()
                    self.live_rect.offset(dx,dy)
                elif self.hit_corner is not None:
                    self.hit_corner.x.val = x
                    self.hit_corner.y.val = y
                else:
                    self.live_rect.setBottomRight(x,y)

                self.restoreSprite()
                qp = QtGui.QPainter(self.sprite)
                qp.setPen(self.foregroundColor)
                left,top,right,bottom = self.live_rect.getNormalize()
                qp.drawEllipse(left, top,right-left-1,bottom-top-1)
                qp.end()
                self.outer.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Return or e.key() == QtCore.Qt.Key_Enter:
            #
            self.initEllipse()
            self.outer.repaint()


