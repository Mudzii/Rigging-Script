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


#  ================= Function to create twist joints =================================== #
#def CreateTwistJnt(jntList, jntRadius, jntName, prefix, prntJnt, nxtJnt, moveConst, Reparent):
def CreateTwistJnt(jntList, prefix, jntName, prntJnt, nxtJnt, jntRadius, moveConst, Reparent):
    
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
    ind = jntList.index(prntJnt)
    jntList.insert(ind + 1, twistJnt)

   


    # add jnts to list & create IK FK jnts    
    jntList.extend([clavicle, shoulder, elbow, wrist])
    
"""

............................

"""

#  ================= Function to create finger joints ================================== #
def CreateFinger(axis, prefix, jntList, wristJnt, wristPos, finger, pos, jntRadius):
    
    """
    newPos = [0,0,0] 
    if prefix == 'R_':
        newPos[0] = -0.2
        newPos[1] = -0.1
        newPos[2] = pos[2] * -1
        
    else:  
        newPos[0] = 0.2
        newPos[1] = 0.1
        newPos[2] = pos[2] 
    """     
    
    # create metacarpal jnt ==========
    FingerMeta = pm.joint(n = str(prefix) + str(finger) + '_finder_metacarpal_jnt', p = (0,0,0), rad = jntRadius)  
    pm.parent(FingerMeta, world = True)
    
    # temp parentconstr to move to pos
    tempConst = pm.parentConstraint(wristJnt, FingerMeta, mo = False)
    pm.delete(tempConst)
    
    pm.parent(FingerMeta, wristJnt)
    pm.move(FingerMeta, ((axis * pos[0]), pos[1], pos[2]), relative = True)
    
    """
    createControllers.CleanHist(FingerMeta)
    
    print axis
    print (axis * 0.5)
    
    # create finger jnts ============== 
    if finger is not 'thumb':
        
        Knuckle = pm.joint(n = str(prefix) + str(finger) + '_finger_knuckle_jnt', r = True, p = (0.4, -0.15, 0.05), rad = jntRadius)
    """
        #middle = pm.joint(n = str(prefix) + str(finger) + '_finder_middle_jnt', r = True, p = (0.3, 0.4, 0), rad = jntRadius)
        #tip = pm.joint(n = str(prefix) + str(finger) + '_finder_2_jnt', r = True, p = (axis * newPos[0],0,0), rad = jntRadius)
        #JointEnd = pm.joint(n = str(prefix) + str(finger) + '_finder_End_jnt', r = True, p = (axis * newPos[0],0,0), rad = jntRadius)
    
        # add jnts to list
        #jntList.extend([FingerMeta, Knuckle, middle, tip, JointEnd]) 
    
        # set orientations
        #pm.joint(FingerMeta, e=True, zso = True, oj='xyz', sao = 'yup')
        #pm.joint(Knuckle, e=True, zso = True, oj='xyz', sao = 'yup')
        #pm.joint(middle, e=True, zso = True, oj='xyz', sao = 'yup')
        #pm.joint(tip, e=True, zso = True, oj='xyz', sao = 'yup')
        #pm.joint(JointEnd, e=True, zso = True, oj='xyz', sao = 'yup')
        
    #if finger is 'thumb':
        #Knuckle = pm.joint(n = str(prefix) + str(finger) + '_finger_knuckle_jnt', r = True, p = (axis * newPos[0], 0,(axis * 0.25)), rad = jntRadius)
        #middle = pm.joint(n = str(prefix) + str(finger) + '_finder_middle_jnt', r = True, p = ((axis * newPos[1]),0,(axis * 0.15)), rad = jntRadius)
        #JointEnd = pm.joint(n = str(prefix) + str(finger) + '_finder_End_jnt', r = True, p = ((axis * newPos[1]),0,(axis * 0.15)), rad = jntRadius)
        
        # add jnts to list
        #jntList.extend([FingerMeta, Knuckle, middle, JointEnd]) 
    
        # set orientations
        #pm.joint(FingerMeta, e=True, zso = True, oj='xyz', sao = 'yup')
        #pm.joint(Knuckle, e=True, zso = True, oj='xyz', sao = 'yup')
        #pm.joint(Joint1, e=True, zso = True, oj='xyz', sao = 'yup')
        #pm.joint(JointEnd, e=True, oj='none', zso = True)
        

#  ================= Function to create hand joints ==================================== #
def CreateHand(prefix, axis, wristJnt, jntRadius):
    
    handJntList = []
    wristPos = cmds.xform(str(wristJnt), query=True, translation=True, worldSpace=True )

    
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'middle', (0.2, -0.01, 0.05), jntRadius)
    """ 
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'index', ((axis * 0.3), -0.06, 0.25), jntRadius)
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'ring', ((axis * 0.35), -0.06, -0.05), jntRadius)
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'pinky', ((axis * 0.4), -0.09, -0.2), jntRadius)
      
    CreateFinger(axis, prefix, handJntList, wristJnt, wristPos, 'thumb', ((axis * 0.15), -0.1, (axis * 0.3)), jntRadius)
    """
    return handJntList
    
    
    
    
    
