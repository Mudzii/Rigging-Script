# ================================ #
# ================================ #
import pymel.core as pm
import maya.cmds as cmds

import sys

path = r'D:\00.Documents\03. Scripting and Programming\Maya Scripts'
if path not in sys.path:
    sys.path.append(path)
    
import createControllers
import createJoints
# ================================ #
# ================================ #


#  ================= Function to create Arm ============================================ #
#def CreateArm(WS_LOC, spaceGrps, rigging_GRP, ctrl_GRP, skeleton_GRP, vis_aid_GRP, jntList, IKJntList, FKJntList, CTRLs, prefix, jntRadius):

def CreateArm(WS_LOC, space_Grps, rigging_GRPs, CTRLs_GRP, prefix, jntList, IKJntList, FKJntList, jntRadius):

    axis = 1
    if prefix == 'R_':
        axis = -1
        
      
    # ===================== create simple arm jnts ===================== *
    clavicle = pm.joint(n = str(prefix) + 'clavicle_jnt', p = (axis * 0.4,0,0), rad = jntRadius)
    shoulder = pm.joint(n = str(prefix) + 'shoulder_jnt', p = (axis * 1.3,0.3,0.4), rad = jntRadius) 
    elbow = pm.joint(n = str(prefix) + 'elbow_jnt', p = (axis * 3,0,0), rad = jntRadius) 
 
    dist = Distance(shoulder,elbow)
    wrist = pm.joint(n = str(prefix) + 'wrist_jnt', p = ( axis *(3 + dist),-0.1,0.4), rad = jntRadius) 
    pm.parent(clavicle, world=True) 

    # set jnt orientation
    pm.joint(clavicle, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(shoulder, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(elbow, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(wrist, e=True, zso = True, oj='none')

    # add jnts to list & create IK FK jnts    
    jntList.extend([clavicle, shoulder, elbow, wrist])
    

jntList = []
IKJntList = []
FKJntList = []
jntRadius = 0.1

CreateArm('na', 'na', 'na', 'na', 'L_', jntList, IKJntList, FKJntList, jntRadius)
    
