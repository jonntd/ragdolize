# -*- coding: utf-8 -*-
"""Pyside2 custom widgets

MIT License

Copyright (c) 2020 Mauro Lopez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFT
"""
from PySide2 import QtWidgets
from PySide2 import QtGui
from PySide2 import QtCore
import os
import resources

def labeledWidget(widgetInst, parent=None, label='', pixmap=None, siconSize=40):
    wid = QtWidgets.QWidget(parent)
    lay = QtWidgets.QHBoxLayout(wid)
    lay.setContentsMargins(1, 1, 1, 1)
    label =  QtWidgets.QLabel(label)
    if pixmap is None:
        lay.addWidget(label)
    else:
        lay1 = QtWidgets.QHBoxLayout(wid)
        lay1.setContentsMargins(0, 0, 0, 0)
        lay1.setSpacing(5)
        icon =  QtWidgets.QLabel(label)
        pixmap = QtGui.QPixmap(pixmap);
        pixmap = pixmap.scaled(siconSize, siconSize, QtCore.Qt.KeepAspectRatio) 
        icon.setPixmap(pixmap)
        lay1.addWidget(icon)
        lay1.addWidget(label)
        lay.addLayout(lay1)
    currW = widgetInst(wid)
    lay.addWidget(currW)
    wid.setLayout(lay)
    lay.setStretch(0,0)
    lay.setStretch(1,1)
    lay.setSpacing(15)
    return wid, currW

class QHLine(QtWidgets.QFrame):
    def __init__(self, parent):
        super(QHLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class QVLine(QtWidgets.QFrame):
    def __init__(self, parent):
        super(QVLine, self).__init__(parent)
        self.setFrameShape(QtWidgets.QFrame.VLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)

class QCustomSlider(QtWidgets.QSlider):

    def paintEvent(self, event):
        QtWidgets.QSlider.paintEvent(self, event)
        painter = QtGui.QPainter(self)
        painter.setPen(QtGui.QPen(QtCore.Qt.white))
        rect = self.geometry()
        curr_value = float(self.value()) / self.maximum()
        round_value = round(curr_value, 2)
        font_metrics = QtGui.QFontMetrics(self.font())
        font_height = font_metrics.height()
        horizontal_x_pos = 0
        horizontal_y_pos = rect.height() - font_height-3
        painter.drawText(QtCore.QPoint(horizontal_x_pos, horizontal_y_pos), str(round_value))

        numTicks = (self.maximum() - self.minimum())/self.tickInterval()

        if self.orientation() == QtCore.Qt.Horizontal:
            for i in range(numTicks+1):
                tickX = ((rect.width()/float(numTicks)) * i)
                if tickX >= rect.width():
                    tickX = rect.width()-2
                elif tickX == 0:
                    tickX = 2
                height = 5
                if i==0 or i==numTicks or i==numTicks/2:
                    height = 10
                painter.drawLine(tickX, rect.height(), tickX, rect.height()-height)

class CollapsibleGroup(QtWidgets.QGroupBox):

    def __init__(self, parent, title, iconPath):
        super(CollapsibleGroup, self).__init__(parent)
        mainLay = QtWidgets.QVBoxLayout(self)
        mainLay.setContentsMargins(1, 1, 1, 1)
        titleLay = QtWidgets.QHBoxLayout(self)
        titleLay.setContentsMargins(0, 0, 0, 0)
        self.collapsibleCBx = QtWidgets.QCheckBox()
        self.collapsibleCBx.setChecked(True)
        self.collapsibleCBx.stateChanged.connect(self.diableGroup)
        titleLay.addWidget(self.collapsibleCBx)
        titleWidg, self.title = labeledWidget(QHLine, 
                                            self,
                                            title,
                                            iconPath,
                                            30)
        titleLay.addWidget(titleWidg)
        mainLay.addLayout(titleLay)
        self.centerWidg = QtWidgets.QWidget(self)
        self.centerLay = QtWidgets.QVBoxLayout(self)
        self.centerLay.setContentsMargins(0, 0, 0, 0)
        self.centerLay.setSpacing(0)
        self.centerWidg.setLayout(self.centerLay)
        mainLay.addWidget(self.centerWidg)
        self.setLayout(mainLay)
        st = ""
        stream = QtCore.QFile(':styles/collapsibleGroup.qss')
        if stream.open(QtCore.QFile.ReadOnly):
            st = str(stream.readAll())
            stream.close()
        self.collapsibleCBx.setStyleSheet(st)

        
    def diableGroup(self, value):
        if value:
            self.title.setEnabled(True)
            self.centerWidg.setVisible(True)
        else:
            self.title.setEnabled(False)
            self.centerWidg.setVisible(False)
        self.adjustSize()
        self.window().adjustSize()
        return

    def isChecked(self):
        return self.collapsibleCBx.isChecked()

    def addWidget(self, widget):
        widget.setParent(self.centerWidg)
        self.centerLay.addWidget(widget)

    def setCollapsed(self, value=True):
        self.collapsibleCBx.setChecked(not value)

class VectorSpin(QtWidgets.QWidget):
    def __init__(self, parent, values = [0,0,0]):
        super(VectorSpin, self).__init__(parent)
        mainLay = QtWidgets.QHBoxLayout(self)
        mainLay.setContentsMargins(0, 0, 0, 0)
        frame = QtWidgets.QFrame(self)
        frame.setFrameShape(QtWidgets.QFrame.Box)
        frame.setFrameShadow(QtWidgets.QFrame.Sunken)
        frameLay = QtWidgets.QHBoxLayout(frame)
        frameLay.setContentsMargins(1, 1, 1, 1)
        frame.setLayout(frameLay)
        self.xSpin = QtWidgets.QDoubleSpinBox(frame)
        self.xSpin.setMinimum(-1)
        self.xSpin.setMaximum(1)
        self.xSpin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        frameLay.addWidget(self.xSpin)
        frameLay.addWidget(QVLine(frame))
        self.ySpin = QtWidgets.QDoubleSpinBox(frame)
        self.ySpin.setMinimum(-1)
        self.ySpin.setMaximum(1)
        self.ySpin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        frameLay.addWidget(self.ySpin)
        frameLay.addWidget(QVLine(frame))
        self.zSpin = QtWidgets.QDoubleSpinBox(frame)
        self.zSpin.setMinimum(-1)
        self.zSpin.setMaximum(1)
        self.zSpin.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        frameLay.addWidget(self.zSpin)
        mainLay.addWidget(frame)
        
        self.setLayout(mainLay)
        self.setValue(*values)


    @property
    def x(self):
        return self.xSpin.value()

    @property
    def y(self):
        return self.ySpin.value()

    @property
    def z(self):
        return self.zSpin.value()

    @x.setter
    def x(self, val):
        self.xSpin.setValue(val)
    
    @y.setter
    def y(self, val):
        self.zSpin.setValue(val)

    @z.setter
    def z(self, val):
        self.zSpin.setValue(val)

    def setValue(self, x,y,z):
        self.xSpin.setValue(x)
        self.ySpin.setValue(y)
        self.zSpin.setValue(z)

    def value(self):
        return [self.xSpin.value(), self.ySpin.value(), self.zSpin.value()]

