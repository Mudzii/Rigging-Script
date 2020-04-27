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
def CreateIK(jntIKList, ctrl_GRP):
    
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

    ctrl_GRP.extend([str(Arm_CTRL) + '_offset_GRP', pole_GRP])
    
# ================================ # 
def CreateFK(jntFKList,ctrl_GRP):

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
        
    ctrl_GRP.extend([str(shoulder_CTR_Name) + '_offset_GRP' ,str(wrist_CTR_Name) + '_offset_GRP', str(elbow_CTR_Name) + '_offset_GRP'])
            
# ================================ # 

def IK_FKChain(jnList, IKJntList, FKJntList, ctrl_GRP):
       
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
    CreateIK(IKJntList,ctrl_GRP)    
    CreateFK(FKJntList,ctrl_GRP)
    
# ================================ # 
def ConnectIKFKConstr(utilNode, Constr, prefix, jnt, Switch_CTRL):
    
    constrAttr = pm.listAttr( str(Constr), st= str(prefix) + str(jnt) + '*')   

    pm.connectAttr(str(Switch_CTRL) + '.IK_FK_Switch', str(Constr) + '.' + str(constrAttr[1]), force = True)
    pm.connectAttr(str(utilNode) + '.outputX', str(Constr) + '.' + str(constrAttr[0]), force = True)

