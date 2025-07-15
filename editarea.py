#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Created on 30 Juin 2025

Customn QWidget for drawing canvas

@author: nguray
'''
import os
from PySide6 import QtGui, QtCore, QtWidgets
from collections import namedtuple

from edit_mode import EditMode
from pencil_mode import PencilModeCls
from rectangle_mode import RectangleModeCls
from select_mode import SelectModeCls
from fill_mode import FillModeCls
from ellipse_mode import EllipseModeCls

from rect import Rect

class MyEditArea(QtWidgets.QWidget):
    '''
    classdocs
    '''

    cursorPosChanged = QtCore.Signal(int, int)
    pipetForeColor = QtCore.Signal(QtGui.QColor)
    pipetBackColor = QtCore.Signal(QtGui.QColor)
    fileNameChanged = QtCore.Signal(str)

    EditeModes = namedtuple('EditModes', [
        'Select', 'Pencil', 'Rubber', 'DrawLine', 'DrawRectangle',
        'DrawEllipse', 'Fill'
    ])
    EDIT = EditeModes(0, 1, 2, 3, 4, 5, 6)

    x = -1
    y = -1

    edit_mode = 0
    prev_edit_mode = 0

    current_edit_mode = None
    canvasScale = 1.0

    start_x = 0
    start_y = 0
    start_origin_x = 0
    start_origin_y = 0 

    def __init__(self, parent=None):
        '''
        Constructor
        '''
        QtWidgets.QWidget.__init__(self, parent)

        self.myPickColorCursor = QtGui.QCursor(QtGui.QPixmap(":res/PickColor.png"),6,23)
        # ----------------------------------------------------------------------
        myCursorSelect = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorSelect.png", "PNG"), 0, 0)
        myCursorPencil = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorPencil.png", "PNG"), 12, 19)
        myCursorRubber = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorRubber1.png", "PNG"), 12, 19)
        myCursorLine = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorLine.png", "PNG"), 12, 19)
        myCursorRectangle = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorRectangle.png", "PNG"), 12, 19)
        myCursorEllipse = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorEllipse.png", "PNG"), 12, 19)
        myCursorFill = QtGui.QCursor(
            QtGui.QPixmap("cursors/CursorFill.png", "PNG"), 7, 21)
        self.editCursors = [
            myCursorSelect, myCursorPencil, myCursorRubber,
            myCursorLine, myCursorRectangle, myCursorEllipse, myCursorFill
        ]

        self.init32Sprite()

        selectRectModeAction = QtGui.QAction(QtGui.QIcon('SelectRect.png'), 'Select',
                                       self)
        selectRectModeAction.setStatusTip('Select Tool')
        pencilModeAction = QtGui.QAction(QtGui.QIcon('Pencil.png'), 'Pencil', self)
        pencilModeAction.setStatusTip('Pencil Tool')

        rectangleModeAction = QtGui.QAction(QtGui.QIcon('DrawRectangle.png'),
                                      'Draw Rectangle', self)
        rectangleModeAction.setStatusTip('Draw Rectangle Tool')
        ellipseModeAction = QtGui.QAction(QtGui.QIcon('DrawEllipse.png'),
                                    'Draw Ellipse', self)
        ellipseModeAction.setStatusTip('Draw Ellipse Tool')
        fillerModeAction = QtGui.QAction(QtGui.QIcon('Filler.png'), 'Fill', self)
        fillerModeAction.setStatusTip('Fill Tool')

        self.editActions = [
            selectRectModeAction, pencilModeAction,
            rectangleModeAction,
            ellipseModeAction, fillerModeAction
        ]

        # -- Instancier les objects des classes
        self.pencil_mode_obj = PencilModeCls(self)
        self.rectangle_mode_obj = RectangleModeCls(self)
        self.select_mode_obj = SelectModeCls(self)
        self.fill_mode_obj = FillModeCls(self)
        self.ellipse_mode_obj = EllipseModeCls(self)

        self.current_edit_mode = self.pencil_mode_obj

        self.show()
        self.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.setAcceptDrops(True)


    def init32Sprite(self):
        EditMode.pixSize = 12
        EditMode.nbRowPix = 32
        EditMode.nbColumnPix = 32
        EditMode.sprite = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
        EditMode.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        EditMode.sprite_bak = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)
        EditMode.sprite_cpy = QtGui.QImage(32, 32, QtGui.QImage.Format_ARGB32)

    def init16Sprite(self):
        EditMode.pixSize = 24
        EditMode.nbRowPix = 16
        EditMode.nbColumnPix = 16
        EditMode.sprite = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)
        EditMode.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        EditMode.sprite_bak = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)
        EditMode.sprite_cpy = QtGui.QImage(16, 16, QtGui.QImage.Format_ARGB32)

    def init64Sprite(self):
        EditMode.pixSize = 8
        EditMode.nbRowPix = 64
        EditMode.nbColumnPix = 64
        EditMode.sprite = QtGui.QImage(64, 64, QtGui.QImage.Format_ARGB32)
        EditMode.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
        EditMode.sprite_bak = QtGui.QImage(64, 64, QtGui.QImage.Format_ARGB32)
        EditMode.sprite_cpy = QtGui.QImage(64, 64, QtGui.QImage.Format_ARGB32)

    def contextMenuEvent(self, event):
        """
        """
        pass
        # menu = QMenu(self)

        # for a in self.editActions:
        #     menu.addAction(a)

        # # Afficher le context menu
        # action = menu.exec_(self.mapToGlobal(event.pos()))

        # # Traiter le choix de l'utilisateur
        # for m, a in enumerate(self.editActions):
        #     if a == action:
        #         self.setEditMode(m)

    def resetSelect(self):
        """
            Réinitialser les sélections
        """
        self.select_mode_obj.initPasteRect()
        self.select_mode_obj.initSelectRect()
        self.rectangle_mode_obj.initRectangle()
        self.ellipse_mode_obj.initEllipse()

    def setEditMode(self, m):
        """
        """
        if self.edit_mode != m:
            self.prev_edit_mode = self.edit_mode
            self.edit_mode = m
            self.resetSelect()
            # Changer la forme du curseur de la souris
            #self.setCursor(self.editCursors[self.edit_mode])

            if (self.edit_mode == self.EDIT.Select):  # Select Rectangle Mode
                self.current_edit_mode = self.select_mode_obj

            elif (self.edit_mode == self.EDIT.Pencil):  # Pencil Mode
                self.current_edit_mode = self.pencil_mode_obj

            elif (self.edit_mode == self.EDIT.DrawRectangle
                  ):  # Draw rectangle Mode
                self.current_edit_mode = self.rectangle_mode_obj

            elif (self.edit_mode == self.EDIT.DrawEllipse
                  ):  # Draw ellipse Mode
                self.current_edit_mode = self.ellipse_mode_obj

            elif (self.edit_mode == self.EDIT.Fill):  # Fill Mode
                self.current_edit_mode = self.fill_mode_obj
            # --
            self.repaint()

    def changeForeColor(self, c):
        EditMode.foregroundColor = c

    def changeBackColor(self, c):
        EditMode.backgroundColor = c

    def computeSize(self):
        w = EditMode.nbColumnPix * EditMode.pixSize + 1
        h = EditMode.nbRowPix * EditMode.pixSize + 1
        return w, h

    def drawGrid(self, qp):
        '''
        '''
        col = QtGui.QColor(50, 50, 50)
        qp.setPen(col)
        for iy in range(0, EditMode.nbRowPix + 1):
            y = iy * EditMode.pixSize
            for ix in range(0, EditMode.nbColumnPix + 1):
                x = ix * EditMode.pixSize
                qp.drawPoint(x, y)

    def drawSpritePixels(self, qp):
        color = QtGui.QColor()
        for y in range(0, EditMode.nbRowPix):
            py = y * EditMode.pixSize + 1
            for x in range(0, EditMode.nbColumnPix):
                px = x * EditMode.pixSize + 1
                icol = EditMode.sprite.pixel(x, y)
                color.setRgba(icol)
                qp.setPen(color)
                qp.setBrush(color)
                qp.drawRect(px, py, EditMode.pixSize - 2, EditMode.pixSize - 2)

    def doUndo(self):
        self.select_mode_obj.restoreSprite()
        self.select_mode_obj.initPasteRect()
        self.select_mode_obj.initSelectRect()
        self.initDrawRect()
        self.initDrawEllipse()

    def doCutRect(self):
        self.select_mode_obj.cutRect()

    def doCopyRect(self):
        self.select_mode_obj.copyRect()

    def doPasteRect(self):
        self.select_mode_obj.pasteRect()

    def mousePressEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        mousePos -= QtCore.QPoint(EditMode.origin_x,EditMode.origin_y)
        self.x, self.y = EditMode.mouseToPixCoord(mousePos.x(), mousePos.y())
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if mouseEvent.buttons() == QtCore.Qt.LeftButton and modifiers & QtCore.Qt.ShiftModifier:
            if EditMode.InSprite(self.x, self.y):
                c = EditMode.sprite.pixel(self.x, self.y)
                EditMode.foregroundColor.setRgba(c)
                EditMode.pipetForeColor.emit(EditMode.foregroundColor)
        elif mouseEvent.buttons() == QtCore.Qt.MiddleButton:
            self.start_x = mousePos.x()
            self.start_y = mousePos.y()
            self.start_origin_x = EditMode.origin_x
            self.start_origin_y = EditMode.origin_y

        else:
            # --
            self.current_edit_mode.mousePressEvent(mouseEvent)
            self.cursorPosChanged.emit(self.x, self.y)

    def mouseReleaseEvent(self, mouseEvent):
        self.current_edit_mode.mouseReleaseEvent(mouseEvent)

    def mouseMoveEvent(self, mouseEvent):
        mousePos = mouseEvent.pos()
        self.x, self.y = EditMode.mouseToPixCoord(mousePos.x(), mousePos.y())
        # modifiers = QApplication.keyboardModifiers()

        if mouseEvent.buttons() == QtCore.Qt.MiddleButton:
            dx = mousePos.x() - self.start_x 
            dy = mousePos.y() - self.start_y 
            if dx!=0 or dy!=0:
                EditMode.origin_x = self.start_origin_x + dx
                EditMode.origin_y = self.start_origin_y + dy
                self.repaint()
            #print('dx={} dy={}'.format(dx,dy))
        else:
            self.current_edit_mode.mouseMoveEvent(mouseEvent)
            self.cursorPosChanged.emit(self.x, self.y)

    def doMirrorHorizontal(self):
        #
        self.select_mode_obj.initPasteRect()
        self.select_mode_obj.initSelectRect()
        self.rectangle_mode_obj.initRectangle()
        self.ellipse_mode_obj.initEllipse()
        self.current_edit_mode.backupSprite()
        #
        h = int(EditMode.nbColumnPix / 2)
        w = EditMode.nbColumnPix - 1
        for y in range(0, EditMode.nbRowPix):
            for i in range(0, h):
                c0 = EditMode.sprite.pixel(i, y)
                c1 = EditMode.sprite.pixel(w - i, y)
                EditMode.sprite.setPixel(i, y, c1)
                EditMode.sprite.setPixel(w - i, y, c0)
        #
        self.repaint()

    def doMirrorVertical(self):
        #
        self.select_mode_obj.initPasteRect()
        self.select_mode_obj.initSelectRect()
        self.rectangle_mode_obj.initRectangle()
        self.ellipse_mode_obj.initEllipse()
        self.current_edit_mode.backupSprite()
        #
        h = int(EditMode.nbRowPix / 2)
        w = EditMode.nbRowPix - 1
        for x in range(0, EditMode.nbColumnPix):
            for i in range(0, h):
                c0 = EditMode.sprite.pixel(x, i)
                c1 = EditMode.sprite.pixel(x, w - i)
                EditMode.sprite.setPixel(x, i, c1)
                EditMode.sprite.setPixel(x, w - i, c0)
        #
        self.repaint()

    def doRotate90Clock(self):
        #
        self.select_mode_obj.initPasteRect()
        self.select_mode_obj.initSelectRect()
        self.rectangle_mode_obj.initRectangle()
        self.ellipse_mode_obj.initEllipse()
        self.current_edit_mode.backupSprite()
        #
        for y in range(0, EditMode.nbColumnPix):
            for x in range(0, EditMode.nbRowPix):
                c = EditMode.sprite_bak.pixel(x, y)
                EditMode.sprite.setPixel(EditMode.nbColumnPix - y - 1, x, c)

        #
        self.repaint()

    def doRotate90AntiClock(self):
        #
        self.select_mode_obj.initPasteRect()
        self.select_mode_obj.initSelectRect()
        self.rectangle_mode_obj.initRectangle()
        self.ellipse_mode_obj.initEllipse()
        self.current_edit_mode.backupSprite()
        #
        for y in range(0, EditMode.nbColumnPix):
            for x in range(0, EditMode.nbRowPix):
                c = EditMode.sprite_bak.pixel(x, y)
                EditMode.sprite.setPixel(y, EditMode.nbRowPix - x - 1, c)

        #
        self.repaint()

    def setEditSprite(self, sprite: QtGui.QImage):
        EditMode.nbColumnPix = sprite.width()
        EditMode.nbRowPix = sprite.height()
        EditMode.sprite_bak = QtGui.QImage(EditMode.nbColumnPix, EditMode.nbRowPix, QtGui.QImage.Format_ARGB32)
        EditMode.sprite_cpy = QtGui.QImage(EditMode.nbColumnPix, EditMode.nbRowPix, QtGui.QImage.Format_ARGB32)
        EditMode.sprite = sprite
        self.repaint()

    def keyPressEvent(self, e):
        if e.key() == QtCore.Qt.Key_Space:
            self.setEditMode(self.prev_edit_mode)
        elif e.key()==QtCore.Qt.Key_Shift:
            self.setCursor(self.myPickColorCursor)
        else:
            self.current_edit_mode.keyPressEvent(e)

    def keyReleaseEvent(self,e):
        if e.key()==QtCore.Qt.Key_Shift:
            self.setCursor(QtCore.Qt.ArrowCursor)

    def paintEvent(self, e):

        qp = QtGui.QPainter()
        
        qp.begin(self)
    
        qp.translate(QtCore.QPoint(EditMode.origin_x,EditMode.origin_y))

        size = self.size()
        w = size.width()
        h = size.height()
        #print('w = {}    h = {}'.format(w,h))

        # Compute pixels size for display
        o1 = (w-4) / EditMode.nbColumnPix
        o2 = (h-4) / EditMode.nbRowPix
        if o1<o2:
            EditMode.pixSize = int(o1 * self.canvasScale)
        else:
            EditMode.pixSize = int(o2 * self.canvasScale)

        self.drawGrid(qp)

        #
        self.drawSpritePixels(qp)

        self.pencil_mode_obj.drawPolygon(qp)

        # Draw Select rectangle
        if not self.select_mode_obj.select_rect.isEmpty():
            self.select_mode_obj.drawSelectRect(qp)

        if not self.select_mode_obj.paste_rect.isEmpty():
            self.select_mode_obj.drawPasteRect(qp)

        if not self.rectangle_mode_obj.live_rect.isEmpty():
            self.rectangle_mode_obj.drawLiveRect(qp)

        if not self.ellipse_mode_obj.live_rect.isEmpty():
            self.ellipse_mode_obj.drawLiveRect(qp)

        qp.end()

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                path = url.path()
                if path[0] == '/':
                    path = path[1:]
                if os.path.isfile(path):
                    print(path)
                    if (path.upper().endswith(".PNG")):
                        self.sprite.fill(QtGui.qRgba(0, 0, 0, 0))
                        img = QtGui.QImage()
                        img.load(path, "PNG")
                        qp = QtGui.QPainter()
                        qp.begin(self.sprite)
                        wSrc = img.width()
                        hSrc = img.height()
                        if (wSrc <= 32):
                            wDes = wSrc
                        else:
                            wDes = 32
                        if (hSrc < 32):
                            hDes = hSrc
                        else:
                            hDes = 32
                        qp.drawImage(QtCore.QRect(0, 0, wDes, hDes), img,
                                     QtCore.QRect(0, 0, wSrc, hSrc))
                        qp.end()
                        self.repaint()
                        self.fileNameChanged.emit(path)

    def wheelEvent(self, event):
        qp= event.angleDelta()/8
        if qp.y()>0:
            if self.canvasScale<5.0:
                self.canvasScale += 0.05
        elif qp.y()<0:
            if self.canvasScale>0.5:
                self.canvasScale -= 0.05
        self.repaint()
