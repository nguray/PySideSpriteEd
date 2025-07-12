from PySide6 import QtGui, QtCore, QtWidgets

class EditMode:

    sprite = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
    sprite_bak = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
    sprite_cpy = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
    pixSize = 12
    nbRowPix = 32
    nbColumnPix = 32
    foregroundColor = QtGui.QColor(0, 0, 255, 255)
    backgroundColor = QtGui.QColor(0, 0, 0, 0)
    origin_x = 0
    origin_y = 0

    def __init__(self):
        pass


    def backupSprite(self):
        self.sprite_bak.fill(QtGui.qRgba(0, 0, 0, 0))
        qp = QtGui.QPainter()
        qp.begin(self.sprite_bak)
        qp.drawImage(QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix),
                     self.sprite,
                     QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix))
        qp.end()

    def restoreSprite(self):
        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        qp = QtGui.QPainter()
        qp.begin(self.sprite)
        qp.drawImage(QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix),
                     self.sprite_bak,
                     QtCore.QRect(0, 0, self.nbColumnPix, self.nbColumnPix))
        qp.end()

    @classmethod
    def mouseToPixCoord(self, mx, my):
        x = int(mx / self.pixSize)
        y = int(my / self.pixSize)
        return x, y

    @classmethod
    def pixToMouseCoord(self, px, py):
        mx = px * self.pixSize
        my = py * self.pixSize
        return mx, my

    @classmethod
    def InSprite(self, x, y):
        if ((x >= 0) and (x < self.nbColumnPix) and (y >= 0)
                and (y < self.nbRowPix)):
            return True
        else:
            return False

    def floodFill(self, x0, y0, iTargetColor, iNewColor):
        """
        """
        c = self.sprite.pixel(x0, y0)
        if c == iNewColor or c != iTargetColor:
            return
        self.sprite.setPixel(x0, y0, iNewColor)
        if (y0 > 0):
            self.floodFill(x0, y0 - 1, iTargetColor, iNewColor)
        if (y0 < self.nbColumnPix - 1):
            self.floodFill(x0, y0 + 1, iTargetColor, iNewColor)
        if x0 < self.nbColumnPix - 1:
            self.floodFill(x0 + 1, y0, iTargetColor, iNewColor)
        if x0 > 0:
            self.floodFill(x0 - 1, y0, iTargetColor, iNewColor)
