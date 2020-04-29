
# ====================================================================================== #
# ====================================================================================== #
import pymel.core as pm
import maya.cmds as cmds

import imp
import sys

path = r'D:\00.Documents\03. Scripting and Programming\Maya Scripts'
if path not in sys.path:
    sys.path.append(path)
    
    
import createControllers
import createJoints

    
# ====================================================================================== #
# ====================================================================================== #

#  ================= Function to create CTRLS ========================================== #
def IK_FKChain(jnList, IKJntList, FKJntList, ctrl_GRP):
    
    # create IK jnt chain =============
    IKChain = cmds.duplicate(str(jnList[1]), n= str(jnList[1] + '_IK'))[0]
    pm.parent(IKChain, world=True )
    createControllers.RecolourObj(IKChain, 'joint') 
    
    # rename jnts
    dagObjIK = pm.listRelatives(IKChain, ad=True, type="joint")
    for y in dagObjIK:
        pm.rename(y, str(y) + '_IK') 
        IKJntList.append(y) 
        createControllers.RecolourObj(y, 'joint') 
    
    # append jnt & rev list          
    IKJntList.append(IKChain) 
    IKJntList = IKJntList[::-1]
    
    
    #CreateIK(IKJntList,ctrl_GRP)
    
    # create FK jnt chain =============
    FKChain = cmds.duplicate(str(jnList[1]), n= str(jnList[1] + '_FK'))[0]
    pm.parent(FKChain, world=True )
    createControllers.RecolourObj(FKChain, 'joint') 
     
    # rename jnts
    dagObjFK = pm.listRelatives(FKChain, ad=True, type="joint") 
    for x in dagObjFK:
        pm.rename(x, str(x) + '_FK')
        FKJntList.append(x)
        createControllers.RecolourObj(x, 'joint') 
    
    # append jnt & rev list    
    FKJntList.append(FKChain)
    FKJntList = FKJntList[::-1]
    
    #CreateFK(FKJntList,ctrl_GRP)

#  ================= Function to create Arm ============================================ #
#def CreateArm(WS_LOC, spaceGrps, rigging_GRP, ctrl_GRP, skeleton_GRP, vis_aid_GRP, jntList, IKJntList, FKJntList, CTRLs, prefix, jntRadius):

def CreateArm(WS_LOC, space_Grps, rigging_GRPs, CTRLs_GRP, prefix, jntList, IKJntList, FKJntList, jntRadius):
    
    imp.reload(createControllers)
    imp.reload(createJoints)
    
    offset_GRP_Name = '_offset_GRP'
    axis = 1
    if prefix == 'R_':
        axis = -1
        
      
    # ===================== create simple arm jnts ===================== *
    clavicle = pm.joint(n = str(prefix) + 'clavicle_jnt', p = (axis * 0.4,0,0), rad = jntRadius)
    shoulder = pm.joint(n = str(prefix) + 'shoulder_jnt', p = (axis * 1.3,0.3,0.4), rad = jntRadius) 
    elbow = pm.joint(n = str(prefix) + 'elbow_jnt', p = (axis * 3,0,0), rad = jntRadius) 
 
    dist = createControllers.Distance(shoulder,elbow)
    wrist = pm.joint(n = str(prefix) + 'wrist_jnt', p = ( axis *(3 + dist),-0.1,0.4), rad = jntRadius) 
    pm.parent(clavicle, world=True) 

    # set jnt orientation
    pm.joint(clavicle, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(shoulder, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(elbow, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(wrist, e=True, zso = True, oj='none')

    # add jnts to list & create IK FK jnts    
    jntList.extend([clavicle, shoulder, elbow, wrist])
    
    #clavicle CTRL
    clavicle_Ctrl = str(prefix) + 'clavicle_CTRL'
    createControllers.CreateCircleCTRL(str(clavicle_Ctrl),CTRLs_GRP, clavicle, (0,1,0), 0.8, (0,0,80))   
    
    # ===================== create IK FK chain ========================= *
    IK_FKChain(jntList, IKJntList, FKJntList, CTRLs_GRP)
    
    #print CTRLs_GRP
 
    
# ====================================================================================== #    
# ====================================================================================== #    
#def CreateArm(WS_LOC, space_Grps, rigging_GRPs, CTRLs_GRP, prefix, jntList, IKJntList, FKJntList, jntRadius):
jntList = []
CTRL_List = []
IKJntList = []
FKJntList = []
jntRadius = 0.1

CreateArm('na', 'na', 'na', CTRL_List, 'L_', jntList, IKJntList, FKJntList, jntRadius)
    
