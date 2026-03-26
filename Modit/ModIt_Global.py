##GLOBAL VARIABLEs
from PySide6 import QtWidgets, QtCore, QtGui
from maya import cmds as mc
import maya.mel as mel
import json
from .Qt import QtWidgets, QtCore, QtCompat
import os
import maya.cmds as cmds
from maya import OpenMayaUI as omui

from shiboken6 import wrapInstance
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget

from . import ModIt_CSS


##_____________________________________________PATH
USERAPPDIR = mc.internalVar(userAppDir=True)
VERSION = mc.about(v=True)
IconsPathThemeClassic = os.path.join(USERAPPDIR, VERSION+'/scripts/ModIt/Icons/Theme_Classic/')
ToolPath = os.path.join(USERAPPDIR, VERSION+'/scripts/ModIt/Tools/')
PreferencePath = os.path.join(USERAPPDIR, VERSION+'/scripts/ModIt/Preferences/')
PlugInsPath = os.path.join(USERAPPDIR, VERSION+'/plug-ins')
PrefIcons = os.path.join(USERAPPDIR, VERSION+'/prefs/icons')
UserScriptFolder = os.path.join(USERAPPDIR, VERSION+'/scripts')
RessourcePath = os.path.join(USERAPPDIR, VERSION+'/scripts/ModIt/Ressources/')



##_____________________________________________PREFERENCES
ModItTitle = "ModIt 3.0"


##_____________________________________________UI
#_____________#Theme
Theme_pref = json.load(open(PreferencePath + 'Pref_Theme.json', "r"))
PREF_THEME = (Theme_pref['THEME'])

if PREF_THEME == 0:
    Theme = ModIt_CSS.ModIt_CSS
    IconPath = IconsPathThemeClassic
elif PREF_THEME == 1:
    Theme = ModIt_CSS.Maya_CSS
    IconPath = IconsPathThemeClassic

#_____________#IconSize
IconSize_pref = json.load(open(PreferencePath + 'Pref_IconSize.json', "r"))
PREF_ICONSIZE = (IconSize_pref['ICONSIZE'])

IconButtonSize = PREF_ICONSIZE

# ******************************************
#           BUTTONS PARAMS
# ******************************************
iconFixeSize = 30
iconButtonSize = 30
separatorWidth = 1


##_____________________________________________WARNING POP UP
def WarningWindow(message, size, *args):
    BackgroundColor = 0.16
    # ________________//
    if mc.window("WarningWindow", exists=True):
        mc.deleteUI("WarningWindow")
    mc.window("WarningWindow", title=' Warning ', s=False, vis=True, rtf=False)
    mc.columnLayout(adj=True, rs=3, bgc=[BackgroundColor, BackgroundColor, BackgroundColor])
    mc.separator(h=8, style='none')
    mc.text(l="  " + message + "  ", al="center")
    mc.separator(h=8, style='none')
    mc.button(l="OK", c=WarningOKButton)
    mc.window("WarningWindow", e=True, wh=(size, 80))

    qw = omui.MQtUtil.findWindow("WarningWindow")
    widget = wrapInstance(int(qw), QWidget)
    icon = QIcon(IconPath + "Windows_Ico_Warning.png")
    widget.setWindowIcon(icon)

    mc.showWindow()

def WarningOKButton(*args):
    mc.deleteUI("WarningWindow")



def LoadingWindow(message, size, *args):
    BackgroundColor = 0.110
    # ________________//
    if mc.window("LoadingWindow", exists=True):
        mc.deleteUI("LoadingWindow")
    mc.window("LoadingWindow", title='Loading Asset', s=False, vis=True, rtf=False)
    mc.columnLayout(adj=True, rs=3, bgc=[BackgroundColor, BackgroundColor, BackgroundColor])
    mc.separator(h=5, style='none')
    mc.text(l=" " + message + " ", al="center")
    mc.iconTextButton(image1= IconPath + "Refresh_Button.png")
    mc.window("LoadingWindow", e=True, wh=(size, 70))

    qw = omui.MQtUtil.findWindow("LoadingWindow")
    widget = wrapInstance(int(qw), QWidget)
    icon = QIcon(IconPath + "Windows_Ico2.png")
    widget.setWindowIcon(icon)

    mc.showWindow()

















