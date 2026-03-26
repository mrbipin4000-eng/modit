##--------------------------------------------------------------------------
## ScriptName : ModIt 3.0
## Author     : Wizix
## StartDate : 2022/09/09
## LastUpdate : 2022/13/09
## Version    : 0.0.1
##-------------------------------------------------------------------------- I M P O R T
from PySide6 import QtWidgets, QtCore, QtGui
from maya import cmds as mc
import maya.mel as mel
import json
from ..Qt import QtWidgets, QtCore, QtCompat
import os
from maya import OpenMayaUI as omui
from functools import partial
from shiboken6 import wrapInstance
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget
##---------------------------------------- Import Modules
import importlib
from .. import ModIt_Global
importlib.reload(ModIt_Global)
from .. import ModIt_CSS
importlib.reload(ModIt_CSS)
##---------------------------------------- Import Classes


##-------------------------------------------------------------------------- G L O B A L   V A R
##PATH_SET
IconPath = ModIt_Global.IconsPathThemeClassic
PreferencePath = ModIt_Global.PreferencePath
ToolsPath = ModIt_Global.ToolPath

WindowsTitle = "Radial Duplication"


Num = ""


##UI INFO
# ________________//
# ___________________________________________
# ________________//
def SEND_INFO(NumVersion):
    global Num
    Num = NumVersion

    return Num


