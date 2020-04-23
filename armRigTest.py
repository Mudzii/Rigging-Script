# ================================ #
# ================================ #
from math import pow,sqrt
import pymel.core as pm
import maya.cmds as cmds
# ================================ #
# ================================ #

#jntList = []
#del jntList[:]

#IKJntList = []
#del IKJntList[:]

#FKJntList = []
#del FKJntList[:]

# ================================ #
def CleanHist(obj):
    pm.delete(obj , ch = 1)
    pm.makeIdentity(obj, apply = True )
    
# ================================ #
def Distance(objA, objB): 
    vecA = cmds.xform(str(objA), q=True, t=True, ws=True)
    vecB = cmds.xform(str(objB), q=True, t=True, ws=True)
	
    return sqrt(pow(vecA[0]-vecB[0],2)+pow(vecA[1]-vecB[1],2)+pow(vecA[2]-vecB[2],2))
    
# ================================ #
def RecolourObj(obj):
    
    pm.setAttr(str(obj) + '.overrideEnabled', 1)
    pm.setAttr(str(obj) + '.overrideRGBColors', 1)
    
    rel = pm.listRelatives(obj)
    
    # if IK/FK joint
    if pm.objectType( str(obj), isType= 'joint' ):
        if obj[-2] == 'I':
            pm.setAttr(str(obj) + '.overrideColorRGB', 0, 1, 0)
            
        elif obj[-2] == 'F':
            pm.setAttr(str(obj) + '.overrideColorRGB', 1, 0, 1)       
    
    # if CTRL
    elif pm.objectType( str(rel[0]), isType= 'nurbsCurve' ):
        if obj[0] == 'L':
            pm.setAttr(str(obj) + '.overrideColorRGB', 1, 0, 0)
        elif obj[0] == 'R':
            pm.setAttr(str(obj) + '.overrideColorRGB', 0, 0, 1)       
        else: 
            pm.setAttr(str(obj) + '.overrideColorRGB', 1, 1, 0) 
            
    
        
# ================================ #
def ReparentShape(nurbCTRL, parentCTRL):
    ctrlName = str(nurbCTRL[0])

    shapes = pm.listRelatives(ctrlName)
    shape = shapes[0]
 
    pm.parent(shape,parentCTRL[0], relative = True, shape= True)
    pm.delete(ctrlName)
    
# ================================ # 
def CreateStarCTRL(CTRL_name, rad, scle, norm):
    
    nurbCTRL = cmds.circle( n = str(CTRL_name), nr =norm, c=(0, 0, 0), r= rad )
    
    curveCVs = cmds.ls('{0}.cv[:]'.format(CTRL_name), fl = True)
    selList = [curveCVs[0], curveCVs[2], curveCVs[4], curveCVs[6]]
    
    sel = pm.select(selList)
    pm.scale(sel, scle)
    
    CleanHist(nurbCTRL[0])
    
    offset_GRP = pm.group( em=True, name= str(CTRL_name) + '_offset_GRP' )
    pm.parent(nurbCTRL[0], offset_GRP)
    
    RecolourObj(CTRL_name)
 
# ================================ #    
def CreateBallCTRL(CTRL_name, rad):
    
    nurbCTRL = cmds.circle( n = str(CTRL_name), nr =(1,0,0), c=(0, 0, 0), r= rad )
    nurbCTRL1 = cmds.circle( n = str('circle1'), nr =(0,0,1), c=(0, 0, 0), r= rad )
    nurbCTRL2 = cmds.circle( n = str('circle2'), nr =(0,1,0), c=(0, 0, 0), r= rad )

    nurbCTRL3 = cmds.circle( n = str('circle3'), nr =(1,0,0), c=(0, 0, 0), r= rad )
    pm.rotate(nurbCTRL3, [0,0,45])

    nurbCTRL4 = cmds.circle( n = str('circle4'), nr =(1,0,0), c=(0, 0, 0), r= rad )
    pm.rotate(nurbCTRL4, [0,0,-45])

    CleanHist(nurbCTRL[0])
    CleanHist(nurbCTRL1[0])
    CleanHist(nurbCTRL2[0])
    CleanHist(nurbCTRL3[0])
    CleanHist(nurbCTRL4[0])

    ReparentShape(nurbCTRL4, nurbCTRL)
    ReparentShape(nurbCTRL3, nurbCTRL)
    ReparentShape(nurbCTRL2, nurbCTRL)    
    ReparentShape(nurbCTRL1, nurbCTRL)    

    CleanHist(nurbCTRL[0])
    offset_GRP = pm.group( em=True, name= str(CTRL_name) + '_offset_GRP' )
    #pm.parent(nurbCTRL[0], offset_GRP)
    
    RecolourObj(CTRL_name)
    
