##--------------------------------------------------------------------------
from PySide6 import QtWidgets, QtCore, QtGui
from maya import cmds as mc
import maya.mel as mel
import json
from ..Qt import QtWidgets, QtCore, QtCompat
import os
import maya.cmds as cmds
from maya import OpenMayaUI as omui
import mtoa.core as core
from functools import partial

from shiboken6 import wrapInstance
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget

import importlib
from .. import ModIt_Global

importlib.reload(ModIt_Global)

from .. import ModIt_CSS



##______________________GLOBAL VAR
##PATH_SET
IconPath = ModIt_Global.IconsPathThemeClassic
PreferencePath = ModIt_Global.PreferencePath
ToolsPath = ModIt_Global.ToolPath

# ******************************************
#           BUTTONS PARAMS
# ******************************************
iconFixeSize = 26
iconButtonSize = 26
separatorWidth = ModIt_Global.separatorWidth

##JSON PREF DATA
PRIM_MODE =(json.load(open(PreferencePath + 'Setting_Primitives_Placement.json',"r"))['PRIM_MODE'])
PRIM_SIZE =(json.load(open(PreferencePath + 'Setting_Primitives_Size.json',"r"))['PRIM_SIZE'])


class MyCustomBtn_Widget(QtWidgets.QPushButton):
    def __init__(self):
        super().__init__()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
    def mousePressEvent(self, event):
        super().mousePressEvent(event)
        if event.button() == QtCore.Qt.RightButton:
          # emit the signal, we can grab the pos directly from the event, no need to get cursor position anymore
          self.customContextMenuRequested.emit(event.pos())
          # make a call to mouseRelease event to restore button back to its original state
          self.mouseReleaseEvent(event)