# ================================ #    
def CreateFinger(side, prefix, jntList, wristJnt, wristPos, finger, pos, jntRadius):
    
    newPos = [0,0,0] 
    if prefix == 'R_':
        newPos[0] = -0.2
        newPos[1] = -0.1
        newPos[2] = pos[2] * -1
        
    else:  
        newPos[0] = 0.2
        newPos[1] = 0.1
        newPos[2] = pos[2]  
    
    # create metacarpal jnt
    FingerMeta = pm.joint(n = str(prefix) + str(finger) + '_finder_metacarpal_jnt', p = (0,0,0), rad = jntRadius)  
    pm.parent(FingerMeta, world = True)

    pm.move(FingerMeta, (wristPos[0] + pos[0], wristPos[1] + pos[1], wristPos[2] + newPos[2]))
        
    pm.parent(FingerMeta, wristJnt)
    CleanHist(FingerMeta)
    
    if finger is not 'thumb':
        # create rest of jnts
        Knuckle = pm.joint(n = str(prefix) + str(finger) + '_finger_knuckle_jnt', r = True, p = (side * newPos[0] + (-1 * -0.2), 0,0), rad = jntRadius)
        Joint1 = pm.joint(n = str(prefix) + str(finger) + '_finder_1_jnt', r = True, p = ((side * newPos[0]),0,0), rad = jntRadius)
        Joint2 = pm.joint(n = str(prefix) + str(finger) + '_finder_2_jnt', r = True, p = (side * newPos[0],0,0), rad = jntRadius)
        JointEnd = pm.joint(n = str(prefix) + str(finger) + '_finder_End_jnt', r = True, p = (side * newPos[0],0,0), rad = jntRadius)
    
        # add jnts to list
        jntList.extend([FingerMeta, Knuckle, Joint1, Joint2, JointEnd]) 
    
        # set orientations
        pm.joint(FingerMeta, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(Knuckle, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(Joint1, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(Joint2, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(JointEnd, e=True, zso = True, oj='xyz', sao = 'yup')
        
    if finger is 'thumb':
        Knuckle = pm.joint(n = str(prefix) + str(finger) + '_finger_knuckle_jnt', r = True, p = (side * newPos[0], 0,(side * 0.25)), rad = jntRadius)
        Joint1 = pm.joint(n = str(prefix) + str(finger) + '_finder_1_jnt', r = True, p = ((side * newPos[1]),0,(side * 0.15)), rad = jntRadius)
        JointEnd = pm.joint(n = str(prefix) + str(finger) + '_finder_End_jnt', r = True, p = ((side * newPos[1]),0,(side * 0.15)), rad = jntRadius)
        
        # add jnts to list
        jntList.extend([FingerMeta, Knuckle, Joint1, JointEnd]) 
    
        # set orientations
        pm.joint(FingerMeta, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(Knuckle, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(Joint1, e=True, zso = True, oj='xyz', sao = 'yup')
        pm.joint(JointEnd, e=True, oj='none', zso = True)
    
# ================================ #     
def CreateHand(side, wristJnt, jntRadius):
    
    handJntList = []
    prefix = str(wristJnt[0:2])
        
    #pm.select(wristJnt)
    wristPos = cmds.xform(str(wristJnt), query=True, translation=True, worldSpace=True )
    
    CreateFinger(side, prefix, handJntList, wristJnt, wristPos, 'middle', ((side *0.3), -0.05, 0.1), jntRadius)
    CreateFinger(side, prefix, handJntList, wristJnt, wristPos, 'index', ((side * 0.3), -0.06, 0.25), jntRadius)
    CreateFinger(side, prefix, handJntList, wristJnt, wristPos, 'ring', ((side * 0.35), -0.06, -0.05), jntRadius)
    CreateFinger(side, prefix, handJntList, wristJnt, wristPos, 'pinky', ((side * 0.4), -0.09, -0.2), jntRadius)
      
    CreateFinger(side, prefix, handJntList, wristJnt, wristPos, 'thumb', ((side * 0.15), -0.1, (side * 0.3)), jntRadius)
    
    return handJntList
  
# ================================ # 
def CreateArm(WS_LOC, spaceGrps, rigging_GRP, ctrl_GRP, skeleton_GRP, jntList, IKJntList, FKJntList, CTRLs, prefix, jntRadius):
    
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
    
    # create IK FK jnts
    IK_FKChain(jntList, IKJntList, FKJntList, CTRLs)   
    IKJntList = IKJntList[::-1]
    FKJntList = FKJntList[::-1]
    
    # create hand
    handJntList = CreateHand(side, wrist, jntRadius)
    jntList.extend(handJntList)
    

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
    Switch_Offset_GRP = str(Switch_CTRL) + '_offset_GRP'
    CreateStarCTRL(Switch_CTRL, 0.5, [0.3,0.3,0.3], (0,0,1))
    pm.addAttr(longName='IK_FK_Switch', at = 'double', defaultValue=0.0, minValue=0.0, maxValue=1)
    pm.setAttr(str(Switch_CTRL) + '.IK_FK_Switch', k = True)
    

    # move offset GRP to wrist jnt, remove const
    tempConst = pm.parentConstraint(wrist, str(Switch_CTRL), mo = False, sr= ['x', 'y', 'z'])
    pm.delete(tempConst)
   
    pm.move(str(Switch_CTRL), (side * 0.3,0.6, -1 ),  relative = True)
    CleanHist(Switch_CTRL)
    
    pm.xform(str(Switch_Offset_GRP), cp = True)
    
    # IK FK switch line
    Switch_Line = pm.curve(n = str(prefix) + 'IK_FK_VIS',d=1, p=[(0, 0, 0),(-1, 0, 0)], k=[0,1] )
    curvePoints = cmds.ls('{0}.cv[:]'.format(Switch_Line), fl = True)
    
    wristPos = cmds.xform(str(wrist), query=True, translation=True, worldSpace=True ) 
    CTRL_Pos = cmds.xform(str(Switch_CTRL), query=True, translation=True, worldSpace=True )
    
    pm.move( curvePoints[1], wristPos)
    pm.move( curvePoints[0], ((side * 5.07),-0.11,-0.6))  
    CleanHist(Switch_Line)
    
    pm.xform(str(Switch_Line), cp = True)
    pm.parent(Switch_Line, str(ctrl_GRP))    
    
    wristCluster = pm.cluster(curvePoints[1], n = (str(wrist) + '_IKFK_line_cluster'))
    CTRL_cluster = pm.cluster(curvePoints[0], n = (str(Switch_CTRL) + '_IKFK_line_cluster'))
    
    tempClusterConst = pm.parentConstraint(str(wrist), str(wristCluster[1]), mo = False, w = 1)
    
    tempCtrlConst = pm.parentConstraint(str(wrist), str(Switch_Offset_GRP), mo=True, w = 1)
    pm.parent(str(CTRL_cluster[1]), str(Switch_Offset_GRP))
    pm.parent(str(wristCluster[1]), str(ctrl_GRP))
   
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
    
    #create grps for IK FK jnts
    IK_GRP = pm.group( em=True, name= str(prefix) + 'IK_GRP' )
    pm.parent(str(IKJntList[0]) , IK_GRP)
   
    FK_GRP = pm.group( em=True, name= str(prefix) + 'FK_GRP' )
    pm.parent(str(FKJntList[0]) , FK_GRP)
    
    arm_GRP = pm.group( em=True, name= str(prefix) + 'arm_GRP' )
    pm.parent(FK_GRP, arm_GRP)
    pm.parent(IK_GRP, arm_GRP)
    
    # tidy up
    CTRLs.append(str(Switch_CTRL) + '_offset_GRP')
    pm.parent(arm_GRP, rigging_GRP)
    pm.parent(jntList[0], skeleton_GRP)
    
    pm.parent(CTRLs[0], ctrl_GRP)
    pm.parent(CTRLs[1], ctrl_GRP)
    pm.parent(CTRLs[2], ctrl_GRP)
    pm.parent(CTRLs[5], ctrl_GRP)
    
    
    
    # parent switch ----------------------------------------------------
    Hand_Space_GRP = pm.group( em=True, name= str(prefix) + 'Hand_Space')
    spaceGrps.append(Hand_Space_GRP)
    
    pm.parent(Hand_Space_GRP, spaceGrps[0])
    
    hand_offset_GRP = ''
    for i in range(len(CTRLs)):
	    if str(CTRLs[i]) == str(prefix) + 'arm_IK_CTRL_offset_GRP':
		    hand_offset_GRP = CTRLs[i]
    
    armSpaceConst = pm.parentConstraint(str(hand_offset_GRP), str(Hand_Space_GRP), mo = False, w = 1)
    
    world_HandSpace_GRP = pm.group( em=True, name= str(prefix) + 'world_Hand_space')
    HandSpace_Pos = pm.xform(str(Hand_Space_GRP), q=1, ws=1, rp=1)
 	
    pm.setAttr(world_HandSpace_GRP + ".rotatePivotX", HandSpace_Pos[0])
    pm.setAttr(world_HandSpace_GRP + ".rotatePivotY", HandSpace_Pos[1])
    pm.setAttr(world_HandSpace_GRP + ".rotatePivotZ", HandSpace_Pos[2])
    pm.setAttr(world_HandSpace_GRP + ".scalePivotX", HandSpace_Pos[0])
    pm.setAttr(world_HandSpace_GRP + ".scalePivotY", HandSpace_Pos[1])
    pm.setAttr(world_HandSpace_GRP + ".scalePivotZ", HandSpace_Pos[2])
    
    pm.parent(world_HandSpace_GRP, spaceGrps[1])
    HandCTRLSpace_GRP = pm.group( em=True, name= str(prefix) + 'Hand_CTRL_space')
    HandCTRLSpace_CTRL = pm.listRelatives(str(hand_offset_GRP))
   
    
    pm.setAttr(HandCTRLSpace_GRP + ".rotatePivotX", HandSpace_Pos[0])
    pm.setAttr(HandCTRLSpace_GRP + ".rotatePivotY", HandSpace_Pos[1])
    pm.setAttr(HandCTRLSpace_GRP + ".rotatePivotZ", HandSpace_Pos[2])
    pm.setAttr(HandCTRLSpace_GRP + ".scalePivotX", HandSpace_Pos[0])
    pm.setAttr(HandCTRLSpace_GRP + ".scalePivotY", HandSpace_Pos[1])
    pm.setAttr(HandCTRLSpace_GRP + ".scalePivotZ", HandSpace_Pos[2])
    
    
    pm.parent(HandCTRLSpace_GRP,hand_offset_GRP)   
    pm.parent(HandCTRLSpace_CTRL, HandCTRLSpace_GRP)
    CleanHist(HandCTRLSpace_CTRL)
    
    world_HandSpace_Inbetween_GRP = pm.group( em=True, name= str(prefix) + 'world_Hand_space_inbetween')
    pm.setAttr(world_HandSpace_Inbetween_GRP + ".rotatePivotX", HandSpace_Pos[0])
    pm.setAttr(world_HandSpace_Inbetween_GRP + ".rotatePivotY", HandSpace_Pos[1])
    pm.setAttr(world_HandSpace_Inbetween_GRP + ".rotatePivotZ", HandSpace_Pos[2])
    pm.setAttr(world_HandSpace_Inbetween_GRP + ".scalePivotX", HandSpace_Pos[0])
    pm.setAttr(world_HandSpace_Inbetween_GRP + ".scalePivotY", HandSpace_Pos[1])
    pm.setAttr(world_HandSpace_Inbetween_GRP + ".scalePivotZ", HandSpace_Pos[2])
    
    pm.parent(world_HandSpace_Inbetween_GRP, hand_offset_GRP)
    CleanHist(world_HandSpace_Inbetween_GRP)
    
    world_inbetween_Const = pm.parentConstraint(str(world_HandSpace_GRP), str(world_HandSpace_Inbetween_GRP), mo = False, w = 1)
    
    
    #WS_LOC
    #spaceGrps


# ======================================================================== # 


jointList = []
IKjointList = []
FKjointList = []
CTRLs = []

jointList2 = []
IKjointList2 = []
FKjointList2 = []
CTRLs2 = []




rigging_GRP = pm.group( em=True, name= 'rigging_GRP' )
ctrl_GRP = pm.group( em=True, name= 'controllers_GRP' )
skeleton_GRP = pm.group( em=True, name= 'skeleton_GRP' )

spaceGrps = []
world_LOC = pm.spaceLocator(n ='worldSpace_LOC')

spaces_GRP = pm.group( em=True, name= 'spaces_GRP')
world_GRP = pm.group( em=True, name= 'world_Space')

spaceGrps.append(spaces_GRP)
spaceGrps.append(world_GRP)

#L_Hand_GRP = pm.group( em=True, name= 'L_Hand_Space')
#R_Hand_GRP = pm.group( em=True, name= 'R_Hand_Space')

pm.parent(world_GRP, spaces_GRP)
WorldSpaceConst = pm.parentConstraint(str(world_LOC), str(world_GRP), mo = False, w = 1)

#pm.parent(L_Hand_GRP, spaces_GRP)
#pm.parent(R_Hand_GRP, spaces_GRP)

#CreateArm(jointList, IKjointList, FKjointList, CTRLs, 'R_', 0.1)
#CreateArm(rigging_GRP, ctrl_GRP, skeleton_GRP, jointList2, IKjointList2, FKjointList2, CTRLs2, 'R_', 0.1)
CreateArm(world_LOC, spaceGrps, rigging_GRP, ctrl_GRP, skeleton_GRP, jointList, IKjointList, FKjointList, CTRLs, 'L_', 0.1)