# ================================ #   
def CreateCircleCTRL(CTRL_name, prntJnt, norm, rad, offset):
    
    CTRL = cmds.circle( n = str(CTRL_name), nr = norm, c=(0, 0, 0), r= rad )
    offset_GRP = pm.group( em=True, name= str(CTRL_name) + '_offset_GRP' )
    pm.parent(CTRL[0], offset_GRP) 
    
    CleanHist(CTRL[0])
    CleanHist(offset_GRP)
    
    tempConst = pm.parentConstraint(prntJnt, str(offset_GRP), mo = False)
    pm.delete(tempConst)
    
    curveCVs = cmds.ls('{0}.cv[:]'.format(CTRL[0]), fl = True)
    pm.rotate(curveCVs, offset)
    
    pm.parentConstraint(str(CTRL_name), str(prntJnt), mo= False, w=1)
    
    RecolourObj(CTRL_name)
    
        
# ================================ #
def CreateTwistJnt(jntList, jntRadius, jntName, prefix, prntJnt, nxtJnt, moveConst, Reparent):
    
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


# ================================ # 
def CreateIK(jntIKList):
    
    prefix = str(jntIKList[0][0:2])
    
    # create arm CTRL
    Arm_CTRL = str(prefix) + "arm_IK_CTRL"
    CreateStarCTRL(Arm_CTRL, 0.6, [0.4, 0.4, 0.4], (1,0,0))
    
    # move offset GRP to wrist jnt, remove const
    tempConst = pm.parentConstraint(jntIKList[2], str(Arm_CTRL) + '_offset_GRP')
    pm.delete(tempConst)

    # create IK handle 
    arm_ik = pm.ikHandle( n = str(prefix) + 'IK_Handle', sj=jntIKList[0], ee=jntIKList[2])
    pm.parent(arm_ik[0],Arm_CTRL)
    
    
    # create pole vector CTRL
    poleVector_CTRL = str(prefix) + 'pole_vector'
    pole_GRP = str(poleVector_CTRL) + '_offset_GRP'
    CreateBallCTRL(str(poleVector_CTRL), 0.15)
    
    # move offset GRP to wrist jnt, remove const
    tempConst = pm.parentConstraint(jntIKList[1], str(pole_GRP), sr = ['x', 'y', 'z'])
    pm.delete(tempConst)
    CleanHist(pole_GRP)    
    
    # point + aim constraint CTRL to prevent joint from moving after pole V Constr
    pointConst = pm.pointConstraint( str(jntIKList[0]), str(jntIKList[2]), str(poleVector_CTRL), mo= False, w=1 )
    pm.delete(pointConst)
    
    aimConst = pm.aimConstraint( str(jntIKList[1]), str(poleVector_CTRL), mo= False, w=1 )
    pm.delete(aimConst)
    
    # constrain PV
    PVConstr = pm.poleVectorConstraint(poleVector_CTRL, arm_ik[0], n = str(poleVector_CTRL) + '_constraint')
    pm.move(str(poleVector_CTRL), (1,0, 0 ), os = True, wd = False, relative = True)
    
    CleanHist(poleVector_CTRL)   
    pm.parent(poleVector_CTRL, pole_GRP) 
    
    for x in jntIKList:
        RecolourObj(x)
    
    
# ================================ # 
def CreateFK(jntFKList):

    prefix = str(jntFKList[0][0:2])
    
    # shoulder CTRL
    shoulder_CTR_Name = str(prefix) + 'shoulder_FK_CTRL'  
    CreateCircleCTRL(str(shoulder_CTR_Name), jntFKList[0], (0,1,0), 0.6, (0,0,-100))
    
    # elbow CTRL
    elbow_CTR_Name = str(prefix) + 'elbow_FK_CTRL'  
    CreateCircleCTRL(str(elbow_CTR_Name), jntFKList[1], (0,1,0), 0.5, (0,0,-100))
    
    # wrist CTRL
    wrist_CTR_Name = str(prefix) + 'wrist_FK_CTRL'  
    CreateCircleCTRL(str(wrist_CTR_Name), jntFKList[2], (0,1,0), 0.3, (0,0,-100))
    
    pm.parent(str(wrist_CTR_Name) + '_offset_GRP', elbow_CTR_Name)
    pm.parent(str(elbow_CTR_Name) + '_offset_GRP', shoulder_CTR_Name)
    
    for x in jntFKList:
        RecolourObj(x)
            
# ================================ # 

