# ====================================================================================== #
# ====================================================================================== #
import pymel.core as pm
import maya.cmds as cmds

import imp
import sys

path = r'D:\00.Documents\03. Scripting and Programming\Maya Scripts'
if path not in sys.path:
    sys.path.append(path)
    
#import armRig

# Qt
try:
    import PySide2
    from PySide2 import QtWidgets, QtCore, QtGui
    from PySide2.QtUiTools import *
    from shiboken2 import wrapInstance
    
except ImportError:
    import PySide2
    from PySide import QtCore, QtGui
    from PySide2.QtUiTools import *
    from shiboken2 import wrapInstance 
    QtWidgets = QtGui
    
import logging

logging.basicConfig()
logger = logging.getLogger('AutoRig')
logger.setLevel(logging.INFO)
# ====================================================================================== #
# ====================================================================================== #

class AutoRig(QtWidgets.QMainWindow):
    # ================================ #
    def __init__(self):
        super(AutoRig, self).__init__()
        
        global windowName 
        windowName = 'AutoRig'
        
        # Delete window if it already exists
        if cmds.window(windowName, exists=True):
            self.CloseWindow(windowName)
        else:
            logger.debug('No previous UI exists')
            pass
            
        # Get Maya window and parent the controller to it
        mayaMainWindow = {o.objectName(): o for o in QtWidgets.qApp.topLevelWidgets()}["MayaWindow"]
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setWindowTitle('Auto Rig')
        self.setObjectName(windowName)
        self.resize(350, 400)
        self.primary_layout = QtWidgets.QVBoxLayout()
        
        self.BuildUI()
        self.raise_()
        
    # ================================ #  
    def CloseWindow(self, windowName):
        cmds.deleteUI(windowName)
        logger.debug('Deleted previous UI')
                       
    # ================================ #   
    def BuildUI(self):
        
        #mainLayout = QtWidgets.QGridLayout() 
        
        # Arm Rig Creation ========================================
                
        # Arm label
        textArm = QtWidgets.QLabel("Create Arm Rig", parent=self)
        textArm.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        textArm.setFixedHeight(50)
        textArm.setFixedWidth(250)
        textArm.move(5,10)
        textArm.setFont(QtGui.QFont('MS Sans Serif', 11, QtGui.QFont.Bold))

        # Check box L Arm
        create_L_ArmCkeckBox = QtWidgets.QCheckBox("Create Left Arm",parent=self)
        create_L_ArmCkeckBox.move(35,30)
        create_L_ArmCkeckBox.setFixedHeight(24)
        create_L_ArmCkeckBox.setFixedWidth(250)
        
        # Check box R Arm
        create_R_ArmCkeckBox = QtWidgets.QCheckBox("Create Right Arm",parent=self)
        create_R_ArmCkeckBox.move(35,50)
        create_R_ArmCkeckBox.setFixedHeight(24)
        create_R_ArmCkeckBox.setFixedWidth(250)
        
        # arm creation button 
        createArmButton = QtWidgets.QPushButton("Create Arm rig", parent=self)
        createArmButton.setFixedWidth(100)
        createArmButton.move(190,36)
        createArmButton.clicked.connect(lambda: self.CreateArms())
        
        # divider
        divider = QtWidgets.QFrame(parent=self)
        divider.setFrameShape(QtWidgets.QFrame.HLine)
        divider.setFixedWidth(340)
        divider.setLineWidth(2)
        divider.move(5,75)
        
        # Arm Prnt switch Creation ====================================
                
        # Arm label
        prntSwitchText = QtWidgets.QLabel("Create Parent Switch", parent=self)
        prntSwitchText.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        prntSwitchText.setFixedHeight(50)
        prntSwitchText.setFixedWidth(250)
        prntSwitchText.move(5,100)
        prntSwitchText.setFont(QtGui.QFont('MS Sans Serif', 11, QtGui.QFont.Bold))
        
        # add main ctrl =================
        
        # Arm label
        textMainCTRL = QtWidgets.QLabel("Main CTRL", parent=self)
        textMainCTRL.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        textMainCTRL.setFixedHeight(50)
        textMainCTRL.setFixedWidth(60)
        textMainCTRL.move(5,130)
        
        # 
        prntSwitchMain_CTRL = self.currentDirTxt = QtWidgets.QLineEdit(parent=self)
        prntSwitchMain_CTRL.setStyleSheet("border: 1px groove black; border-radius: 4px;")
        #prntSwitchAdd.returnPressed.connect(lambda: self.LoadMesh(col_mesh_view.text()))
        prntSwitchMain_CTRL.setFixedHeight(20)
        prntSwitchMain_CTRL.setFixedWidth(200)
        prntSwitchMain_CTRL.move(65,126)
        
        # arm creation button 
        addMainCtrl = QtWidgets.QPushButton("Select", parent=self)
        addMainCtrl.setFixedWidth(55)
        addMainCtrl.setFixedHeight(20)
        addMainCtrl.move(275,126)
        #addMainCtrl.clicked.connect(lambda: self.CreateArms())
        
        # add ctrl  =================
        
        # Arm label
        textAddCTRL = QtWidgets.QLabel("Add Switch CTRL", parent=self)
        textAddCTRL.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        textAddCTRL.setFixedHeight(50)
        textAddCTRL.setFixedWidth(100)
        textAddCTRL.move(5,160)
        
        prntSwitchAdd = self.currentDirTxt = QtWidgets.QLineEdit(parent=self)
        prntSwitchAdd.setStyleSheet("border: 1px groove black; border-radius: 4px;")
        #prntSwitchAdd.returnPressed.connect(lambda: self.LoadMesh(col_mesh_view.text()))
        prntSwitchAdd.setFixedHeight(20)
        prntSwitchAdd.setFixedWidth(170)
        prntSwitchAdd.move(95,155)
        
        # arm creation button 
        addSwitchCtrlBtn = QtWidgets.QPushButton("Add", parent=self)
        addSwitchCtrlBtn.setFixedWidth(55)
        addSwitchCtrlBtn.setFixedHeight(20)
        addSwitchCtrlBtn.move(275,155)
        
        # Switch CTRLS list =================
        
        # label
        textCTLRList = QtWidgets.QLabel("Added switch CTRLs:", parent=self)
        textCTLRList.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        textCTLRList.setFixedHeight(50)
        textCTLRList.setFixedWidth(240)
        textCTLRList.move(5,190)
        
        # list widget 
        switchCTRLList = QtWidgets.QListWidget(parent=self)
        
        switchCTRLList.move(5,210)
        switchCTRLList.setFixedWidth(240)
        switchCTRLList.setFixedHeight(120)
    
        switchCTRLList.insertItem(0, "Red")
        switchCTRLList.insertItem(0, "Blue")
        
        # Remove BTN
        removeSwitchCtrlBtn = QtWidgets.QPushButton("Remove Sel", parent=self)
        removeSwitchCtrlBtn.setFixedWidth(85)
        removeSwitchCtrlBtn.setFixedHeight(30)
        removeSwitchCtrlBtn.move(255,235)
        
        # Remove BTN
        removeAllSwitchCtrlBtn = QtWidgets.QPushButton("Remove All", parent=self)
        removeAllSwitchCtrlBtn.setFixedWidth(85)
        removeAllSwitchCtrlBtn.setFixedHeight(30)
        removeAllSwitchCtrlBtn.move(255,275)
        
        
        # switch CTRL creation button 
        createSwitchButton = QtWidgets.QPushButton("Create Parent Switch", parent=self)
        createSwitchButton.setFixedWidth(120)
        createSwitchButton.move(100,350)
        #createArmButton.clicked.connect(lambda: self.CreateArms())


    def CreateArms(self):
        print "CREATE ARMS"        
        
# ======================================================================================= # 
win = AutoRig()
win.show()        
        
