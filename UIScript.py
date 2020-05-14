# ====================================================================================== #
# ====================================================================================== #
import pymel.core as pm
import maya.cmds as cmds

import imp
import sys

path = r'D:\00.Documents\03. Scripting and Programming\Maya Scripts'
if path not in sys.path:
    sys.path.append(path)
    
import armRig

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

# logger    
import logging

logging.basicConfig()
logger = logging.getLogger('AutoRig')
logger.setLevel(logging.INFO)
# ====================================================================================== #
# ====================================================================================== #
global main_CTRL 
main_CTRL = ''

global switch_CTRL_List
switch_CTRL_List = []

global spaceGrps 
spaceGrps = []

global LOCinfo 
LOCinfo = []
# LISTS ==============================================
global arm_Jnt_List 
arm_Jnt_List = []
    
global arm_CTRL_List
arm_CTRL_List = []
    
global arm_IK_List
arm_IK_List = []
    
global arm_FK_List
arm_FK_List = []
    
global rigging_GRPs 
rigging_GRPs = []

# ====================================================================================== #

def CreateBasicGrps():
    
    # Rigging GRPS ======================================
    global rigging_GRPs 
    
    rigging_GRP = pm.group( em=True, name= 'rigging_GRP' )
    ctrl_GRP = pm.group( em=True, name= 'controllers_GRP' )
    skeleton_GRP = pm.group( em=True, name= 'skeleton_GRP' )
    vis_GRP= pm.group( em=True, name= 'vis_aid' )
    switch_GRP= pm.group( em=True, name= 'IKFK_Switch_GRP' )

    rigging_GRPs.extend([rigging_GRP, ctrl_GRP, skeleton_GRP, vis_GRP, switch_GRP])
    pm.parent(vis_GRP, rigging_GRP)
    
