
import copy

from PySide6 import QtGui, QtCore, QtWidgets
from edit_mode import EditMode
from rect import Rect
from selectcorner import SelectCorner
from selectrect import SelectRect

class SelectModeCls(EditMode):

    def __init__(self, outer):
        EditMode.__init__(self)
        self.outer = outer
        self.initPasteRect()
        self.initSelectRect()
        # self.select_rect.setTopLeft(10,20)
        # x, y = self.select_rect.getBottomLeft()
        # pass

    def initSelectRect(self):
        self.cpy_width = 0
        self.cpy_height = 0
        self.select_rect = SelectRect()
        self.hit_corner = None
        self.start_x = 0
        self.start_y = 0
        self.f_move = False
        self.top_left_handle = Rect(0,0,0,0)
        self.top_right_handle = Rect(0,0,0,0)
        self.bottom_left_handle = Rect(0,0,0,0)
        self.bottom_right_handle = Rect(0,0,0,0)

    def initPasteRect(self):
        self.paste_rect = Rect(-1,-1,-1,-1)
        self.hit_paste = False
        self.hit_paste_x = -1
        self.hit_paste_y = -1
        self.hit_paste_rect = Rect(0, 0, 0, 0)

    def drawPasteRect(self, qp):
        pen = QtGui.QPen(QtGui.QColor(50, 50, 200), 2, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        x1, y1 = self.pixToMouseCoord(self.paste_rect.left,
                                            self.paste_rect.top)
        x2, y2 = self.pixToMouseCoord(self.paste_rect.right+1,
                                            self.paste_rect.bottom+1)
        qp.drawLine(x1, y1, x2, y1)
        qp.drawLine(x2, y1, x2, y2)
        qp.drawLine(x2, y2, x1, y2)
        qp.drawLine(x1, y2, x1, y1)

    def drawSelectRect(self, qp):
        """
        """
        x1,y1,x2,y2 = self.select_rect.getNormalize()
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
            return self.select_rect.TopLeft
        elif self.top_right_handle.contains(x,y):
            return self.select_rect.TopRight
        elif self.bottom_left_handle.contains(x,y):
            return self.select_rect.BottomLeft
        elif self.bottom_right_handle.contains(x,y):
            return self.select_rect.BottomRight
        else:
            return None

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()
        if self.InSprite(x, y):
            if mouseEvent.buttons() == QtCore.Qt.LeftButton:

                self.hit_paste = False
                if not self.paste_rect.isEmpty():
                    if self.paste_rect.contains(x,y):
                        self.hit_paste = True
                        self.hit_paste_x = x
                        self.hit_paste_y = y
                        self.hit_paste_rect = copy.copy(self.paste_rect)
                    else:
                        self.initPasteRect()

                if not self.hit_paste:
                    if self.select_rect.isEmpty():
                        self.select_rect.setTopLeft(x,y)
                        self.select_rect.setBottomRight(x,y)
                    else:
                        self.hit_corner = self.hitCorner(mousePos.x(), mousePos.y())
                        if self.hit_corner is None:
                            if self.select_rect.contains(x,y):
                                self.select_rect.backup()
                                self.start_x = x
                                self.start_y = y
                                self.f_move = True
                            else:
                                self.select_rect.setTopLeft(x,y)
                                self.select_rect.setBottomRight(x,y)


                self.outer.repaint()

    def mouseReleaseEvent(self, mouseEvent):
        self.hit_corner = None
        self.f_move = False
        self.select_rect.normalize()

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        x, y = self.mouseToPixCoord(mousePos.x(), mousePos.y())
        #modifiers = QtWidgets.QApplication.keyboardModifiers()
        if self.InSprite(x, y):

            if self.hit_paste:
                if (x != self.hit_paste_x) or (y != self.hit_paste_y):
                    dx = x - self.hit_paste_x
                    dy = y - self.hit_paste_y
                    self.restoreSprite()
                    self.paste_rect = copy.copy(self.hit_paste_rect)
                    self.paste_rect.left += dx
                    self.paste_rect.top += dy
                    self.paste_rect.right += dx
                    self.paste_rect.bottom += dy
                    qp = QtGui.QPainter()
                    qp.begin(self.sprite)
                    w = self.cpy_width
                    h = self.cpy_height
                    qp.drawImage(
                        QtCore.QRect(self.paste_rect.left, self.paste_rect.top,
                                    w, h), self.sprite_cpy,
                        QtCore.QRect(0, 0, w, h))
                    qp.end()
            else:
                if self.f_move:
                    dx = x - self.start_x
                    dy = y - self.start_y
                    #if (dx!=0) or (dy!=0):
                    self.select_rect.restore()
                    self.select_rect.offset(dx,dy)
                elif self.hit_corner is not None:
                    self.hit_corner.x.val = x
                    self.hit_corner.y.val = y
                else:
                    self.select_rect.setBottomRight(x,y)

            self.outer.repaint()

    def keyPressEvent(self, e):
        pass

    def copyRect(self):
        if not self.select_rect.isEmpty():
            self.sprite_cpy.fill(QtGui.qRgba(0, 0, 0, 0))
            qp = QtGui.QPainter()
            qp.begin(self.sprite_cpy)
            self.cpy_width = self.select_rect.width()
            self.cpy_height = self.select_rect.height()
            w = self.cpy_width
            h = self.cpy_height
            qp.drawImage(
                QtCore.QRect(0, 0, w, h), EditMode.sprite,
                QtCore.QRect(self.select_rect.left,
                             self.select_rect.top, w, h))
            qp.end()
            self.initSelectRect()

    def pasteRect(self):
        if self.cpy_width and self.cpy_height:
            self.backupSprite()
            self.paste_rect.left = 0
            self.paste_rect.top = 0
            self.paste_rect.right = self.cpy_width-1
            self.paste_rect.bottom = self.cpy_height-1
            qp = QtGui.QPainter()
            qp.begin(self.sprite)
            w = self.cpy_width
            h = self.cpy_height
            qp.drawImage(QtCore.QRect(0, 0, w, h), self.sprite_cpy,
                         QtCore.QRect(0, 0, w, h))
            qp.end()

    def cutRect(self):
        if not self.select_rect.isEmpty():
            self.sprite_cpy.fill(QtGui.qRgba(0, 0, 0, 0))
            qp = QtGui.QPainter()
            # Faire une copie de zone
            qp.begin(self.sprite_cpy)
            self.cpy_width = self.select_rect.width()
            self.cpy_height = self.select_rect.height()
            w = self.cpy_width
            h = self.cpy_height
            qp.drawImage(
                QtCore.QRect(0, 0, w, h), EditMode.sprite,
                QtCore.QRect(self.select_rect.left,
                             self.select_rect.top, w, h))
            qp.end()
            # Effacer la zone
            qp1 = QtGui.QPainter()
            qp1.begin(EditMode.sprite)
            r, g, b, a = EditMode.backgroundColor.getRgb()
            qp1.setCompositionMode(QtGui.QPainter.CompositionMode_Source)
            qp1.fillRect(
                QtCore.QRect(self.select_rect.left,
                             self.select_rect.top, w, h),
                QtGui.QColor(r, g, b, a))
            qp1.end()
            self.initSelectRect()
