# ======================================================================================= #
# ================================= IMPORTS ============================================= #
# ======================================================================================= #
import pymel.core as pm
import maya.cmds as cmds
#import os
#from os.path import dirname
#from glob import glob
#from maya import OpenMayaUI as omui
from math import pow,sqrt

import sys

path = r'D:\00.Documents\03. Scripting and Programming\Maya Scripts'
if path not in sys.path:
    sys.path.append(path)

import armRigTest 

"""
jointList = []
IKjointList = []
FKjointList = []
CTRLs = []


armRigTest.CreateArm(jointList, IKjointList, FKjointList, CTRLs, 'L_', 0.1)
"""


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

# ======================================================================================= #
# ======================================================================================= #
# ======================================================================================= #

# ======================================================================================= #
# ======================================================================================= #

class RiggingScript(QtWidgets.QMainWindow):
    
    # ================================ # 
    def __init__(self):
        super(RiggingScript, self).__init__()
      
        global windowName 
        windowName = 'RiggingScript'
        
    
        # Delete if exists
        if cmds.window(windowName, exists=True):
            self.CloseWindow(windowName)
            
        else:
            pm.warning('No previous UI exists')  
            pass
            
        
        # Get Maya window and parent the controller to it
        mayaMainWindow = {o.objectName(): o for o in QtWidgets.qApp.topLevelWidgets()}["MayaWindow"]
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setWindowTitle('Rigging Script')
        self.setObjectName(windowName)
        self.resize(350, 500)
        
        # function that builds UI layout + buttons
        self.BuildUI()
            
    # ================================ #   
    def BuildUI(self):
        
        # Main widget
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)
        
        # Layout
        lot = QtWidgets.QGridLayout()
        widget.setLayout(lot)
                
    # ================================ #        
    def CloseWindow(self, winName):
        cmds.deleteUI(winName)

      
    #def CreateArm():
                        
    """              
        # Get Maya window and parent the controller to it
        mayaMainWindow = {o.objectName(): o for o in QtWidgets.qApp.topLevelWidgets()}["MayaWindow"]
        self.setParent(mayaMainWindow)
        self.setWindowFlags(QtCore.Qt.Window)

        self.setWindowTitle('NURB collision rig')
        self.setObjectName(windowName)
        self.resize(400, 150)

        self.BuildUI()
        
    # ================================ #  
    def CloseWindow(self, windowName):
        cmds.deleteUI(windowName)
        logger.debug('Deleted previous UI')
                       
    # ================================ #   
    def BuildUI(self):
        
        # Main widget
        widget = QtWidgets.QWidget(self)
        self.setCentralWidget(widget)
        
        # Layout
        lot = QtWidgets.QGridLayout()
        widget.setLayout(lot)
        
        # collision mesh viewer
        global col_mesh_view
        col_mesh_view = self.currentDirTxt = QtWidgets.QLineEdit()
        col_mesh_view.setStyleSheet("border: 1px groove black; border-radius: 4px;")
        col_mesh_view.returnPressed.connect(lambda: self.LoadMesh(col_mesh_view.text()))
        lot.addWidget(self.currentDirTxt,0,0,1,10,0)
        
        # load mesh button  
        loadMeshButton = QtWidgets.QPushButton()
        loadMeshButton.setText("Load Mesh")
        loadMeshButton.clicked.connect(lambda: self.LoadMesh(col_mesh_view.text()))
        lot.addWidget(loadMeshButton,0,10,1,1,0)   
        
        # nurb mesh viewer
        global nurb_mesh_view
        nurb_mesh_view = self.currentDirTxt = QtWidgets.QLineEdit()
        nurb_mesh_view.setStyleSheet("border: 1px groove black; border-radius: 4px;")
        nurb_mesh_view.returnPressed.connect(lambda: self.LoadNurb(nurb_mesh_view.text()))
        lot.addWidget(self.currentDirTxt,1,0,1,10,0)
        
        # load nurb button  
        loadNURBButton = QtWidgets.QPushButton()
        loadNURBButton.setText("Load Nurb")
        loadNURBButton.clicked.connect(lambda: self.LoadNurb(nurb_mesh_view.text()))
        lot.addWidget(loadNURBButton,1,10,1,1,0) 
        
        # create button  
        createButton = QtWidgets.QPushButton()
        createButton.setText("Create NURB collision rig")
        createButton.clicked.connect(lambda: self.CreateCurve())
        lot.addWidget(createButton,2,0,1,11,0) 
        
    # ================================ #
    def LoadMesh(self, meshName):
        
        if len(meshName) > 0:
            pm.select(meshName)
            
            #check if added shape is a mesh
            shapes = cmds.listRelatives(str(meshName))            
            if pm.objectType(shapes, isType='mesh'):
            
                global collision_mesh
                collision_mesh = pm.ls( selection=True )[0] 
                
            else:
                pm.warning('Please select a mesh instead')  
        
    # ================================ #        
    def LoadNurb(self, nurbName):
        
        if len(nurbName) > 0:
            pm.select(nurbName)
            
            #check if added shape is a NURB
            shapes = cmds.listRelatives(str(nurbName))        
            if pm.objectType(shapes, isType='nurbsCurve'):
            
                global NURB
                NURB = pm.ls( selection=True )[0] 
                
            else:
                pm.warning('Please select a nurb curve instead')    
    
    # ================================ # 
    def CreateCurve(self):
        
        global NURB        
        global clusters        
        global collision_mesh   
        
        # try loading nurb if not loaded
        if not NURB:
            global nurb_mesh_view
            if nurb_mesh_view.text() > 0:
                self.LoadNurb(nurb_mesh_view.text())
        
        # try loading mesh if not loaded
        if not collision_mesh:
            global col_mesh_view
            if col_mesh_view.text() > 0:
                self.LoadMesh(col_mesh_view.text())
        
        
        # if NURB and mesh loaded            
        if NURB and collision_mesh:

            #make mesh muscle object
            pm.select(collision_mesh )
            mel.eval('cMuscle_makeMuscle(0);')
            
            # del history and freeze transforms
            CleanObj(NURB)
            CleanObj(collision_mesh)
            
            # get points on NURB curve
            numCVs = NURB.numCVs()
            curveCVs = cmds.ls('{0}.cv[:]'.format(NURB), fl = True)
            
            # if points found, create stuff
            if curveCVs:
                
                # create clusters and keepout                     
                CLSTRgrp = pm.group( em = True, name = str(NURB) + '_cluster_GRP' )
                CreateClusters(curveCVs, CLSTRgrp)
                ClusterToKeepOut(clusters)
                ConnectKeepOut()
                
                # create joint setup
                JNTgrp = pm.group( em = True, name = str(NURB) + '_rig_GRP' )
                JointSetup(JNTgrp, numCVs, curveCVs)
                
                global windowName
                self.CloseWindow(windowName)
            
     """       
 
    

# ======================================================================================= # 
win = RiggingScript()
win.show() 



