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
        create_L_ArmCkeckBox.move(15,30)
        create_L_ArmCkeckBox.setFixedHeight(24)
        create_L_ArmCkeckBox.setFixedWidth(250)
        
        # Check box R Arm
        create_R_ArmCkeckBox = QtWidgets.QCheckBox("Create Right Arm",parent=self)
        create_R_ArmCkeckBox.move(15,50)
        create_R_ArmCkeckBox.setFixedHeight(24)
        create_R_ArmCkeckBox.setFixedWidth(250)
        
        # arm creation button 
        createArmButton = QtWidgets.QPushButton("Create Arm rig", parent=self)
        createArmButton.setFixedWidth(100)
        createArmButton.move(125,90)
        createArmButton.clicked.connect(lambda: self.CreateArms())
        
        # Arm Prnt switch Creation ====================================
                
        # Arm label
        textArm = QtWidgets.QLabel("Create Parent Switch", parent=self)
        textArm.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        textArm.setFixedHeight(50)
        textArm.setFixedWidth(250)
        textArm.move(5,140)
        textArm.setFont(QtGui.QFont('MS Sans Serif', 11, QtGui.QFont.Bold))
        
        # add main ctrl =====
        
        # Arm label
        textArm = QtWidgets.QLabel("Main CTRL", parent=self)
        textArm.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)
        textArm.setFixedHeight(50)
        textArm.setFixedWidth(60)
        textArm.move(5,170)
        
        # 
        prntSwitchMain_CTRL = self.currentDirTxt = QtWidgets.QLineEdit(parent=self)
        prntSwitchMain_CTRL.setStyleSheet("border: 1px groove black; border-radius: 4px;")
        #prntSwitchAdd.returnPressed.connect(lambda: self.LoadMesh(col_mesh_view.text()))
        prntSwitchMain_CTRL.setFixedHeight(20)
        prntSwitchMain_CTRL.setFixedWidth(200)
        prntSwitchMain_CTRL.move(65,165)
        
        # arm creation button 
        addMainCtrl = QtWidgets.QPushButton("Select", parent=self)
        addMainCtrl.setFixedWidth(55)
        addMainCtrl.setFixedHeight(20)
        addMainCtrl.move(275,164)
        #addMainCtrl.clicked.connect(lambda: self.CreateArms())
        
        # add ctrl =====
        prntSwitchAdd = self.currentDirTxt = QtWidgets.QLineEdit(parent=self)
        prntSwitchAdd.setStyleSheet("border: 1px groove black; border-radius: 4px;")
        #prntSwitchAdd.returnPressed.connect(lambda: self.LoadMesh(col_mesh_view.text()))
        prntSwitchAdd.setFixedHeight(20)
        prntSwitchAdd.setFixedWidth(250)
        prntSwitchAdd.move(5,210)
        
        # 
        """
        listW = QtWidgets.QListWidget(parent=self)
        listW.setFixedWidth(340)
        listW.move(5,170)
        """


    def CreateArms(self):
        print "CREATE ARMS"        
        
# ======================================================================================= # 
win = AutoRig()
win.show()        
        
