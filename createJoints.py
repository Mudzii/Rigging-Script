# ====================================================================================== #
# ====================================================================================== #
import pymel.core as pm
import maya.cmds as cmds
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

#  ================= Function to create IK/FK Chain =================================== #
