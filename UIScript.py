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
        
        """
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
        """
        
        
# ======================================================================================= # 
win = AutoRig()
win.show()        
        
