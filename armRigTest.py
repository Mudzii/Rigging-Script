from math import pow,sqrt
import pymel.core as pm
import maya.cmds as cmds

jntList = []
del jntList[:]
side = 'L_'

IKJntList = []
del IKJntList[:]

FKJntList = []
del FKJntList[:]

# ================================ #
def Distance(objA, objB): 
    vecA = cmds.xform(str(objA), q=True, t=True, ws=True)
    vecB = cmds.xform(str(objB), q=True, t=True, ws=True)
	
    return sqrt(pow(vecA[0]-vecB[0],2)+pow(vecA[1]-vecB[1],2)+pow(vecA[2]-vecB[2],2))

# ================================ #
def CreateTwistJnt(jntRadius, jntName, side, prntJnt, nxtJnt, moveConst, Reparent):
    
    twistJnt = cmds.duplicate(str(prntJnt), n= str(side) + str(jntName), parentOnly=True)[0]
    pm.joint(twistJnt, e=True, rad = jntRadius)
    
    if moveConst is True:
        pm.parent(twistJnt, world=True )
        constr = pm.parentConstraint( prntJnt, nxtJnt, twistJnt, sr = ["x", "y", "z"], mo = False, w=1 )    
        pm.delete(constr)
      
    if Reparent is True:  
        pm.parent(twistJnt, prntJnt)
    
    ind = jntList.index(prntJnt)
    jntList.insert(ind + 1, twistJnt)


# ================================ # 

def DuplicateChain(jnList):
    
    IKshoulder = cmds.duplicate(str(jnList[1]), n= str(jnList[1] + '_IK'), parentOnly=True)[0]
    pm.parent(IKshoulder, world=True )
    
    IKelbow = cmds.duplicate(str(jnList[2]), n= str(jnList[2]) + '_IK', parentOnly=True)[0]
    pm.parent(IKelbow, IKshoulder)
    
    IKwrist = cmds.duplicate(str(jnList[3]), n= str(jnList[3] + '_IK'), parentOnly=True)[0]
    pm.parent(IKwrist, IKelbow)
    
    
    
    FKChain = cmds.duplicate(str(jnList[1]), n= str(jnList[1] + '_FK'))[0]
    pm.parent(FKChain, world=True )
    
    dagObj = pm.listRelatives(FKChain, ad=True, type="joint")
    for x in dagObj:
        print x
        name = x
        pm.rename(x, str(x) + '_FK')
    
# ================================ # 

def CreateArm(jntRadius):

    clavicle = pm.joint(n = str(side) + 'clavicle_jnt', p = (1,0,0), rad = jntRadius) 
    shoulder = pm.joint(n = str(side) + 'shoulder_jnt', p = (2,0.3,0.4), rad = jntRadius) 
    elbow = pm.joint(n = str(side) + 'elbow_jnt', p = (3.7,0,0), rad = jntRadius) 

    dist = Distance(shoulder,elbow)
    wrist = pm.joint(n = str(side) + 'wrist_jnt', p = ((3.7 + dist),-0.3,0.4), rad = jntRadius) 

    pm.joint(clavicle, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(shoulder, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(elbow, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(wrist, e=True, zso = True, oj='none')

    jntList.append(clavicle)
    jntList.append(shoulder)
    jntList.append(elbow)
    jntList.append(wrist)
    
    DuplicateChain(jntList)
    
    
    # create twist joints    
    twistJntRadius = jntRadius + 0.5
    CreateTwistJnt(twistJntRadius, 'shoulder_twist_jnt', side, shoulder, 'none', False, True)
    CreateTwistJnt(twistJntRadius, 'bicep_twist_jnt', side, shoulder, elbow, True, True)
    CreateTwistJnt(twistJntRadius, 'elbow_upper_twist_jnt', side, elbow, shoulder, False, False)
    CreateTwistJnt(twistJntRadius, 'elbow_twist_jnt', side, elbow, 'none', False, True)
    CreateTwistJnt(twistJntRadius, 'radius_twist_jnt', side, elbow, wrist, True, True)
    CreateTwistJnt(twistJntRadius, 'wrist_twist_jnt', side, wrist, elbow, False, False)


CreateArm(0.5)

print "____________________________________"    
for x in jntList:
    print x

