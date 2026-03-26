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
importlib.reload(ModIt_CSS)

from . import ModIt_2Bevels_UI
importlib.reload(ModIt_2Bevels_UI)



##______________________GLOBAL VAR
##PATH_SET
IconPath = ModIt_Global.IconsPathThemeClassic
PreferencePath = ModIt_Global.PreferencePath
ToolsPath = ModIt_Global.ToolPath

# ******************************************
#           BUTTONS PARAMS
# ******************************************
iconFixeSize = 32
iconButtonSize = 32
separatorWidth = ModIt_Global.separatorWidth


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


class MESH_LAYOUT(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        SECTION_MESH_LAYOUT = QtWidgets.QVBoxLayout()  # MAIN
        SECTION_MESH_LAYOUT.setContentsMargins(10, 0, 5, 0)
        SECTION_MESH_LAYOUT.setSpacing(0)
        self.setLayout(SECTION_MESH_LAYOUT)


        MESH_HLyt_1 = QtWidgets.QHBoxLayout()
        MESH_HLyt_1.setContentsMargins(0,0,0,0)
        MESH_HLyt_1.setSpacing(0)
        SECTION_MESH_LAYOUT.addLayout(MESH_HLyt_1)

        ##-------------------------------------------------------------------------------   SOFT/HARD EDGE
        ##---------------------------------------------------- SET SOFT EDGE
        self.SoftEdge_btn = QtWidgets.QPushButton()
        self.SoftEdge_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.SoftEdge_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.SoftEdge_btn.setIcon(QtGui.QIcon(IconPath + "polySoftEdge.png"))
        self.SoftEdge_btn.setToolTip("  Soften Edge  ")
        self.SoftEdge_btn.clicked.connect(partial(self.SetSoftHardAngle, 180))
        MESH_HLyt_1.addWidget(self.SoftEdge_btn)

        ##---------------------------------------------------- SET HARD EDGE
        self.HardEdge_btn = QtWidgets.QPushButton()
        self.HardEdge_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.HardEdge_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.HardEdge_btn.setIcon(QtGui.QIcon(IconPath + "polyHard.png"))
        self.HardEdge_btn.setToolTip("  Harden Edge  ")
        self.HardEdge_btn.clicked.connect(partial(self.SetSoftHardAngle, 0))
        MESH_HLyt_1.addWidget(self.HardEdge_btn)

        MESH_HLyt_1.addSpacing(5)
        self.Separator = QtWidgets.QLabel()
        self.Separator.setFixedSize(1,30)
        self.Separator.setStyleSheet("background-color:#fba636;")
        MESH_HLyt_1.addWidget(self.Separator)
        MESH_HLyt_1.addSpacing(5)


        ##---------------------------------------------------- GET HARD EDGE
        self.SelectHardEdge_btn = MyCustomBtn_Widget()
        self.SelectHardEdge_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.SelectHardEdge_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.SelectHardEdge_btn.setIcon(QtGui.QIcon(IconPath + "HardEdge.png"))
        self.SelectHardEdge_btn.setToolTip("  Get Hard Edges from Selection  ")
        self.SelectHardEdge_btn.clicked.connect(self.GetHardEdges)
        MESH_HLyt_1.addWidget(self.SelectHardEdge_btn)
        #   C O N N E C T   P O P U P   M E N U   T O   O U R   B U T T O N
        self.SelectHardEdge_btn.customContextMenuRequested.connect(self.showPopupEdgeAngle)
        #   CUBE M E N U   I T E M S
        self.popupMenuEdgeAngle = QtWidgets.QMenu()
        Angle_Entry_1 = self.popupMenuEdgeAngle.addAction("Smooth 30°")
        Angle_Entry_1.triggered.connect(partial(self.SetSoftHardAngle, 30))
        Angle_Entry_2 = self.popupMenuEdgeAngle.addAction("Smooth 35°")
        Angle_Entry_2.triggered.connect(partial(self.SetSoftHardAngle, 35))
        Angle_Entry_3 = self.popupMenuEdgeAngle.addAction("Smooth 40°")
        Angle_Entry_3.triggered.connect(partial(self.SetSoftHardAngle, 40))
        Angle_Entry_4 = self.popupMenuEdgeAngle.addAction("Smooth 45°")
        Angle_Entry_4.triggered.connect(partial(self.SetSoftHardAngle, 45))

        MESH_HLyt_1.addSpacing(12)
        self.Separator = QtWidgets.QLabel()
        self.Separator.setFixedSize(1,30)
        self.Separator.setStyleSheet("background-color:#434343;")
        MESH_HLyt_1.addWidget(self.Separator)
        MESH_HLyt_1.addSpacing(12)


        ##-------------------------------------------------------------------------------   SYMETRY
        ##---------------------------------------------------- SYM MERGE
        self.SymMerge_btn = MyCustomBtn_Widget()
        self.SymMerge_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.SymMerge_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.SymMerge_btn.setIcon(QtGui.QIcon(IconPath + "SymMerge.png"))
        self.SymMerge_btn.setToolTip(" Symmetry based on Pivot and Merge ")
        self.SymMerge_btn.clicked.connect(partial(self.Symmetry, 4))
        MESH_HLyt_1.addWidget(self.SymMerge_btn)
        #   C O N N E C T   P O P U P   M E N U   T O   O U R   B U T T O N
        self.SymMerge_btn.customContextMenuRequested.connect(self.showPopupSymMerge)
        #   CUBE M E N U   I T E M S
        self.popupMenuSymMerge = QtWidgets.QMenu()
        SymMerge_Entry_1 = self.popupMenuSymMerge.addAction("X")
        SymMerge_Entry_1.triggered.connect(partial(self.Symmetry, 0))
        SymMerge_Entry_2 = self.popupMenuSymMerge.addAction("Y")
        SymMerge_Entry_2.triggered.connect(partial(self.Symmetry, 1))
        SymMerge_Entry_3 = self.popupMenuSymMerge.addAction("Z")
        SymMerge_Entry_3.triggered.connect(partial(self.Symmetry, 2))

        MESH_HLyt_1.addSpacing(5)
        self.Separator = QtWidgets.QLabel()
        self.Separator.setFixedSize(1,30)
        self.Separator.setStyleSheet("background-color:#ff5f70;")
        MESH_HLyt_1.addWidget(self.Separator)
        MESH_HLyt_1.addSpacing(5)


        ##---------------------------------------------------- SYM FLIP
        self.SymFlip_btn = MyCustomBtn_Widget()
        self.SymFlip_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.SymFlip_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.SymFlip_btn.setIcon(QtGui.QIcon(IconPath + "SymFlip.png"))
        self.SymFlip_btn.setToolTip("  Flip on World Axis  ")
        self.SymFlip_btn.clicked.connect(partial(self.FlipWorld, 4))
        MESH_HLyt_1.addWidget(self.SymFlip_btn)
        #   C O N N E C T   P O P U P   M E N U   T O   O U R   B U T T O N
        self.SymFlip_btn.customContextMenuRequested.connect(self.showPopupSymFlip)
        #   CUBE M E N U   I T E M S
        self.popupMenuSymFlip = QtWidgets.QMenu()
        SymFlip_Entry_1 = self.popupMenuSymFlip.addAction("X")
        SymFlip_Entry_1.triggered.connect(partial(self.FlipWorld, 0))
        SymFlip_Entry_2 = self.popupMenuSymFlip.addAction("Y")
        SymFlip_Entry_2.triggered.connect(partial(self.FlipWorld, 1))
        SymFlip_Entry_3 = self.popupMenuSymFlip.addAction("Z")
        SymFlip_Entry_3.triggered.connect(partial(self.FlipWorld, 2))

        ##---------------------------------------------------- SYM PIVOT
        self.SymPivot_btn = MyCustomBtn_Widget()
        self.SymPivot_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.SymPivot_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.SymPivot_btn.setIcon(QtGui.QIcon(IconPath + "SymPivot.png"))
        self.SymPivot_btn.setToolTip("  Flip based on Pivot  ")
        self.SymPivot_btn.clicked.connect(partial(self.FlipPivot, 4))
        MESH_HLyt_1.addWidget(self.SymPivot_btn)
        #   C O N N E C T   P O P U P   M E N U   T O   O U R   B U T T O N
        self.SymPivot_btn.customContextMenuRequested.connect(self.showPopupSymPivot)
        #   CUBE M E N U   I T E M S
        self.popupMenuSymPivot = QtWidgets.QMenu()
        SymPivot_Entry_1 = self.popupMenuSymPivot.addAction("X")
        SymPivot_Entry_1.triggered.connect(partial(self.FlipPivot, 0))
        SymPivot_Entry_2 = self.popupMenuSymPivot.addAction("Y")
        SymPivot_Entry_2.triggered.connect(partial(self.FlipPivot, 1))
        SymPivot_Entry_3 = self.popupMenuSymPivot.addAction("Z")
        SymPivot_Entry_3.triggered.connect(partial(self.FlipPivot, 2))




        ## ______________________________________________________________________________________/ Separator
        SECTION_MESH_LAYOUT.addSpacing(4)
        self.Separator = QtWidgets.QLabel()
        self.Separator.setFixedSize(280,1)
        self.Separator.setStyleSheet("background-color:#434343;")
        SECTION_MESH_LAYOUT.addWidget(self.Separator)
        SECTION_MESH_LAYOUT.addSpacing(4)

        ##-------------------------------------------------------------------------------   OPERATIONS
        MESH_HLyt_2 = QtWidgets.QHBoxLayout()
        MESH_HLyt_2.setContentsMargins(10,0,0,0)
        MESH_HLyt_2.setSpacing(5)
        SECTION_MESH_LAYOUT.addLayout(MESH_HLyt_2)

        Operation_VLyt = QtWidgets.QVBoxLayout()
        MESH_HLyt_2.addLayout(Operation_VLyt)
        Op_Line_1_Hlyt = QtWidgets.QHBoxLayout()
        Operation_VLyt.addLayout(Op_Line_1_Hlyt)
        Op_Line_2_Hlyt = QtWidgets.QHBoxLayout()
        Operation_VLyt.addLayout(Op_Line_2_Hlyt)


        ##---------------------------------------------------- COMBINE
        self.Combine_btn = MyCustomBtn_Widget()
        self.Combine_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.Combine_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.Combine_btn.setIcon(QtGui.QIcon(IconPath + "Combine.png"))
        self.Combine_btn.setToolTip("  Combine  ")
        self.Combine_btn.clicked.connect(self.Combine)
        Op_Line_1_Hlyt.addWidget(self.Combine_btn)

        ##---------------------------------------------------- SEPARATE
        self.Separate_btn = MyCustomBtn_Widget()
        self.Separate_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.Separate_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.Separate_btn.setIcon(QtGui.QIcon(IconPath + "Separate.png"))
        self.Separate_btn.setToolTip("  Separate  ")
        self.Separate_btn.clicked.connect(self.Separate)
        Op_Line_1_Hlyt.addWidget(self.Separate_btn)
        ##---------------------------------------------------- DUPLICATE FACE
        self.DupFace_btn = MyCustomBtn_Widget()
        self.DupFace_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.DupFace_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.DupFace_btn.setIcon(QtGui.QIcon(IconPath + "FaceDupli.png"))
        self.DupFace_btn.setToolTip("  Duplicate Faces  ")
        self.DupFace_btn.clicked.connect(self.DuplicatFace)
        Op_Line_2_Hlyt.addWidget(self.DupFace_btn)

        ##---------------------------------------------------- EXTRACT FACE
        self.ExtractFace_btn = MyCustomBtn_Widget()
        self.ExtractFace_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.ExtractFace_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.ExtractFace_btn.setIcon(QtGui.QIcon(IconPath + "FaceExtract.png"))
        self.ExtractFace_btn.setToolTip("  Extract Faces  ")
        self.ExtractFace_btn.clicked.connect(self.ExtractFace)
        Op_Line_2_Hlyt.addWidget(self.ExtractFace_btn)




        MESH_HLyt_2.addSpacing(12)
        self.Separator = QtWidgets.QLabel()
        self.Separator.setFixedSize(1,60)
        self.Separator.setStyleSheet("background-color:#434343;")
        MESH_HLyt_2.addWidget(self.Separator)
        MESH_HLyt_2.addSpacing(12)

        Bevels_VLyt = QtWidgets.QVBoxLayout()
        MESH_HLyt_2.addLayout(Bevels_VLyt)



        ##---------------------------------------------------- MIXED BEVEL
        self.BevelVar_OnBothBorder_btn = QtWidgets.QPushButton()
        self.BevelVar_OnBothBorder_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.BevelVar_OnBothBorder_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.BevelVar_OnBothBorder_btn.setIcon(QtGui.QIcon(IconPath + "2Bevel.png"))
        self.BevelVar_OnBothBorder_btn.setToolTip(" Mixed Bevels / Shift+Click : Mixed Bevels on 2 borders  ")
        self.BevelVar_OnBothBorder_btn.clicked.connect(self.BevelVar)
        Bevels_VLyt.addWidget(self.BevelVar_OnBothBorder_btn)


        ##---------------------------------------------------- BEVEL VERTEX
        self.BevelVertex_btn = QtWidgets.QPushButton()
        self.BevelVertex_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.BevelVertex_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.BevelVertex_btn.setIcon(QtGui.QIcon(IconPath + "fillet.png"))
        self.BevelVertex_btn.setToolTip("  Bevel Vertex on open area (use Marking Menu to change segment/offset ")
        self.BevelVertex_btn.clicked.connect(self.BevelVertex)
        Bevels_VLyt.addWidget(self.BevelVertex_btn)


        MESH_HLyt_2.addSpacing(12)
        self.Separator = QtWidgets.QLabel()
        self.Separator.setFixedSize(1,60)
        self.Separator.setStyleSheet("background-color:#434343;")
        MESH_HLyt_2.addWidget(self.Separator)
        MESH_HLyt_2.addSpacing(12)

        Flow_VLyt = QtWidgets.QVBoxLayout()
        MESH_HLyt_2.addLayout(Flow_VLyt)



        ##---------------------------------------------------- EDGE FLOW
        self.EdgeFlow_btn = QtWidgets.QPushButton()
        self.EdgeFlow_btn.setFixedSize(iconFixeSize, iconFixeSize)
        self.EdgeFlow_btn.setIconSize(QtCore.QSize(iconButtonSize, iconButtonSize))
        self.EdgeFlow_btn.setIcon(QtGui.QIcon(IconPath + "fixFlow.png"))
        self.EdgeFlow_btn.setToolTip(" Fix Edge Flow  ")
        self.EdgeFlow_btn.clicked.connect(self.EdgeFlow)
        Flow_VLyt.addWidget(self.EdgeFlow_btn)


        MESH_HLyt_2.addSpacing(20)


        ##---------------------------------------------------- Add to Layout









    #------------------------------------------------
    ##----------------------------------------------------   D E F I N I T I O N
    # ------------------------------------------------ MENUS
    def showPopupEdgeAngle(self, position):
        self.popupMenuEdgeAngle.exec(self.SelectHardEdge_btn.mapToGlobal(position))
        self.SelectHardEdge_btn.update()

    def showPopupSymMerge(self, position):
        self.popupMenuSymMerge.exec(self.SymMerge_btn.mapToGlobal(position))
        self.SymMerge_btn.update()

    def showPopupSymFlip(self, position):
        self.popupMenuSymFlip.exec(self.SymFlip_btn.mapToGlobal(position))
        self.SymFlip_btn.update()

    def showPopupSymPivot(self, position):
        self.popupMenuSymPivot.exec(self.SymPivot_btn.mapToGlobal(position))
        self.SymPivot_btn.update()



    #------------------------------------------------ ACTIONS
    def BAM(self):
        print("BAMMM")

    def SetSoftHardAngle(self, angle):
        mc.polySoftEdge(a= angle, ch=1)

    def GetHardEdges(self):
        mc.undoInfo(openChunk=True, infinity=True)
        obSelName = str(mc.ls(sl=True)[0])
        objSel = mc.ls(sl=True)
        mc.ConvertSelectionToEdgePerimeter()

        # verif if perim or nor
        verifPerim = mc.ls(sl=True)
        print(verifPerim)
        if verifPerim == []:
            mc.select(objSel)
            mc.polySelectConstraint(m=3, t=0x8000, sm=1)
            mc.polySelectConstraint(m=0)
            mel.eval('doMenuComponentSelectionExt(" ' + obSelName + '", "edge", 0);')
        else:
        # Store EdgePerim Set
            mc.sets(n="ModIt_EdgePerim_tempSet")

            mc.polySelectConstraint(m=3, t=0x8000, sm=1)
            mc.polySelectConstraint(m=0)

            # Store All HardEdge
            mc.sets(n="ModIt_AllHardEdge_tempSet")

            # Sub Perim Edge
            mc.select("ModIt_EdgePerim_tempSet")
            mc.sets(rm='ModIt_AllHardEdge_tempSet')

            mc.select("ModIt_AllHardEdge_tempSet")

            mc.delete("ModIt_AllHardEdge_tempSet")
            mc.delete("ModIt_EdgePerim_tempSet")

            mel.eval('doMenuComponentSelectionExt(" ' + obSelName + '", "edge", 0);')

        mc.undoInfo(closeChunk=True)






    def Symmetry(self, axis):
        # Store Sel
        selection = mc.ls(sl=True, fl=True, dag=True)
        selVerif = mc.ls(sl=True)

        #VERIR SEULEMENT 1 MESH
        try:
            mc.objectType(selection[1])
        except:
            ModIt_Global.WarningWindow(" Symmetry is only working on Geometry Mesh.", 350)
            return

        if mc.objectType(selection[1]) != "mesh":
            ModIt_Global.WarningWindow(" Symmetry is only working on Geometry Mesh.", 350)
            return



        if len(selVerif) > 1:
            ModIt_Global.WarningWindow(" You should select ONE mesh only.", 350)
            return

        selection = selection[0]




        mc.undoInfo(openChunk=True, infinity=True)

        #AXIS Info
        if axis == 4:
            AXIS = (json.load(open(PreferencePath + 'Pref_SymAxis.json', "r"))['VALUE'])
        else:
            AXIS = axis

        ##_____________________________________ Pour avoir l'info de quel sens faire la sym
        # Clean
        if mc.objExists("ModItSymInfo"):
            mc.delete("ModItSymInfo")
        if mc.objExists("ModIt_Sym_Loc"):
            mc.delete("ModIt_Sym_Loc")

        # Dup and Center Piv
        mc.duplicate(n="ModItSymInfo")
        mc.CenterPivot()
        mc.FreezeTransformations()

        # PlaceLocator / Freeze
        mc.spaceLocator(p=[0, 0, 0], n="ModIt_Sym_Loc")
        mc.select("ModIt_Sym_Loc", "ModItSymInfo")
        mc.MatchTransform()
        mc.select("ModIt_Sym_Loc")
        mc.FreezeTransformations()

        # Mathc Locator /
        mc.select("ModIt_Sym_Loc", selection)
        mc.MatchTransform()

        # Analyz = VALUE + -
        if AXIS == 0:
            axisLetter = "X"
        elif AXIS == 1:
            axisLetter = "Y"
        elif AXIS == 2:
            axisLetter = "Z"

        locAxeValue = mc.getAttr("ModIt_Sym_Loc.translate" + axisLetter)
        if locAxeValue > 0:
            axisDir = -1
            print("axisDir = " + str(axisDir))
        if locAxeValue < 0:
            axisDir = 1
            print("axisDir = " + str(axisDir))
        if locAxeValue == 0:
            axisDir = 1
            print("axisDir = " + str(axisDir))

        # Clean
        if mc.objExists("ModItSymInfo"):
            mc.delete("ModItSymInfo")
        if mc.objExists("ModIt_Sym_Loc"):
            mc.delete("ModIt_Sym_Loc")



        ##_____________________________________
        mc.select(selection)
        mc.polyMirrorFace(cutMesh=1, mirrorAxis= 1, axis= AXIS, axisDirection= axisDir, mergeMode=1, mergeThresholdType=0,
                          mirrorPosition=0, smoothingAngle=30, flipUVs=0, ch=1)

        mc.delete(ch=True)
        mc.SelectVertexMask()
        mc.SelectToggleMode()


        mc.undoInfo(closeChunk=True)


































    def FlipWorld(self, axis):
        mc.undoInfo(openChunk=True, infinity=True)
        selection = mc.ls(sl = True, fl = True, dag = True, hd = 1)

        #CLEAN
        if mc.objExists("DupliF"):
            mc.delete("DupliF")

        DupSel = mc.duplicate(rc= True)
        mc.group(em= True, n="DupliF")
        mc.parent(DupSel[0], 'DupliF')

        if axis == 0:
            mc.setAttr("DupliF.scaleX", -1)
        elif axis == 1:
            mc.setAttr("DupliF.scaleY", -1)
        elif axis == 2:
            mc.setAttr("DupliF.scaleZ", -1)
        elif axis == 4:
            AXIS = (json.load(open(PreferencePath + 'Pref_SymAxis.json', "r"))['VALUE'])
            if AXIS == 0:
                mc.setAttr("DupliF.scaleX", -1)
            elif AXIS == 1:
                mc.setAttr("DupliF.scaleY", -1)
            elif AXIS == 2:
                mc.setAttr("DupliF.scaleZ", -1)



        mc.select("DupliF")
        mc.FreezeTransformations()
        mc.delete(ch=True)
        mc.Ungroup()
        mc.undoInfo(closeChunk=True)

    def FlipPivot(self, axis):
        mc.undoInfo(openChunk=True, infinity=True)
        mc.FreezeTransformations()
        mc.duplicate(rc= True)
        mc.rename("DupliF")
        if axis == 0:
            mc.setAttr("DupliF.scaleX", -1)
        elif axis == 1:
            mc.setAttr("DupliF.scaleY", -1)
        elif axis == 2:
            mc.setAttr("DupliF.scaleZ", -1)
        elif axis == 4:
            AXIS = (json.load(open(PreferencePath + 'Pref_SymAxis.json', "r"))['VALUE'])
            if AXIS == 0:
                mc.setAttr("DupliF.scaleX", -1)
            elif AXIS == 1:
                mc.setAttr("DupliF.scaleY", -1)
            elif AXIS == 2:
                mc.setAttr("DupliF.scaleZ", -1)

        mc.rename("DupliF", "DupliFlip")
        mc.FreezeTransformations()
        mc.delete(ch=True)
        mc.undoInfo(closeChunk=True)

    def Separate(self):
        mc.undoInfo(openChunk=True, infinity=True)

        testSelection = mc.ls(sl=True, l=True)
        if testSelection == []:
            print("ModIt Error : Nothing Selected")
            return
        else:
            mc.SeparatePolygon()
            getParent = mc.listRelatives(parent=True, f=True)
            separateSel = mc.ls(sl=True, l=True)
            mc.CenterPivot()
            addSelToNewSet = mc.sets(n='ModIt_Set_Separate')
            mc.delete(ch=True)
            mc.ungroup(getParent)
            mc.select('ModIt_Set_Separate')
            newSel = mc.ls(sl=True, l=True)
            mc.FreezeTransformations()
            mc.delete('ModIt_Set_Separate')
            mc.select(newSel[0])

        mc.undoInfo(closeChunk=True)

    def Combine(self):
        mc.undoInfo(openChunk=True, infinity=True)
        try:
            mel.eval('source "' + ToolsPath + 'Combine.mel"')
            mc.CenterPivot()
        except:
            ModIt_Global.WarningWindow("You should select at least 2 meshes.", 300)
            return

        mc.undoInfo(closeChunk=True)


    def ExtractFace(self):
        #Verif Selection is Face
        checkSelectedComponent = mc.filterExpand(sm=34)
        if checkSelectedComponent == None:
            ModIt_Global.WarningWindow(" You should select Faces.", 300)
            return
        else:
            mel.eval('source "' + ToolsPath + 'ExtractFace.mel"')

    def DuplicatFace(self):
        #Verif Selection is Face
        checkSelectedComponent = mc.filterExpand(sm=34)
        if checkSelectedComponent == None:
            ModIt_Global.WarningWindow(" You should select Faces.", 300)
            return
        else:
            mel.eval('source "' + ToolsPath + 'DuplicateFace.mel"')

    def EdgeFlow(self):
        #Verif Selection is Edge
        checkSelectedComponent = mc.filterExpand(sm=32)
        if checkSelectedComponent == None:
            ModIt_Global.WarningWindow(" You should select Edges.", 300)
            return
        else:
            mc.polyEditEdgeFlow(ch=1, adjustEdgeFlow=1)
        




    def BevelVertex(self):
        #Verif Selection is Vertex
        checkSelectedComponent = mc.filterExpand(sm=31)
        if checkSelectedComponent == None:
            ModIt_Global.WarningWindow(" Works only for Vertex on border.", 300)
            return
        else:
            mc.undoInfo(openChunk=True, infinity=True)
            ###_________Selection
            VertexInitSelection = mc.ls(sl=True)
            mc.ConvertSelectionToFaces()
            mc.ConvertSelectionToContainedEdges()
            BorderAll = mc.sets(n="Border_Set")

            mc.select(VertexInitSelection)
            mc.ConvertSelectionToEdges()
            BorderToVerif = mc.sets(n="ToVerif_Set")

            # Return the union of two sets
            Verif = mc.sets("Border_Set", sub="ToVerif_Set")
            mc.select(Verif)
            EdgeSel = mc.ls(sl=True)

            mc.delete("Border_Set")
            mc.delete("ToVerif_Set")

            mc.polyExtrudeEdge(EdgeSel, kft=True, pvx=0, pvy=0, pvz=0, divisions=1, twist=0, taper=1, offset=0, thickness=0)

            mc.ConvertSelectionToFaces()
            extrudeFaces = mc.ls(sl=True)
            # mc.ToggleVisibilityAndKeepSelection()
            mc.ConvertSelectionToContainedEdges()
            edgeToBevel = mc.ls(sl=True)

            mel.eval('dR_DoCmd("bevelPress")')
            mc.undoInfo(closeChunk=True)





    def BevelVar_InMiddle(self):
        edgeSelect = mc.ls(sl=True, l=True)

        mc.undoInfo(openChunk=True, infinity=True)

        #CLEAN VERIF
        if mc.objExists("EdgePerimBefore_SET"):
            mc.delete("EdgePerimBefore_SET")
        if mc.objExists("EdgePerimAfter_SET"):
            mc.delete("EdgePerimAfter_SET")
        if mc.objExists("FaceToDel_SET"):
            mc.delete("FaceToDel_SET")
        if mc.objExists("OriginVertexSave_SET"):
            mc.delete("OriginVertexSave_SET")



        #START PROCEDURE
        mc.select(edgeSelect)
        mel.eval("SelectVertexMask;")
        mel.eval("SelectToggleMode;")
        objectName = mc.ls(sl=True, l=True)

        mc.select(edgeSelect)
        OriginVertexSave = mc.ConvertSelectionToVertices()
        mc.sets(n="OriginVertexSave_SET")

        # Get face shader
        mc.select(edgeSelect)
        mc.ConvertSelectionToFaces()
        cmds.hyperShade(shaderNetworksSelectMaterialNodes=True)
        getMaterial = cmds.ls(sl=True)[0]
        print(getMaterial)

        ##
        mc.select(edgeSelect)
        faceToDel = mc.ConvertSelectionToFaces()
        mc.sets(n="FaceToDel_SET")

        # Save PerimBefore
        mc.ConvertSelectionToEdgePerimeter()
        edgePerimBefore = mc.sets(n="EdgePerimBefore_SET")

        # Del Face to hole
        mc.select("FaceToDel_SET")
        mc.delete()

        mc.select("OriginVertexSave_SET")
        # Selected vertices
        vertexOrgerList = []
        for vertex in mc.ls(sl=1, fl=1):
            vertexOrgerList.append(vertex)

        vertexOne = vertexOrgerList[0]

        ##____ BEVEL VERTEX : 1 ______________________________________
        mc.select(vertexOne)
        ###_________Selection
        VertexInitSelection = mc.ls(sl=True)
        mc.ConvertSelectionToFaces()
        mc.ConvertSelectionToContainedEdges()
        BorderAll = mc.sets(n="Border_Set")

        mc.select(VertexInitSelection)
        mc.ConvertSelectionToEdges()
        BorderToVerif = mc.sets(n="ToVerif_Set")

        # Return the union of two sets
        Verif = mc.sets("Border_Set", sub="ToVerif_Set")
        mc.select(Verif)
        EdgeSel = mc.ls(sl=True)

        mc.delete("Border_Set")
        mc.delete("ToVerif_Set")

        mc.polyExtrudeEdge(EdgeSel, kft=True, pvx=0, pvy=0, pvz=0, divisions=1, twist=0, taper=1, offset=0, thickness=0)

        mc.ConvertSelectionToFaces()
        extrudeFaces = mc.ls(sl=True)
        mc.ConvertSelectionToContainedEdges()
        edgeToBevel = mc.ls(sl=True)

        mel.eval('dR_DoCmd("bevelPress")')
        mel.eval('string $getBevelNode[] = `listHistory -lv 1`;')
        mel.eval('setAttr ($getBevelNode[1] + ".segments") 4;')

        mc.setToolTo('moveSuperContext')

        ##____ BEVEL VERTEX : 2 ______________________________________
        mc.select("OriginVertexSave_SET")
        ###_________Selection
        VertexInitSelection = mc.ls(sl=True)
        mc.ConvertSelectionToFaces()
        mc.ConvertSelectionToContainedEdges()
        BorderAll = mc.sets(n="Border_Set")

        mc.select(VertexInitSelection)
        mc.ConvertSelectionToEdges()
        BorderToVerif = mc.sets(n="ToVerif_Set")

        # Return the union of two sets
        Verif = mc.sets("Border_Set", sub="ToVerif_Set")
        mc.select(Verif)
        EdgeSel = mc.ls(sl=True)

        mc.delete("Border_Set")
        mc.delete("ToVerif_Set")

        mc.polyExtrudeEdge(EdgeSel, kft=True, pvx=0, pvy=0, pvz=0, divisions=1, twist=0, taper=1, offset=0, thickness=0)

        mc.ConvertSelectionToFaces()
        extrudeFaces = mc.ls(sl=True)
        mc.ConvertSelectionToContainedEdges()
        edgeToBevel = mc.ls(sl=True)

        mel.eval('dR_DoCmd("bevelPress")')
        mel.eval('string $getBevelNode[] = `listHistory -lv 1`;')
        mel.eval('setAttr ($getBevelNode[1] + ".segments") 4;')

        mc.setToolTo('moveSuperContext')

        ##____ FILL HOLE and CONNECT ______________________________________
        # Get sel to Bridge then
        mc.select("EdgePerimBefore_SET")
        mc.FillHole()
        mc.sets(n="EdgePerimAfter_SET")
        mc.ConvertSelectionToContainedFaces()
        mc.delete()

        setDiff = mc.sets("EdgePerimBefore_SET", sub="EdgePerimAfter_SET")
        mc.select(setDiff)
        # BRIDGE
        mc.polyBridgeEdge(divisions=0)
        mc.ConvertSelectionToFaces()
        mc.polySoftEdge(angle=45)
        # Fill Holes
        mc.select("EdgePerimBefore_SET")
        mc.FillHole()
        mc.ConvertSelectionToContainedFaces()
        mc.hyperShade(assign=str(getMaterial))
        mc.select("EdgePerimAfter_SET")
        mc.polySoftEdge(angle=0)

        #Clear
        mc.SelectNone()  # Deselect All
        mc.delete("EdgePerimBefore_SET")
        mc.delete("EdgePerimAfter_SET")
        mc.delete("FaceToDel_SET")
        mc.delete("OriginVertexSave_SET")




        # 1 - GET ALL BEVEL NODE
        typ = "polyBevel3"
        nodes = []
        for obj in objectName:
            for node in cmds.listHistory(obj):
                if cmds.nodeType(node) == typ:
                    nodes.append(node)

        BevelA_node = nodes[0]
        BevelB_node = nodes[1]

        print(BevelA_node)
        print(BevelB_node)
        mc.undoInfo(closeChunk=True)
        #---------------------- UI



        #Pour eviter la boucle infinie avec le atClose qui clean la THumbScene
        if mc.window("Bevel2", exists=True):
            mc.deleteUI("Bevel2")


        importlib.reload(ModIt_2Bevels_UI)
        ModIt_2Bevels_UI.SEND_INFO(str(BevelA_node), str(BevelB_node))
        ModIt_2Bevels_UI.showUI()
    def BevelVar_OnBothBorder(self):
        # 1 - VERIF SELECTION
        edgeSelect = mc.ls(sl=True, l=True)

        #------------------
        mc.undoInfo(openChunk=True, infinity=True)

        #CLEAN VERIF
        if mc.objExists("savePerim_SET"):
            mc.delete("savePerim_SET")
        if mc.objExists("AllEdgePerim_SET"):
            mc.delete("AllEdgePerim_SET")
        if mc.objExists("saveVertex_SET"):
            mc.delete("saveVertex_SET")

        mel.eval("SelectVertexMask;")
        mel.eval("SelectToggleMode;")
        objectName = mc.ls(sl=True, l=True)

        print(objectName)
        # SAVE 2 VERTEX
        mc.select(edgeSelect)
        mc.ConvertSelectionToVertices()
        saveVertex = mc.ls(sl=True, l=True)
        saveVertex_SET = mc.sets(n="saveVertex_SET")

        print(saveVertex)
        if len(saveVertex) == 2:
            vertexA = saveVertex[0]
            vertexB = saveVertex[1]

        else:
            newList = str(saveVertex).replace(str(objectName[0]) + ".vtx[", "")
            print("newList" + newList)
            newList2 = newList.replace("]", "")
            print(newList2)
            newList3 = newList2.replace("[", "")
            print(newList3)
            newList4 = newList3.replace("'", "")
            print(newList4)
            newList5 = newList4.split(":")
            numVertA = newList5[0]
            numVertB = newList5[1]
            print(numVertA)
            print(numVertB)

            vertexA = str(objectName[0]) + str(".vtx[") + str(numVertA) + str("]")
            vertexB = str(objectName[0]) + str(".vtx[") + str(numVertB) + str("]")
            print(vertexA)
            print(vertexB)

        # SAVE FACE
        mc.select(edgeSelect)
        mc.ConvertSelectionToFaces()
        convertFace = mc.ls(sl=True, l=True)




        mc.ConvertSelectionToEdgePerimeter()
        savePerim = mc.ls(sl=True, l=True)
        savePerim_SET = mc.sets(n="savePerim_SET")

        mc.select(convertFace)
        mc.delete()

        mc.select(vertexB)
        ##____BEVEL VERTEX______________________________________
        ###_________Selection
        VertexInitSelection = mc.ls(sl=True)
        mc.ConvertSelectionToFaces()
        mc.ConvertSelectionToContainedEdges()
        BorderAll = mc.sets(n="Border_Set")

        mc.select(VertexInitSelection)
        mc.ConvertSelectionToEdges()
        BorderToVerif = mc.sets(n="ToVerif_Set")

        # Return the union of two sets
        Verif = mc.sets("Border_Set", sub="ToVerif_Set")
        mc.select(Verif)
        EdgeSel = mc.ls(sl=True)

        mc.delete("Border_Set")
        mc.delete("ToVerif_Set")

        mc.polyExtrudeEdge(EdgeSel, kft=True, pvx=0, pvy=0, pvz=0, divisions=1, twist=0, taper=1, offset=0, thickness=0)

        mc.ConvertSelectionToFaces()
        extrudeFaces = mc.ls(sl=True)
        # mc.ToggleVisibilityAndKeepSelection()
        mc.ConvertSelectionToContainedEdges()
        edgeToBevel = mc.ls(sl=True)

        mel.eval('dR_DoCmd("bevelPress")')
        mel.eval('string $getBevelNode[] = `listHistory -lv 1`;')
        mel.eval('setAttr ($getBevelNode[1] + ".segments") 4;')

        mc.setToolTo('moveSuperContext')
        mc.select(vertexA)



        ##____BEVEL VERTEX______________________________________
        ###_________Selection
        VertexInitSelection = mc.ls(sl=True)
        mc.ConvertSelectionToFaces()
        mc.ConvertSelectionToContainedEdges()
        BorderAll = mc.sets(n="Border_Set")

        mc.select(VertexInitSelection)
        mc.ConvertSelectionToEdges()
        BorderToVerif = mc.sets(n="ToVerif_Set")

        # Return the union of two sets
        Verif = mc.sets("Border_Set", sub="ToVerif_Set")
        mc.select(Verif)
        EdgeSel = mc.ls(sl=True)

        mc.delete("Border_Set")
        mc.delete("ToVerif_Set")

        mc.polyExtrudeEdge(EdgeSel, kft=True, pvx=0, pvy=0, pvz=0, divisions=1, twist=0, taper=1, offset=0, thickness=0)

        mc.ConvertSelectionToFaces()
        extrudeFaces = mc.ls(sl=True)
        # mc.ToggleVisibilityAndKeepSelection()
        mc.ConvertSelectionToContainedEdges()
        edgeToBevel = mc.ls(sl=True)

        mel.eval('dR_DoCmd("bevelPress")')
        mc.setToolTo('moveSuperContext')
        mel.eval('string $getBevelNode[] = `listHistory -lv 1`;')
        mel.eval('setAttr ($getBevelNode[1] + ".segments") 4;')

        # GET LE CENTER VERTEX
        mc.select(savePerim_SET)
        # mc.SelectEdgeLoopSp()
        mc.ConvertSelectionToEdgePerimeter()
        AllEdgePerim = mc.ls(sl=True, l=True)
        AllEdgePerim_SET = mc.sets(n="AllEdgePerim_SET")

        mc.select(mc.sets(savePerim_SET, sub=AllEdgePerim_SET))

        mc.polyBridgeEdge(divisions=0)
        mc.ConvertSelectionToFaces()
        mc.polySoftEdge(angle=45)

        # Fill HOle
        mc.select(savePerim_SET)
        mc.FillHole()
        mc.ConvertSelectionToFaces()
        mc.polySoftEdge(angle=45)

        # CLEAN
        mc.SelectNone()  # Deselect All
        mc.delete(savePerim_SET)
        mc.delete(AllEdgePerim_SET)
        mc.delete(saveVertex_SET)



        # 1 - GET ALL BEVEL NODE
        typ = "polyBevel3"
        nodes = []
        for obj in objectName:
            for node in cmds.listHistory(obj):
                if cmds.nodeType(node) == typ:
                    nodes.append(node)

        BevelA_node = nodes[0]
        BevelB_node = nodes[1]

        print(BevelA_node)
        print(BevelB_node)
        mc.undoInfo(closeChunk=True)
        #---------------------- UI



        #Pour eviter la boucle infinie avec le atClose qui clean la THumbScene
        if mc.window("Bevel2", exists=True):
            mc.deleteUI("Bevel2")


        importlib.reload(ModIt_2Bevels_UI)
        ModIt_2Bevels_UI.SEND_INFO(str(BevelA_node), str(BevelB_node))
        ModIt_2Bevels_UI.showUI()


    def BevelVar(self):
        edgeSelect = mc.ls(sl=True, l=True)

        # __________________________________________________________________________ 1 - VERIF SELECTION SIMPLE
        if edgeSelect == []:
            ModIt_Global.WarningWindow("You should select one edge", 250)
            return
        # Verif if component mode is edge
        just_the_selected_edges = cmds.filterExpand(sm=32)
        if just_the_selected_edges == None:
            ModIt_Global.WarningWindow("You should select 1 edge", 250)
            return
        else:
            if len(just_the_selected_edges) > 1:
                ModIt_Global.WarningWindow("You should select 1 edge only", 250)
                return



        # __________________________________________________________________________ 2 - FOUND BEVEL MODE


        # CHECK IF OPEN MESH AND IF SO STORE EDGES INFO
        mc.SelectVertexMask()
        mc.SelectToggleMode()
        mc.ConvertSelectionToEdgePerimeter()
        checkEdgesPerimt = mc.ls(sl=True)


        if checkEdgesPerimt == []:  # SO OBJET PLEIN
            # Verif if MIDDLE or one BORDER
            mc.select(edgeSelect)
            # GET VERTEXS
            mc.ConvertSelectionToVertices()
            vertexOrgerList = []
            for vertex in mc.ls(sl=1, fl=1):
                vertexOrgerList.append(vertex)

            # TEST VERTEX ONE
            vertexOne = vertexOrgerList[0]
            mc.select(vertexOne)
            mc.ConvertSelectionToEdges()

            if len(mc.ls(sl=True)) > 3:
                print("> BEVEL IN MIDDLE a")
                mc.select(edgeSelect)
                self.BevelVar_OnBothBorder()

            else:
                # TEST VERTEX TWO
                vertexTwo = vertexOrgerList[1]
                mc.select(vertexTwo)
                mc.ConvertSelectionToEdges()
                if len(mc.ls(sl=True)) > 3:
                    print("> > BEVEL IN MIDDLE b")
                    mc.select(edgeSelect)
                    self.BevelVar_OnBothBorder()
                else:
                    print("> BEVEL BORDER")
                    mc.select(edgeSelect)
                    self.BevelVar_OnBothBorder()


        else:
            ModIt_Global.WarningWindow("One side from the select edge is open which is not good topology for the tool", 500)
            return













































