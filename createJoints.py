# ====================================================================================== #
# ====================================================================================== #
import pymel.core as pm
import maya.cmds as cmds

import sys

path = r'D:\00.Documents\03. Scripting and Programming\Maya Scripts'
if path not in sys.path:
    sys.path.append(path)
    
    
import createControllers

# ====================================================================================== #
# ====================================================================================== #
def CreateArmTwistJnts(prefix, jntList, jntRadius):
    
    twistJntList = []
    twistJntRadius = jntRadius + 0.1
    
    CreateTwistJnt(prefix, twistJntList, 'shoulder_twist_jnt', jntList[1], 'none', twistJntRadius, False, True)
    CreateTwistJnt(prefix, twistJntList, 'bicep_twist_jnt', jntList[1], jntList[2], twistJntRadius, True, True)
    
    CreateTwistJnt(prefix, twistJntList, 'elbow_upper_twist_jnt', jntList[2], jntList[1], twistJntRadius, False, False)
    CreateTwistJnt(prefix, twistJntList, 'elbow_twist_jnt', jntList[2], 'none', twistJntRadius, False, True)
    
    CreateTwistJnt(prefix, twistJntList, 'radius_twist_jnt', jntList[2], jntList[3], twistJntRadius, True, True)
    CreateTwistJnt(prefix, twistJntList, 'wrist_twist_jnt', jntList[3], jntList[2], twistJntRadius, False, False)
    
    return twistJntList
    
#  ================= Function to create twist joints =================================== #
#def CreateTwistJnt(jntList, jntRadius, jntName, prefix, prntJnt, nxtJnt, moveConst, Reparent):
def CreateTwistJnt(prefix, jntList, jntName, prntJnt, nxtJnt, jntRadius, moveConst, Reparent):
    
    twistJnt = cmds.duplicate(str(prntJnt), n= str(prefix) + str(jntName), parentOnly=True)[0]
    pm.joint(twistJnt, e=True, rad = jntRadius)
    
    # move jnt between 2 jnts 
    if moveConst is True:
        pm.parent(twistJnt, world=True )
        constr = pm.parentConstraint( prntJnt, nxtJnt, twistJnt, sr = ["x", "y", "z"], mo = False, w=1 )    
        pm.delete(constr)
    
    # reparent jnts   
    if Reparent is True:  
        pm.parent(twistJnt, prntJnt)
    
    # add new jnt to list
    #ind = jntList.index(prntJnt)
    #jntList.insert(ind + 1, twistJnt)

    # add jnts to list 
    jntList.append(twistJnt)
    

#  ================= Function to create finger joints ================================== #
def CreateFinger(axis, prefix, jntList, wristJnt, wristPos, finger, pos, jntRadius):
    
    
    # create metacarpal jnt ==========
    FingerMeta = pm.joint(n = str(prefix) + str(finger) + '_finger_metacarpal_jnt', p = (0,0,0), rad = jntRadius)  
    pm.parent(FingerMeta, world = True)
    
    # temp parentconstr to move to pos
    tempConst = pm.parentConstraint(wristJnt, FingerMeta, mo = False)
    pm.delete(tempConst)
    
    pm.parent(FingerMeta, wristJnt)
    pm.move(FingerMeta, ((axis * pos[0]), pos[1], pos[2]), relative = True)
    createControllers.CleanHist(FingerMeta)
    
    
    # create finger jnts ============== 
    if finger is not 'thumb':
        
        Knuckle = pm.joint(n = str(prefix) + str(finger) + '_finger_knuckle_jnt', r = True, p = (0.4, -0.005,0), rad = jntRadius)
        middle = pm.joint(n = str(prefix) + str(finger) + '_finger_middle_jnt', r = True, p = (0.4, -0.001,0), rad = jntRadius)
        tip = pm.joint(n = str(prefix) + str(finger) + '_finger_tip_jnt', r = True, p = (0.3, -0.001, 0), rad = jntRadius)
        JointEnd = pm.joint(n = str(prefix) + str(finger) + '_finger_End_jnt', r = True, p = (0.25, -0.001, 0), rad = jntRadius)
    
        # add jnts to list
        jntList.extend([FingerMeta, Knuckle, middle, tip, JointEnd]) 
    
        # set orientations
        pm.joint(FingerMeta, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(Knuckle, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(middle, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(tip, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(JointEnd, e=True, zso = True, oj='xyz', sao = 'yup')
        
    if finger is 'thumb':
        Knuckle = pm.joint(n = str(prefix) + str(finger) + '_finger_knuckle_jnt', r = True, p = (0.15, 0.01, (axis * 0.2)), rad = jntRadius)
        middle = pm.joint(n = str(prefix) + str(finger) + '_finger_middle_jnt', r = True, p = (0.2, -0.02,(axis * 0.12)), rad = jntRadius)
        JointEnd = pm.joint(n = str(prefix) + str(finger) + '_finger_End_jnt', r = True, p = (0.15, 0.01 ,(axis * 0.05)), rad = jntRadius)
        
        # add jnts to list
        jntList.extend([FingerMeta, Knuckle, middle, JointEnd]) 
    
        # set orientations
        pm.joint(FingerMeta, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(Knuckle, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(middle, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(JointEnd, e=True, oj='none', zso = True)
        

#  ================= Function to create hand joints ==================================== #
def CreateHand(prefix, axis, wristJnt, jntRadius):
    
    handJntList = []
    wristPos = cmds.xform(str(wristJnt), query=True, translation=True, worldSpace=True )

    
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'middle', (0.25, -0.01, 0.05), jntRadius)
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'index', (0.2, -0.02, 0.2), jntRadius)
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'ring', (0.25, -0.01, -0.1), jntRadius)
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'pinky', (0.26, -0.03, -0.25), jntRadius)
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'thumb', (0.1, -0.05, 0.25), jntRadius)
   
    return handJntList