def IK_FKChain(jnList, IKJntList, FKJntList):
    
    
    # create IK jnt chain
    IKChain = cmds.duplicate(str(jnList[1]), n= str(jnList[1] + '_IK'))[0]
    pm.parent(IKChain, world=True )
     
    # create FK jnt chain
    FKChain = cmds.duplicate(str(jnList[1]), n= str(jnList[1] + '_FK'))[0]
    pm.parent(FKChain, world=True )
     
    # rename chains
    dagObjFK = pm.listRelatives(FKChain, ad=True, type="joint")
    dagObjIK = pm.listRelatives(IKChain, ad=True, type="joint")
    
    for x in dagObjFK:
        pm.rename(x, str(x) + '_FK')
        FKJntList.append(x)
        
    for y in dagObjIK:
        pm.rename(y, str(y) + '_IK') 
        IKJntList.append(y)   
        
    IKJntList.append(IKChain)
    FKJntList.append(FKChain)
    
    # reverse order of list  
    IKJntList = IKJntList[::-1]
    FKJntList = FKJntList[::-1]
    
    # create IK chain
    CreateIK(IKJntList)    
    CreateFK(FKJntList)
    
# ================================ # 
def ConnectIKFKConstr(utilNode, Constr, prefix, jnt, Switch_CTRL):
    
    constrAttr = pm.listAttr( str(Constr), st= str(prefix) + str(jnt) + '*')   

    pm.connectAttr(str(Switch_CTRL) + '.IK_FK_Switch', str(Constr) + '.' + str(constrAttr[1]), force = True)
    pm.connectAttr(str(utilNode) + '.outputX', str(Constr) + '.' + str(constrAttr[0]), force = True)

