# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'new_sprite_dlg.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLayout, QLineEdit,
    QSizePolicy, QVBoxLayout, QWidget)

class Ui_new_sprite_dlg(object):
    def setupUi(self, new_sprite_dlg):
        if not new_sprite_dlg.objectName():
            new_sprite_dlg.setObjectName(u"new_sprite_dlg")
        new_sprite_dlg.setWindowModality(Qt.WindowModality.WindowModal)
        new_sprite_dlg.resize(260, 141)
        font = QFont()
        font.setPointSize(12)
        new_sprite_dlg.setFont(font)
        new_sprite_dlg.setWindowTitle(u"New Sprite")
        new_sprite_dlg.setModal(True)
        self.buttonBox = QDialogButtonBox(new_sprite_dlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 100, 231, 31))
        font1 = QFont()
        font1.setPointSize(10)
        self.buttonBox.setFont(font1)
        self.buttonBox.setFocusPolicy(Qt.FocusPolicy.TabFocus)
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.verticalLayoutWidget = QWidget(new_sprite_dlg)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 20, 241, 71))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout1 = QHBoxLayout()
        self.horizontalLayout1.setSpacing(0)
        self.horizontalLayout1.setObjectName(u"horizontalLayout1")
        self.horizontalLayout1.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.horizontalLayout1.setContentsMargins(-1, 0, -1, -1)
        self.Width = QLabel(self.verticalLayoutWidget)
        self.Width.setObjectName(u"Width")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Width.sizePolicy().hasHeightForWidth())
        self.Width.setSizePolicy(sizePolicy)
        self.Width.setMinimumSize(QSize(130, 0))
        self.Width.setMaximumSize(QSize(120, 27))
        self.Width.setFont(font)
        self.Width.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout1.addWidget(self.Width)

        self.with_val = QLineEdit(self.verticalLayoutWidget)
        self.with_val.setObjectName(u"with_val")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.with_val.sizePolicy().hasHeightForWidth())
        self.with_val.setSizePolicy(sizePolicy1)
        self.with_val.setMinimumSize(QSize(0, 0))
        self.with_val.setMaxLength(6)

        self.horizontalLayout1.addWidget(self.with_val)

        self.horizontalLayout1.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout1)

        self.horizontalLayout2 = QHBoxLayout()
        self.horizontalLayout2.setSpacing(0)
        self.horizontalLayout2.setObjectName(u"horizontalLayout2")
        self.horizontalLayout2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(130, 0))
        self.label.setMaximumSize(QSize(120, 27))
        self.label.setBaseSize(QSize(200, 27))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.horizontalLayout2.addWidget(self.label)

        self.height_val = QLineEdit(self.verticalLayoutWidget)
        self.height_val.setObjectName(u"height_val")
        sizePolicy1.setHeightForWidth(self.height_val.sizePolicy().hasHeightForWidth())
        self.height_val.setSizePolicy(sizePolicy1)
        self.height_val.setMaxLength(6)

        self.horizontalLayout2.addWidget(self.height_val)

        self.horizontalLayout2.setStretch(1, 1)

        self.verticalLayout.addLayout(self.horizontalLayout2)


        self.retranslateUi(new_sprite_dlg)
        self.buttonBox.accepted.connect(new_sprite_dlg.accept)
        self.buttonBox.rejected.connect(new_sprite_dlg.reject)

        QMetaObject.connectSlotsByName(new_sprite_dlg)
    # setupUi

    def retranslateUi(self, new_sprite_dlg):
        self.Width.setText(QCoreApplication.translate("new_sprite_dlg", u"Width", None))
        self.label.setText(QCoreApplication.translate("new_sprite_dlg", u"Height", None))
        pass
    # retranslateUi