# ====================================================================================== #   
def CreateSpaceGrps(): 
   
    # Locator and spaces switch ========================
    global spaceGrps 
    
    world_LOC = pm.spaceLocator(n ='world_LOC')
    
    spaces_GRP = pm.group( em=True, name= 'spaces_GRP')
    world_GRP = pm.group( em=True, name= 'world_LOC_Space')
    
    spaceGrps.extend([spaces_GRP, world_GRP])
    
    pm.parent(world_GRP, spaces_GRP)
    LOCConst = pm.parentConstraint(world_LOC, world_GRP, mo = False, w=1)
    
    LOCinfo.extend([world_LOC, LOCConst])


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
        
        self.CleanLists()
           
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
        createArmButton.clicked.connect(lambda: self.CreateArms(create_L_ArmCkeckBox, create_R_ArmCkeckBox))
        
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

        addMainCtrl.clicked.connect(lambda: self.AddMainCtrl(prntSwitchMain_CTRL.text(), prntSwitchMain_CTRL))
        
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

        
        # add CTRL button 
        addSwitchCtrlBtn = QtWidgets.QPushButton("Add", parent=self)
        addSwitchCtrlBtn.setFixedWidth(55)
        addSwitchCtrlBtn.setFixedHeight(20)
        addSwitchCtrlBtn.move(275,155)
        
        addSwitchCtrlBtn.clicked.connect(lambda: self.AddCTRL(prntSwitchAdd.text(), switchCTRLList, prntSwitchAdd))
        
        # Remove SEL
        removeSwitchCtrlBtn = QtWidgets.QPushButton("Remove Sel", parent=self)
        removeSwitchCtrlBtn.setFixedWidth(85)
        removeSwitchCtrlBtn.setFixedHeight(30)
        removeSwitchCtrlBtn.move(255,235)
        
        removeSwitchCtrlBtn.clicked.connect(lambda: self.RemoveOBJ(switchCTRLList, False))
        
        
        # Remove BTN
        removeAllSwitchCtrlBtn = QtWidgets.QPushButton("Remove All", parent=self)
        removeAllSwitchCtrlBtn.setFixedWidth(85)
        removeAllSwitchCtrlBtn.setFixedHeight(30)
        removeAllSwitchCtrlBtn.move(255,275)
        
        removeAllSwitchCtrlBtn.clicked.connect(lambda: self.RemoveOBJ(switchCTRLList, True))
        

        # switch CTRL creation button 
        createSwitchButton = QtWidgets.QPushButton("Create Parent Switch", parent=self)
        createSwitchButton.setFixedWidth(120)
        createSwitchButton.move(100,350)
        
        createSwitchButton.clicked.connect(lambda: self.CreateParentSwitch(prntSwitchMain_CTRL, switchCTRLList))
   
    # ================================ #  
    def CleanLists(self):
        
        main_CTRL = ''
        
        del rigging_GRPs[:]
        
        del arm_Jnt_List[:]
        
        del arm_CTRL_List[:]
    
        del arm_IK_List[:]
        
        del arm_FK_List[:]
        
        del switch_CTRL_List[:]
        
        del spaceGrps[:]
        
        del LOCinfo[:]
        
    # ================================ # 
    def RemoveOBJ(self, ListItems, all):
        
        if all == False:
            selectedItem = ListItems.selectedItems()
            currentRow = ListItems.currentRow()
            ListItems.takeItem(currentRow)

            
        elif all == True: 
            ListItems.clear()
            
    # ================================ #         
    def CreateParentSwitch(self, m_CTRL, ctrl_List):   
        
        print
        print "Create Parent switch"
        
        global switch_CTRL_List
        global LOCinfo
        
        global main_CTRL
        global arm_CTRL_List
        global spaceGrps
        
        print LOCinfo
        
        itemCount = ctrl_List.count()
        for i in range(itemCount):
            switch_CTRL_List.append(ctrl_List.item(i).text())
        
        #armRig.CreateSpaceSwitch(spaceGrps, LOCinfo[0], LOCinfo[1], str(main_CTRL), switch_CTRL_List, arm_CTRL_List)
        
    # ================================ #  
    def AddMainCtrl(self, Switch_CTRL_name, qMainCtrlBox):
        
        if len(Switch_CTRL_name) > 0:

            shapes = cmds.listRelatives(str(Switch_CTRL_name))  
            print shapes  
            if len(shapes) > 0: 
                if pm.objectType(shapes[0], isType='nurbsCurve'):
                    
                    splitString = Switch_CTRL_name.split('|', 3)
            
                    global main_CTRL 
                    main_CTRL = splitString[3]
                    
                    qMainCtrlBox.setText(main_CTRL) 

    # ================================ #         
    def AddCTRL(self, CTRL_name, qList, qCtrlBox):       
        
        global main_CTRL 

        if len(CTRL_name) > 0:
            shapes = cmds.listRelatives(str(CTRL_name))  

            if len(shapes) > 0: 
            
                if pm.objectType(shapes[0], isType='locator'):
                    space_CTRL = ''
                    splitString = CTRL_name.split('|', 3)
                    
                    space_CTRL = splitString[1]
                    
                    if str(space_CTRL) != str(main_CTRL):
                        findItem = qList.findItems(space_CTRL,8) 
                        if len(findItem) <= 0:
                            qList.addItem(space_CTRL)
                    
                if pm.objectType(shapes[0], isType='nurbsCurve'):
                    
                    space_CTRL = ''
                    splitString = CTRL_name.split('|', 3)
                    
                    length = len(splitString)
                    space_CTRL = splitString[length - 1] 

                    if str(space_CTRL) != str(main_CTRL):
                        findItem = qList.findItems(space_CTRL,8) 
                        if len(findItem) <= 0:
                            qList.addItem(space_CTRL)
        qCtrlBox.clear()
                            
                       
    # ================================ #  
    def CreateArms(self, L_ArmCkeckBox, R_ArmCkeckBox):
        
        global rigging_GRPs
        global spaceGrps 
         
        global arm_Jnt_List 
        global arm_CTRL_List
        
        global arm_IK_List
        global arm_FK_List
            
        # create Basic rigging grps if not present
        if len(rigging_GRPs) <= 0:
            CreateBasicGrps()
        
        if len(spaceGrps) <= 0:
            CreateSpaceGrps()   
             
        jntRadius = 0.1       
        relatives = pm.listRelatives(rigging_GRPs)
        
        # create L Arm
        if L_ArmCkeckBox. isChecked() == True: 
            if 'L_arm_GRP' not in relatives:
                L_jntList = []
                L_CTRL_List = []
                L_IKJntList = []
                L_FKJntList = []
                
                armRig.CreateArm(rigging_GRPs, L_CTRL_List, 'L_', L_jntList, L_IKJntList, L_FKJntList, jntRadius)
                
                arm_Jnt_List = arm_Jnt_List + L_jntList
                arm_IK_List = arm_IK_List + L_IKJntList
                arm_FK_List = arm_FK_List + L_FKJntList
                
                arm_CTRL_List = arm_CTRL_List + L_CTRL_List
                
                
        # create R Arm    
        if R_ArmCkeckBox. isChecked() == True: 
            if 'R_arm_GRP' not in relatives:
                R_jntList = []
                R_CTRL_List = []
                R_IKJntList = []
                R_FKJntList = []
                
                armRig.CreateArm(rigging_GRPs, R_CTRL_List, 'R_', R_jntList, R_IKJntList, R_FKJntList, jntRadius)     
                
                arm_Jnt_List = arm_Jnt_List + R_jntList
                arm_IK_List = arm_IK_List + R_IKJntList
                arm_FK_List = arm_FK_List + R_FKJntList
                
                arm_CTRL_List = arm_CTRL_List + R_CTRL_List

        
# ======================================================================================= # 
win = AutoRig()
win.show()        
        