# ================================ #    
def CreateFinger(side, prefix, jntList, wristJnt, wristPos, finger, pos, jntRadius):
    
    # create metacarpal jnt
    FingerMeta = pm.joint(n = str(prefix) + str(finger) + '_finder_metacarpal_jnt', p = (0,0,0), rad = jntRadius)  
    pm.parent(FingerMeta, world = True)
    pm.move(FingerMeta, (wristPos[0] + pos[0], wristPos[1] + pos[1], wristPos[2] + pos[2]))
    pm.parent(FingerMeta, wristJnt)
    CleanHist(FingerMeta)
    
    # create rest of jnts
    Knuckle = pm.joint(n = str(prefix) + str(finger) + '_finger_knuckle_jnt', r = True, p = (side * 0.5, 0,0), rad = jntRadius)
    Joint1 = pm.joint(n = str(prefix) + str(finger) + '_finder_1_jnt', r = True, p = (side * 0.3,0,0), rad = jntRadius)
    Joint2 = pm.joint(n = str(prefix) + str(finger) + '_finder_2_jnt', r = True, p = (side * 0.3,0,0), rad = jntRadius)
    JointEnd = pm.joint(n = str(prefix) + str(finger) + '_finder_End_jnt', r = True, p = (side * 0.3,0,0), rad = jntRadius)
    
    # add jnts to list
    jntList.extend([FingerMeta, Knuckle, Joint1, Joint2, JointEnd]) 
    
    # set orientations
    pm.joint(FingerMeta, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(Knuckle, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(Joint1, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(Joint2, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(JointEnd, e=True, zso = True, oj='xyz', sao = 'yup')
    
# ================================ #     
def CreateHand(side, wristJnt, jntRadius):
    
    handJntList = []
    prefix = str(wristJnt[0:2])
        
    pm.select(wristJnt)
    wristPos = cmds.xform( query=True, translation=True, worldSpace=True )
    
    CreateFinger(side, prefix, handJntList, wristJnt, wristPos, 'middle', ((side *0.3), -0.05, 0.1), jntRadius)
    CreateFinger(side, prefix, handJntList, wristJnt, wristPos, 'index', ((side * 0.3), -0.06, 0.25), jntRadius)
    

    
    #pm.select(middleFingerMeta)
    #metaPos = cmds.xform( query=True, translation=True, worldSpace=True )
    
  
# ================================ # 
def CreateArm(jntList, IKJntList, FKJntList, CTRLs, prefix, jntRadius):
    
    side = 1
    if prefix == 'R_':
        side = -1

    # create simple arm jnts
    clavicle = pm.joint(n = str(prefix) + 'clavicle_jnt', p = (side * 0.4,0,0), rad = jntRadius)
    shoulder = pm.joint(n = str(prefix) + 'shoulder_jnt', p = (side * 1.3,0.3,0.4), rad = jntRadius) 
    elbow = pm.joint(n = str(prefix) + 'elbow_jnt', p = (side * 3,0,0), rad = jntRadius) 
 
    dist = Distance(shoulder,elbow)
    wrist = pm.joint(n = str(prefix) + 'wrist_jnt', p = ( side *(3 + dist),-0.3,0.4), rad = jntRadius) 
    pm.parent(clavicle, world=True) 
    
    # set jnt orientation
    pm.joint(clavicle, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(shoulder, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(elbow, e=True, zso = True, oj='xyz', sao = 'yup')
    pm.joint(wrist, e=True, zso = True, oj='none')

    # add jnts to list & create IK FK jnts    
    jntList.extend([clavicle, shoulder, elbow, wrist])
    
    CreateHand(side, wrist, jntRadius)
    
    
    """
    # create IK FK jnts
    IK_FKChain(jntList, IKJntList, FKJntList)   
    IKJntList = IKJntList[::-1]
    FKJntList = FKJntList[::-1]

    # create twist joints    
    twistJntRadius = jntRadius + 0.1
    #CreateTwistJnt(jntList, twistJntRadius, 'shoulder_twist_jnt', prefix, shoulder, 'none', False, True)
    #CreateTwistJnt(twistJntRadius, 'bicep_twist_jnt', prefix, shoulder, elbow, True, True)
    #CreateTwistJnt(twistJntRadius, 'elbow_upper_twist_jnt', prefix, elbow, shoulder, False, False)
    #CreateTwistJnt(twistJntRadius, 'elbow_twist_jnt', prefix, elbow, 'none', False, True)
    #CreateTwistJnt(twistJntRadius, 'radius_twist_jnt', prefix, elbow, wrist, True, True)
    #CreateTwistJnt(twistJntRadius, 'wrist_twist_jnt', prefix, wrist, elbow, False, False)
             
    # constrain jnts to IK and FK jnts 
    shoulderConstr = pm.parentConstraint(FKJntList[0], IKJntList[0], str(shoulder), mo = False, w=1)
    elbowConstr = pm.parentConstraint(FKJntList[1], IKJntList[1], str(elbow), mo = False, w=1)
    wristConstr = pm.parentConstraint(FKJntList[2], IKJntList[2], str(wrist), mo = False, w=1)
    
    #create IK/FK Switch ctrl
    Switch_CTRL = str(prefix) + 'IK_FK_Switch_CTRL'
    CreateStarCTRL(Switch_CTRL, 0.5, [0.3,0.3,0.3], (0,0,1))
    pm.addAttr(longName='IK_FK_Switch', at = 'double', defaultValue=0.0, minValue=0.0, maxValue=1)
    pm.setAttr(str(Switch_CTRL) + '.IK_FK_Switch', k = True)

    # move offset GRP to wrist jnt, remove const
    tempConst = pm.parentConstraint(wrist, str(Switch_CTRL), mo = False, sr= ['x', 'y', 'z'])
    pm.delete(tempConst)
   
    pm.move(str(Switch_CTRL), (side * 0.3,0.6, -1 ),  relative = True)
    CleanHist(Switch_CTRL)
    
    # connect IK FK with constraints
    revUtility = pm.shadingNode('reverse', n= str(prefix) + 'arm_IK_FK_reverse_node', asUtility=True)
    pm.connectAttr(str(Switch_CTRL) + '.IK_FK_Switch', str(revUtility) + '.inputX', force = True)
    
    ConnectIKFKConstr(revUtility, shoulderConstr, prefix, 'shoulder', Switch_CTRL)
    ConnectIKFKConstr(revUtility, elbowConstr, prefix, 'elbow', Switch_CTRL)
    ConnectIKFKConstr(revUtility, wristConstr, prefix, 'wrist', Switch_CTRL)
    

    pm.orientConstraint(str(prefix) + 'arm_IK_CTRL', IKJntList[2], mo = False)
    pm.connectAttr(str(Switch_CTRL) + '.IK_FK_Switch', str(prefix) + 'arm_IK_CTRL_offset_GRP.visibility', force = True)
    pm.connectAttr(str(Switch_CTRL) + '.IK_FK_Switch', str(prefix) + 'pole_vector_offset_GRP.visibility', force = True)
    pm.connectAttr(str(revUtility) + '.outputX', str(prefix) + 'shoulder_FK_CTRL_offset_GRP.visibility', force = True)
    
    IK_GRP = pm.group( em=True, name= str(prefix) + 'IK_GRP' )
    pm.parent(str(IKJntList[0]) , IK_GRP)
  
    
    FK_GRP = pm.group( em=True, name= str(prefix) + 'FK_GRP' )
    pm.parent(str(FKJntList[0]) , FK_GRP)
    """
    

# ======================================================================== # 


jointList = []
IKjointList = []
FKjointList = []
CTRLs = []

jointList2 = []
IKjointList2 = []
FKjointList2 = []
CTRLs2 = []


#CreateArm(jointList, IKjointList, FKjointList, CTRLs, 'R_', 0.1)
CreateArm(jointList2, IKjointList2, FKjointList2, CTRLs2, 'L_', 0.1)
#rigging_GRP = pm.group( em=True, name= 'rigg_GRP' )

