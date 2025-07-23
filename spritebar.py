#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 24 Nov. 2019

Customn QWidget for sprites 

@author: nguray
'''

from PySide6 import QtGui, QtCore, QtWidgets

class SpriteCell(QtCore.QRect):
    def __init__(self):
        QtCore.QRect.__init__(self)
        self.sprite = None
        self.sc_sprite = None
        self.name = ""


class SpriteBar(QtWidgets.QWidget):
    '''
    Sprites palette
    '''

    spriteChanged = QtCore.Signal()

    list_sprites = []
    nb_cells = 8
    current_sprite = 0
    cell_size = 64

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QWidget.__init__(self, parent)

        for i in range(0, self.nb_cells):
            sc = SpriteCell()
            self.list_sprites.append(sc)
            if (i == 0):
                sc.sprite = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
                sc.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
                sc.sc_sprite = sc.sprite.scaled(QtCore.QSize(self.cell_size-2,self.cell_size-2),
                                                   QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            else:
                sc.sprite = None
                sc.sc_sprite = None

    def mouse2Index(self, mx, my):
        '''
        '''
        for i, s in enumerate(self.list_sprites):
            if s.contains(mx,my):
                return i
        return -1

    def getCurSrpite(self):
        '''
        '''
        return self.list_sprites[self.current_sprite].sprite

    def mousePressEvent(self, mouseEvent):
        '''
        '''
        mousePos = mouseEvent.pos()
        if mouseEvent.buttons() == QtCore.Qt.LeftButton:
            id = self.mouse2Index(mousePos.x(), mousePos.y())
            if id >= 0:
                self.current_sprite = id
                sc = self.list_sprites[id]
                if sc.sprite is None:
                    s = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
                    s.fill(QtGui.qRgba(0, 0, 0, 0))
                    sc.sprite = s
                self.spriteChanged.emit()
                self.repaint()

    def drawSprites(self, qp):
        '''
        '''
        size = self.size()
        w = size.width()
        centerX = w / 2
        for i,s in enumerate(self.list_sprites):
            if i==self.current_sprite: # Update only current sprite
                s.sc_sprite = s.sprite.scaled(QtCore.QSize(self.cell_size-2,self.cell_size-2),
                                                   QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            if s.sc_sprite is not None:
                x = centerX - s.sc_sprite.width() / 2
                y = i * self.cell_size + self.cell_size/2 - s.sc_sprite.height()/2
                qp.drawImage(QtCore.QPoint(int(x), int(y)), s.sc_sprite)

    def loadSprite(self, fileName):
        '''
        '''
        sc = self.list_sprites[self.current_sprite]
        sc.name = fileName
        sc.sprite.load(fileName, "PNG")
        self.spriteChanged.emit()
        self.repaint()

    def createSprite(self, pixWidth: int, pixHeight: int)->None:
        s = QtGui.QImage(pixWidth, pixHeight, QtGui.QImage.Format_ARGB32)
        s.fill(QtGui.qRgba(0, 0, 0, 0))
        sc = self.list_sprites[self.current_sprite]
        sc.sprite = s
        sc.sc_sprite = sc.sc_sprite.scaled(QtCore.QSize(self.cell_size,self.cell_size),
                                            QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        self.spriteChanged.emit()
        self.repaint()

    def saveAsSprite(self, fileName):
        '''
        '''
        sc = self.list_sprites[self.current_sprite]
        sc.name = fileName
        sc.sprite.save(fileName, "PNG")

    def saveSprite(self):
        '''
        '''
        sc = self.list_sprites[self.current_sprite]
        fileName = sc.name
        sc.sprite.save(fileName, "PNG")


    def drawSelectMark(self, qp):
        '''
        '''
        size = self.size()
        self.cell_size = size.width()
        xLeft = 0
        xRight = xLeft + self.cell_size - 1
        pen = QtGui.QPen(QtGui.QColor(20, 20, 255), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        yTop = self.current_sprite * self.cell_size
        yBottom = yTop + self.cell_size
        # -- Top Left
        qp.drawLine(xLeft, yTop, xLeft, yTop+4)
        qp.drawLine(xLeft, yTop, xLeft+4, yTop)
        # -- Bottom Right
        qp.drawLine(xRight, yBottom, xRight, yBottom-4)
        qp.drawLine(xRight, yBottom, xRight-4, yBottom)
        # -- Top Right
        qp.drawLine(xRight, yTop, xRight-4, yTop)
        qp.drawLine(xRight, yTop, xRight, yTop+4)
        # -- Bottom Left
        qp.drawLine(xLeft, yBottom, xLeft, yBottom-4)
        qp.drawLine(xLeft, yBottom, xLeft+4, yBottom)


    def paintEvent(self, e):
        '''
        '''
        qp = QtGui.QPainter()

        qp.begin(self)

        size = self.size()
        self.cell_size = size.width()
        # h = size.height()
        pen = QtGui.QPen(QtGui.QColor(200, 200, 200), 1, QtCore.Qt.SolidLine)
        qp.setPen(pen)
        #qp.drawRect(0, 0, w - 1, (8 * self.cell_size + 4) - 1)

        # Draw cells frames
        xLeft  = 0
        xRight = self.cell_size - 1
        yTop   = 0
        for s in self.list_sprites:
            # Update cells rectangles
            s.setRect(xLeft,yTop,self.cell_size,self.cell_size)
            qp.drawLine(xLeft, yTop, xRight, yTop)
            yTop += self.cell_size
        qp.drawLine(xLeft, yTop, xRight, yTop)
        qp.drawLine(xLeft, 0, xLeft, yTop)
        qp.drawLine(xRight, 0, xRight, yTop)


        self.drawSprites(qp)
        self.drawSelectMark(qp)

        qp.end()