class Radial_UI(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(Radial_UI, self).__init__()
        self.setMinimumSize(460, 230)
        self.buildUI()



    def buildUI(self):
        ##UI - Preferences
        iconFixeSize = 22
        iconButtonSize = 20

        # ________________//
        # ___________________________________________## UI
        # ________________//
        LINEAR_MLyt = QtWidgets.QVBoxLayout(self)
        self.setStyleSheet(ModIt_Global.Theme)


        Title = QtWidgets.QLabel(" -  R a d i a l   D u p l i c a t i o n  -  ")
        Title.setAlignment(QtCore.Qt.AlignCenter)
        LINEAR_MLyt.addWidget(Title)
        LINEAR_MLyt.addSpacing(10)

        Linear_HLyt = QtWidgets.QHBoxLayout()
        LINEAR_MLyt.addLayout(Linear_HLyt)


        # ___________________________________________## LOCATOR ORIGN
        self.LocatorOrign_btn = QtWidgets.QPushButton()
        self.LocatorOrign_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.LocatorOrign_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.LocatorOrign_btn.setIcon(QtGui.QIcon(IconPath + "Locator_orign.png"))
        self.LocatorOrign_btn.setToolTip("  Get Origin Locator  ")
        self.LocatorOrign_btn.clicked.connect(self.get_locatorOrign)
        Linear_HLyt.addWidget(self.LocatorOrign_btn)

        # ___________________________________________## NUMBER OF INSTANCES
        # ___________________________________________##
        SliderNumber_HLyt = QtWidgets.QHBoxLayout(self)
        Linear_HLyt.addLayout(SliderNumber_HLyt)


        Number_label = QtWidgets.QLabel(" Number ")
        SliderNumber_HLyt.addWidget(Number_label)

        self.Number_Slider = QtWidgets.QSlider()
        self.Number_Slider.setMinimum(1)
        self.Number_Slider.setMaximum(100)
        try:
            getValue = mc.getAttr("ModIt_Duplicate_Radial" + str(Num) + "_Distribute.pointCount")
        except:
            getValue = 10
        self.Number_Slider.setProperty("value", getValue)
        self.Number_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.Number_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.Number_Slider.setTickInterval(1)
        self.Number_Slider.setFixedHeight(22)
        self.Number_Slider.valueChanged.connect(self.SliderNumber_Action)
        SliderNumber_HLyt.addWidget(self.Number_Slider)


        self.Number_SpinBox = QtWidgets.QDoubleSpinBox()
        self.Number_SpinBox.setDecimals(1)
        self.Number_SpinBox.setFixedWidth(40)
        self.Number_SpinBox.setFixedHeight(18)
        self.Number_SpinBox.setRange(0, 1000)
        self.Number_SpinBox.setValue(getValue)
        self.Number_SpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.Number_SpinBox.editingFinished.connect(self.SpinBoxA_Action)
        SliderNumber_HLyt.addWidget(self.Number_SpinBox)

        # ___________________________________________## LOCATOR CIBLE
        self.LocatorTarget_btn = QtWidgets.QPushButton()
        self.LocatorTarget_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.LocatorTarget_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.LocatorTarget_btn.setIcon(QtGui.QIcon(IconPath + "Locator_cible.png"))
        self.LocatorTarget_btn.setToolTip("  Get Target Locator  ")
        self.LocatorTarget_btn.clicked.connect(self.get_locatorTarget)
        Linear_HLyt.addWidget(self.LocatorTarget_btn)






        LINEAR_MLyt.addSpacing(4)
        self.Separator = QtWidgets.QLabel()
        self.Separator.setFixedSize(5000,1)
        self.Separator.setStyleSheet("background-color:#434343;")
        LINEAR_MLyt.addWidget(self.Separator)
        LINEAR_MLyt.addSpacing(4)
















        TitleR = QtWidgets.QLabel(" -  R a n d o m  -  ")
        TitleR.setAlignment(QtCore.Qt.AlignCenter)
        LINEAR_MLyt.addWidget(TitleR)
        LINEAR_MLyt.addSpacing(10)
        # ___________________________________________## RANDOM POSITION
        # ___________________________________________##
        SliderRandomP_HLyt = QtWidgets.QHBoxLayout(self)
        LINEAR_MLyt.addLayout(SliderRandomP_HLyt)

        Random_label = QtWidgets.QLabel("Position  ")
        SliderRandomP_HLyt.addWidget(Random_label)

        try:
            getValueP = mc.getAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.positionX")
        except:
            getValueP = 0
        self.RandomP_Slider = QtWidgets.QSlider()
        self.RandomP_Slider.setMinimum(0)
        self.RandomP_Slider.setMaximum(100)
        self.RandomP_Slider.setProperty("value", getValueP)
        self.RandomP_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.RandomP_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.RandomP_Slider.setTickInterval(1)
        self.RandomP_Slider.setFixedHeight(22)
        self.RandomP_Slider.valueChanged.connect(self.SliderPosRandom_Action)
        SliderRandomP_HLyt.addWidget(self.RandomP_Slider)


        self.RandomP_SpinBox = QtWidgets.QDoubleSpinBox()
        self.RandomP_SpinBox.setDecimals(1)
        self.RandomP_SpinBox.setFixedWidth(40)
        self.RandomP_SpinBox.setFixedHeight(18)
        self.RandomP_SpinBox.setRange(0, 1000)
        self.RandomP_SpinBox.setValue(getValueP)
        self.RandomP_SpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.RandomP_SpinBox.editingFinished.connect(self.SpinPosRandom_Action)
        SliderRandomP_HLyt.addWidget(self.RandomP_SpinBox)



        # ___________________________________________## RANDOM ROTATION
        # ___________________________________________##
        SliderRandomR_HLyt = QtWidgets.QHBoxLayout(self)
        LINEAR_MLyt.addLayout(SliderRandomR_HLyt)

        Random_label = QtWidgets.QLabel("Rotation ")
        SliderRandomR_HLyt.addWidget(Random_label)

        try:
            getValueR = mc.getAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.rotationX")
        except:
            getValueR = 0
        self.RandomR_Slider = QtWidgets.QSlider()
        self.RandomR_Slider.setMinimum(0)
        self.RandomR_Slider.setMaximum(360)
        self.RandomR_Slider.setProperty("value", getValueR)
        self.RandomR_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.RandomR_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.RandomR_Slider.setTickInterval(1)
        self.RandomR_Slider.setFixedHeight(22)
        self.RandomR_Slider.valueChanged.connect(self.SliderRotRandom_Action)
        SliderRandomR_HLyt.addWidget(self.RandomR_Slider)

        self.RandomR_SpinBox = QtWidgets.QDoubleSpinBox()
        self.RandomR_SpinBox.setDecimals(1)
        self.RandomR_SpinBox.setFixedWidth(40)
        self.RandomR_SpinBox.setFixedHeight(18)
        self.RandomR_SpinBox.setRange(0, 1000)
        self.RandomR_SpinBox.setValue(getValueR)
        self.RandomR_SpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.RandomR_SpinBox.editingFinished.connect(self.SpinRotRandom_Action)
        SliderRandomR_HLyt.addWidget(self.RandomR_SpinBox)





        # ___________________________________________## RANDOM ROTATION
        # ___________________________________________##
        SliderRandomS_HLyt = QtWidgets.QHBoxLayout(self)
        LINEAR_MLyt.addLayout(SliderRandomS_HLyt)
        LINEAR_MLyt.addSpacing(16)

        Random_label = QtWidgets.QLabel("Scale      ")
        #SliderRandomS_HLyt.addWidget(Random_label)

        try:
            getValueS = mc.getAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.scaleX")
        except:
            getValueS = 0
        self.RandomS_Slider = QtWidgets.QSlider()
        self.RandomS_Slider.setMinimum(0)
        self.RandomS_Slider.setMaximum(100)
        self.RandomS_Slider.setProperty("value", getValueS)
        self.RandomS_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.RandomS_Slider.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.RandomS_Slider.setTickInterval(1)
        self.RandomS_Slider.setFixedHeight(22)
        self.RandomS_Slider.valueChanged.connect(self.SliderScaleRandom_Action)
        #SliderRandomS_HLyt.addWidget(self.RandomS_Slider)

        self.RandomS_SpinBox = QtWidgets.QDoubleSpinBox()
        self.RandomS_SpinBox.setDecimals(1)
        self.RandomS_SpinBox.setFixedWidth(40)
        self.RandomS_SpinBox.setFixedHeight(18)
        self.RandomS_SpinBox.setRange(0, 1000)
        self.RandomS_SpinBox.setValue(getValueS)
        self.RandomS_SpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.RandomS_SpinBox.editingFinished.connect(self.SpinScaleRandom_Action)
        #SliderRandomS_HLyt.addWidget(self.RandomS_SpinBox)

















        #---------------------------------
        LINEAR_MLyt.addSpacing(6)
        self.BakeButton = QtWidgets.QPushButton()
        self.BakeButton.setText(" B A K E ")
        self.BakeButton.setFixedHeight(22)
        self.BakeButton.setObjectName("StoreSet")
        self.BakeButton.clicked.connect(self.Bake)
        LINEAR_MLyt.addWidget(self.BakeButton)




















        LINEAR_MLyt.addStretch()










    def SliderNumber_Action(self):
        NumberValue = self.Number_Slider.value()
        self.Number_SpinBox.setValue(NumberValue)
        self.SpinBoxA_Action()

    def SpinBoxA_Action(self):
        SpinBoxAValue = self.Number_SpinBox.value()
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Distribute.pointCount", SpinBoxAValue)
        self.Number_Slider.setValue(SpinBoxAValue)
        self.Number_SpinBox.clearFocus()





    def SliderPosRandom_Action(self):
        NumberValue = self.RandomP_Slider.value()
        self.RandomP_SpinBox.setValue(NumberValue)
        self.SpinPosRandom_Action()

    def SpinPosRandom_Action(self):
        SpinBoxValue = self.RandomP_SpinBox.value()
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.positionX", SpinBoxValue)
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.positionY", SpinBoxValue)
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.positionZ", SpinBoxValue)
        self.RandomP_Slider.setValue(SpinBoxValue)
        self.RandomP_SpinBox.clearFocus()


    def SliderRotRandom_Action(self):
        NumberValue = self.RandomR_Slider.value()
        self.RandomR_SpinBox.setValue(NumberValue)
        self.SpinRotRandom_Action()

    def SpinRotRandom_Action(self):
        SpinBoxValue = self.RandomR_SpinBox.value()
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.rotationX", SpinBoxValue)
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.rotationY", SpinBoxValue)
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.rotationZ", SpinBoxValue)
        self.RandomR_Slider.setValue(SpinBoxValue)
        self.RandomR_SpinBox.clearFocus()



    def SliderScaleRandom_Action(self):
        NumberValue = self.RandomS_Slider.value()
        self.RandomS_SpinBox.setValue(NumberValue)
        self.SpinScaleRandom_Action()

    def SpinScaleRandom_Action(self):
        SpinBoxValue = self.RandomS_SpinBox.value()
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.scaleX", SpinBoxValue)
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.scaleY", SpinBoxValue)
        mc.setAttr("ModIt_Duplicate_Radial" + str(Num) + "_Random.scaleZ", SpinBoxValue)
        self.RandomS_Slider.setValue(SpinBoxValue)
        self.RandomS_SpinBox.clearFocus()


    def get_locatorOrign(self):
        mc.select("ModIt_Radial_OrignLoc" + str(Num))

    def get_locatorTarget(self):
        mc.select("ModIt_Radial_Loc" + str(Num))



    def Bake(self):
        MashInstancer = "ModIt_Duplicate_Radial" + Num + "_Instancer"

        mc.select(MashInstancer)
        import maya.mel as mel
        mel.eval('MASHBakeGUI;')
        mc.select(MashInstancer)
        import MASHbakeInstancer;
        MASHbakeInstancer.MASHbakeInstancer(False)
        mc.deleteUI("mashBakeStill", window=True)

        mc.select("ModIt_Duplicate_Radial" + Num + "_Instancer_objects")
        mc.CenterPivot()
        mc.delete(ch=True)
        mc.rename("ModIt_Radial_1")


        mc.delete("ModIt_Radial_OrignLoc" + Num)


        if mc.window("Radial Duplication", exists=True):
            mc.deleteUI("Radial Duplication")




def Dock(Widget, width=200, height=200, hp="free", show=True):
    label = getattr(Widget, "label", WindowsTitle)

    try:
        mc.deleteUI(WindowsTitle)
    except RuntimeError:
        pass

    dockControl = mc.workspaceControl(
        WindowsTitle,
        initialWidth=width,
        minimumWidth=False,
        widthProperty=hp,
        heightProperty=hp,
        label=label
    )

    dockPtr = omui.MQtUtil.findControl(dockControl)
    dockWidget = QtCompat.wrapInstance(int(dockPtr), QtWidgets.QWidget)
    dockWidget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    child = Widget(dockWidget)
    dockWidget.layout().addWidget(child)

    if show:
        mc.evalDeferred(
            lambda *args: mc.workspaceControl(
                dockControl,
                edit=True,
                widthProperty="free",
                restore=True
            )
        )
    return child

def showUI():
    ui = Dock(Radial_UI)
    ui.show()


    # Get a pointer and convert it to Qt Widget object
    qw = omui.MQtUtil.findWindow(WindowsTitle)
    widget = wrapInstance(int(qw), QWidget)
    # Create a QIcon object
    icon = QIcon(IconPath + "ModIt_Window_Ico.png")
    # Assign the icon
    widget.setWindowIcon(icon)

    return ui