class COLORS_LAYOUT(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        SECTION_COLORS_LAYOUT = QtWidgets.QHBoxLayout()# MAIN
        SECTION_COLORS_LAYOUT.setContentsMargins(10,5,5,10)
        self.setLayout(SECTION_COLORS_LAYOUT)

        ##-------------------------------------------------------------------------------- COLOR : LAMBERT
        self.ColorGreyBtn = MyCustomBtn_Widget()
        self.ColorGreyBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorGreyBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorGreyBtn.setIcon(QtGui.QIcon(IconPath + "ColorLambert.png"))
        self.ColorGreyBtn.clicked.connect(self.lambert1)
        # C O N T E X T   M E N U
        self.ColorGreyBtn.customContextMenuRequested.connect(self.showPopup_Lambert)
        self.popupMenuGrey = QtWidgets.QMenu()
        ColorGreyMenu_Entry_Select = self.popupMenuGrey.addAction("Select")
        ColorGreyMenu_Entry_Select.triggered.connect(self.SelectLambert)
        ColorGreyMenu_Entry_Transparency = self.popupMenuGrey.addAction("Transparency")
        ColorGreyMenu_Entry_Transparency.triggered.connect(self.TransLambert)
        ColorGreyMenu_Entry_Attributes = self.popupMenuGrey.addAction("Attributes")
        ColorGreyMenu_Entry_Attributes.triggered.connect(self.AttributLambert)


        ##-------------------------------------------------------------------------------- COLOR : YELLOW
        self.ColorYellowBtn = MyCustomBtn_Widget()
        self.ColorYellowBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorYellowBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorYellowBtn.setIcon(QtGui.QIcon(IconPath + "ColorYellow.png"))
        self.ColorYellowBtn.clicked.connect(partial(self.ApplyColor, "Yellow", 0.9, 0.6, 0.0))
        # C O N T E X T   M E N U
        self.ColorYellowBtn.customContextMenuRequested.connect(self.showPopup_Yellow)
        self.popupMenuYellow = QtWidgets.QMenu()
        ColorYellowMenu_Entry_Select = self.popupMenuYellow.addAction("Select")
        ColorYellowMenu_Entry_Select.triggered.connect(partial(self.SelectColor, "Yellow"))
        ColorYellowMenu_Entry_Transparency = self.popupMenuYellow.addAction("Transparency")
        ColorYellowMenu_Entry_Transparency.triggered.connect(partial(self.Transparency, "Yellow"))
        ColorYellowMenu_Entry_Attributes = self.popupMenuYellow.addAction("Attributes")
        ColorYellowMenu_Entry_Attributes.triggered.connect(partial(self.AttributColor, "Yellow"))

        ##-------------------------------------------------------------------------------- COLOR : ORANGE
        self.ColorORangeBtn = MyCustomBtn_Widget()
        self.ColorORangeBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorORangeBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorORangeBtn.setIcon(QtGui.QIcon(IconPath + "ColorOrange.png"))
        self.ColorORangeBtn.clicked.connect(partial(self.ApplyColor, "ORange", 0.9, 0.35, 0.0))
        # C O N T E X T   M E N U
        self.ColorORangeBtn.customContextMenuRequested.connect(self.showPopup_ORange)
        self.popupMenuORange = QtWidgets.QMenu()
        ColorORangeMenu_Entry_Select = self.popupMenuORange.addAction("Select")
        ColorORangeMenu_Entry_Select.triggered.connect(partial(self.SelectColor, "ORange"))
        ColorORangeMenu_Entry_Transparency = self.popupMenuORange.addAction("Transparency")
        ColorORangeMenu_Entry_Transparency.triggered.connect(partial(self.Transparency, "ORange"))
        ColorORangeMenu_Entry_Attributes = self.popupMenuORange.addAction("Attributes")
        ColorORangeMenu_Entry_Attributes.triggered.connect(partial(self.AttributColor, "ORange"))

        ##-------------------------------------------------------------------------------- COLOR : RED
        self.ColorRedBtn = MyCustomBtn_Widget()
        self.ColorRedBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorRedBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorRedBtn.setIcon(QtGui.QIcon(IconPath + "ColorRed.png"))
        self.ColorRedBtn.clicked.connect(partial(self.ApplyColor, "Red", 0.7, 0.011, 0.011))
        # C O N T E X T   M E N U
        self.ColorRedBtn.customContextMenuRequested.connect(self.showPopup_Red)
        self.popupMenuRed = QtWidgets.QMenu()
        ColorRedMenu_Entry_Select = self.popupMenuRed.addAction("Select")
        ColorRedMenu_Entry_Select.triggered.connect(partial(self.SelectColor, "Red"))
        ColorRedMenu_Entry_Transparency = self.popupMenuRed.addAction("Transparency")
        ColorRedMenu_Entry_Transparency.triggered.connect(partial(self.Transparency, "Red"))
        ColorRedMenu_Entry_Attributes = self.popupMenuRed.addAction("Attributes")
        ColorRedMenu_Entry_Attributes.triggered.connect(partial(self.AttributColor, "Red"))

        ##-------------------------------------------------------------------------------- COLOR : GREEN
        self.ColorGreenBtn = MyCustomBtn_Widget()
        self.ColorGreenBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorGreenBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorGreenBtn.setIcon(QtGui.QIcon(IconPath + "ColorGreen.png"))
        self.ColorGreenBtn.clicked.connect(partial(self.ApplyColor, "Green", 0.0, 0.798, 0.292))
        # C O N T E X T   M E N U
        self.ColorGreenBtn.customContextMenuRequested.connect(self.showPopup_Green)
        self.popupMenuGreen = QtWidgets.QMenu()
        ColorGreenMenu_Entry_Select = self.popupMenuGreen.addAction("Select")
        ColorGreenMenu_Entry_Select.triggered.connect(partial(self.SelectColor, "Green"))
        ColorGreenMenu_Entry_Transparency = self.popupMenuGreen.addAction("Transparency")
        ColorGreenMenu_Entry_Transparency.triggered.connect(partial(self.Transparency, "Green"))
        ColorGreenMenu_Entry_Attributes = self.popupMenuGreen.addAction("Attributes")
        ColorGreenMenu_Entry_Attributes.triggered.connect(partial(self.AttributColor, "Green"))

        ##-------------------------------------------------------------------------------- COLOR : CYAN
        self.ColorCyanBtn = MyCustomBtn_Widget()
        self.ColorCyanBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorCyanBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorCyanBtn.setIcon(QtGui.QIcon(IconPath + "ColorCyan.png"))
        self.ColorCyanBtn.clicked.connect(partial(self.ApplyColor, "Cyan", 0.0, 0.6684, 0.894))
        # C O N T E X T   M E N U
        self.ColorCyanBtn.customContextMenuRequested.connect(self.showPopup_Cyan)
        self.popupMenuCyan = QtWidgets.QMenu()
        ColorCyanMenu_Entry_Select = self.popupMenuCyan.addAction("Select")
        ColorCyanMenu_Entry_Select.triggered.connect(partial(self.SelectColor, "Cyan"))
        ColorCyanMenu_Entry_Transparency = self.popupMenuCyan.addAction("Transparency")
        ColorCyanMenu_Entry_Transparency.triggered.connect(partial(self.Transparency, "Cyan"))
        ColorCyanMenu_Entry_Attributes = self.popupMenuCyan.addAction("Attributes")
        ColorCyanMenu_Entry_Attributes.triggered.connect(partial(self.AttributColor, "Cyan"))

        ##-------------------------------------------------------------------------------- COLOR : BLUE
        self.ColorBlueBtn = MyCustomBtn_Widget()
        self.ColorBlueBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorBlueBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorBlueBtn.setIcon(QtGui.QIcon(IconPath + "ColorBlue.png"))
        self.ColorBlueBtn.clicked.connect(partial(self.ApplyColor, "Blue", 0, 0.432, 0.7))
        # C O N T E X T   M E N U
        self.ColorBlueBtn.customContextMenuRequested.connect(self.showPopup_Blue)
        self.popupMenuBlue = QtWidgets.QMenu()
        ColorBlueMenu_Entry_Select = self.popupMenuBlue.addAction("Select")
        ColorBlueMenu_Entry_Select.triggered.connect(partial(self.SelectColor, "Blue"))
        ColorBlueMenu_Entry_Transparency = self.popupMenuBlue.addAction("Transparency")
        ColorBlueMenu_Entry_Transparency.triggered.connect(partial(self.Transparency, "Blue"))
        ColorBlueMenu_Entry_Attributes = self.popupMenuBlue.addAction("Attributes")
        ColorBlueMenu_Entry_Attributes.triggered.connect(partial(self.AttributColor, "Blue"))

        ##-------------------------------------------------------------------------------- COLOR : BLACK
        self.ColorBlackBtn = MyCustomBtn_Widget()
        self.ColorBlackBtn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ColorBlackBtn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ColorBlackBtn.setIcon(QtGui.QIcon(IconPath + "ColorBlack.png"))
        self.ColorBlackBtn.clicked.connect(partial(self.ApplyColor, "Black", 0.05, 0.05, 0.05))
        # C O N T E X T   M E N U
        self.ColorBlackBtn.customContextMenuRequested.connect(self.showPopup_Black)
        self.popupMenuBlack = QtWidgets.QMenu()
        ColorBlackMenu_Entry_Select = self.popupMenuBlack.addAction("Select")
        ColorBlackMenu_Entry_Select.triggered.connect(partial(self.SelectColor, "Black"))
        ColorBlackMenu_Entry_Transparency = self.popupMenuBlack.addAction("Transparency")
        ColorBlackMenu_Entry_Transparency.triggered.connect(partial(self.Transparency, "Black"))
        ColorBlackMenu_Entry_Attributes = self.popupMenuBlack.addAction("Attributes")
        ColorBlackMenu_Entry_Attributes.triggered.connect(partial(self.AttributColor, "Black"))



        ##---------------------------------------------------- Add to Layout
        SECTION_COLORS_LAYOUT.addWidget(self.ColorGreyBtn)
        SECTION_COLORS_LAYOUT.addWidget(self.ColorYellowBtn)
        SECTION_COLORS_LAYOUT.addWidget(self.ColorORangeBtn)
        SECTION_COLORS_LAYOUT.addWidget(self.ColorRedBtn)
        SECTION_COLORS_LAYOUT.addWidget(self.ColorGreenBtn)
        SECTION_COLORS_LAYOUT.addWidget(self.ColorCyanBtn)
        SECTION_COLORS_LAYOUT.addWidget(self.ColorBlueBtn)
        SECTION_COLORS_LAYOUT.addWidget(self.ColorBlackBtn)

    #------------------------------------------------
    ##----------------------------------------------------   D E F I N I T I O N

    def ApplyColor(self, color, num1, num2, num3):
        mc.undoInfo(openChunk=True, infinity=True)
        selection = mc.ls(sl=True)
        if mc.objExists("Sel_" + color):
            mc.hyperShade(assign="Sel_" + color)
        else:
            Lambert = mc.shadingNode("lambert", asShader=True)
            mc.setAttr(Lambert + ".color", num1, num2, num3, type='double3')
            mc.rename("Sel_" + color)
            mc.select(selection)
            mc.hyperShade(assign="Sel_" + color)
        mc.undoInfo(closeChunk=True)
    def SelectColor(self, color):
        mc.undoInfo(openChunk=True, infinity=True)
        if mc.objExists("Sel_" + color):
            mc.hyperShade(objects="Sel_" + color)
        else:
            print("Please First Create this FaceColor Shader")
        mc.undoInfo(closeChunk=True)
    def Transparency(self, color):
        if mc.objExists("Sel_" + color):
            mc.window(title= color + ' Transparency')
            mc.columnLayout()
            mc.attrColorSliderGrp(at='Sel_' + color + '.transparency')
            mc.showWindow()
        else:
            print("Please First Create this FaceColor Shader")

    def AttributColor(self, color):
        if mc.objExists('Sel_' + color):
            mc.select('Sel_' + color)
        else:
            print("Please First Create this FaceColor Shader")

    def lambert1(self):
        mc.hyperShade(assign="lambert1")

    def SelectLambert(self):
        if mc.objExists('lambert1'):
            mc.hyperShade(objects="lambert1")
        else:
            print("Please First Create this FaceColor Shader")

    def TransLambert(self):
        if mc.objExists('lambert1'):
            mc.window(title='Lambert Transparancy')
            mc.columnLayout()
            mc.attrColorSliderGrp(at='lambert1.transparency')
            mc.showWindow()
        else:
            print("Please First Create this FaceColor Shader")

    def AttributLambert(self):
        if mc.objExists('lambert1'):
            mc.select('lambert1')
        else:
            print("Please First Create this FaceColor Shader")



    def showPopup_Lambert(self, position):
        self.popupMenuGrey.exec(self.ColorGreyBtn.mapToGlobal(position))
        self.ColorBlackBtn.update()

    def showPopup_Yellow(self, position):
        self.popupMenuYellow.exec(self.ColorYellowBtn.mapToGlobal(position))
        self.ColorYellowBtn.update()

    def showPopup_ORange(self, position):
        self.popupMenuORange.exec(self.ColorORangeBtn.mapToGlobal(position))
        self.ColorORangeBtn.update()

    def showPopup_Red(self, position):
        self.popupMenuRed.exec(self.ColorRedBtn.mapToGlobal(position))
        self.ColorRedBtn.update()

    def showPopup_Green(self, position):
        self.popupMenuGreen.exec(self.ColorGreenBtn.mapToGlobal(position))
        self.ColorGreenBtn.update()

    def showPopup_Cyan(self, position):
        self.popupMenuCyan.exec(self.ColorCyanBtn.mapToGlobal(position))
        self.ColorCyanBtn.update()

    def showPopup_Black(self, position):
        self.popupMenuBlack.exec(self.ColorBlackBtn.mapToGlobal(position))
        self.ColorBlackBtn.update()

    def showPopup_Blue(self, position):
        self.popupMenuBlue.exec(self.ColorBlueBtn.mapToGlobal(position))
        self.ColorBlueBtn.update()

