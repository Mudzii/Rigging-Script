
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


#  ================= Function to connect IKFK switch =================================== #
def ConnectIKFKSwitch(prefix, Switch_CTRL, CTRLs_GRP, elbowIK, constrGRP): 
    

    switchAttr = pm.listAttr(Switch_CTRL, s = True, k = True, v = True)
    lenAttr = len(switchAttr)
    IKFKSwitchAttr = switchAttr[lenAttr - 1]
   
    # create reverse utility node
    revUtility = pm.shadingNode('reverse', n= str(prefix) + 'arm_IK_FK_reverse_node', asUtility=True)
    pm.connectAttr(str(Switch_CTRL) + '.' + str(IKFKSwitchAttr), str(revUtility) + '.inputX', force = True)
     
    #ConnectIKFKConstr(utilNode, Constr, prefix, jnt, Switch_CTRL):
    createJoints.ConnectIKFKConstr(revUtility, constrGRP[0], prefix, 'shoulder', Switch_CTRL)
    createJoints.ConnectIKFKConstr(revUtility, constrGRP[1], prefix, 'elbow', Switch_CTRL)
    createJoints.ConnectIKFKConstr(revUtility, constrGRP[2], prefix, 'wrist', Switch_CTRL)
    
    
    ArmInd = CTRLs_GRP.index( str(prefix) + 'arm_IK_CTRL_offset_GRP')
    arm_CTRL = pm.listRelatives(CTRLs_GRP[ArmInd])[0]
    
    PoleInd = CTRLs_GRP.index( str(prefix) + 'pole_vector_offset_GRP')
    ShoulderInd = CTRLs_GRP.index( str(prefix) + 'shoulder_FK_CTRL_offset_GRP')
    
    # constrain
    pm.orientConstraint(arm_CTRL, elbowIK, mo = False)
    
    pm.connectAttr(str(Switch_CTRL) + '.' + str(IKFKSwitchAttr), str(CTRLs_GRP[ArmInd]) + '.visibility', force = True)
    pm.connectAttr(str(Switch_CTRL) + '.' + str(IKFKSwitchAttr), str(CTRLs_GRP[PoleInd]) + '.visibility', force = True)
    
    pm.connectAttr(str(revUtility) + '.outputX', str(CTRLs_GRP[ShoulderInd]) + '.visibility', force = True)
    

#  ================= Function to create FK CTRLS ======================================= #
def CreateFK(prefix, jntFKList,ctrl_GRP):
    
    offset_GRP_Name = '_offset_GRP'

    # shoulder CTRL
    shoulder_CTR_Name = str(prefix) + 'shoulder_FK_CTRL'  
    createControllers.CreateCircleCTRL(str(shoulder_CTR_Name), ctrl_GRP, jntFKList[0], (0,1,0), 0.6, (0,0,-100))
    
    # elbow CTRL
    elbow_CTR_Name = str(prefix) + 'elbow_FK_CTRL'  
    createControllers.CreateCircleCTRL(str(elbow_CTR_Name), ctrl_GRP, jntFKList[1], (0,1,0), 0.5, (0,0,-100))
    
    # wrist CTRL
    wrist_CTR_Name = str(prefix) + 'wrist_FK_CTRL'  
    createControllers.CreateCircleCTRL(str(wrist_CTR_Name), ctrl_GRP, jntFKList[2], (0,1,0), 0.3, (0,0,-100))
    
    # parent GTRLS
    pm.parent(str(wrist_CTR_Name) + str(offset_GRP_Name), elbow_CTR_Name)
    pm.parent(str(elbow_CTR_Name) + str(offset_GRP_Name), shoulder_CTR_Name)
 
    # add CTRL to list    
    ctrl_GRP.extend([str(shoulder_CTR_Name) + str(offset_GRP_Name) ,str(wrist_CTR_Name) + str(offset_GRP_Name), str(elbow_CTR_Name) + str(offset_GRP_Name)])
            

#  ================= Function to create IK CTRLS ======================================= #
def CreateIK(prefix, jntIKList, ctrl_GRP):
    
    offset_GRP_Name = '_offset_GRP'
       
    # create arm CTRL ========================
    Arm_CTRL = str(prefix) + "arm_IK_CTRL"
    Arm_Offset_GRP = str(Arm_CTRL) + str(offset_GRP_Name)
    createControllers.CreateStarCTRL(Arm_CTRL, ctrl_GRP, 0.6, [0.4, 0.4, 0.4], (1,0,0))
    
    # move offset GRP to wrist jnt, remove const
    tempConst = pm.parentConstraint(jntIKList[2], str(Arm_Offset_GRP))
    pm.delete(tempConst)

    # create IK handle 
    arm_ik = pm.ikHandle( n = str(prefix) + 'IK_Handle', sj=jntIKList[0], ee=jntIKList[2])
    pm.parent(arm_ik[0], Arm_CTRL)    
     
    # create pole vector CTRL ================
    poleVector_CTRL = str(prefix) + 'pole_vector'
    pole_GRP = str(poleVector_CTRL) + str(offset_GRP_Name)
    createControllers.CreateBallCTRL(str(poleVector_CTRL), ctrl_GRP, 0.15)
   
    # move offset GRP to wrist jnt, remove const
    tempConst = pm.parentConstraint(jntIKList[1], str(pole_GRP), sr = ['x', 'y', 'z'])
    pm.delete(tempConst)
    createControllers.CleanHist(pole_GRP)    
  
    # point + aim constraint CTRL to prevent joint from moving after pole V Constr
    pointConst = pm.pointConstraint( str(jntIKList[0]), str(jntIKList[2]), str(poleVector_CTRL), mo= False, w=1 )
    pm.delete(pointConst)
 
    aimConst = pm.aimConstraint( str(jntIKList[1]), str(poleVector_CTRL), mo= False, w=1 )
    pm.delete(aimConst)
       
    # constrain PV
    PVConstr = pm.poleVectorConstraint(poleVector_CTRL, arm_ik[0], n = str(poleVector_CTRL) + '_constraint')
    pm.move(str(poleVector_CTRL), (1,0, 0 ), os = True, wd = False, relative = True)
    
    # clean hist, parent and add CTRS to list
    createControllers.CleanHist(poleVector_CTRL)   
    pm.parent(poleVector_CTRL, pole_GRP) 
    ctrl_GRP.extend([str(Arm_Offset_GRP), pole_GRP])


#  ================= Function to create IKFK Chain ====================================== #
def IK_FKChain(prefix, jnList, IKJntList, FKJntList, ctrl_GRP):
    
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
    
    
    CreateIK(prefix, IKJntList,ctrl_GRP)
    
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
    
    CreateFK(prefix, FKJntList,ctrl_GRP)

#  ================= Function to create Arm ============================================ #
#def CreateArm(WS_LOC, spaceGrps, rigging_GRP, ctrl_GRP, skeleton_GRP, vis_aid_GRP, jntList, IKJntList, FKJntList, CTRLs, prefix, jntRadius):

def CreateArm(WS_LOC, space_Grps, rigging_GRPs, CTRLs_GRP, prefix, jntList, IKJntList, FKJntList, jntRadius):
    
    imp.reload(createControllers)
    imp.reload(createJoints)
    
    
    # ================================================================== *
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
    IK_FKChain(prefix, jntList, IKJntList, FKJntList, CTRLs_GRP)
    IKJntList = IKJntList[::-1]
    FKJntList = FKJntList[::-1]
    
    # constrain jnts to IK/FK
    constrGRP = []
    
    shoulderConstr = pm.parentConstraint(FKJntList[0], IKJntList[0], str(shoulder), mo = False, w=1)
    elbowConstr = pm.parentConstraint(FKJntList[1], IKJntList[1], str(elbow), mo = False, w=1)
    wristConstr = pm.parentConstraint(FKJntList[2], IKJntList[2], str(wrist), mo = False, w=1)
    
    constrGRP.extend([shoulderConstr, elbowConstr, wristConstr])     
    
    # ===================== create Hand ================================ *
    handJntList = createJoints.CreateHand(prefix, axis, wrist, jntRadius)
    jntList.extend(handJntList)     

    # ===================== create Twist Jnts ========================== *
    #twistJntList = createJoints.CreateArmTwistJnts(prefix, jntList, jntRadius)
    
    # ===================== create IKFK Switch ========================== *
    Switch_CTRL = str(prefix) + 'IK_FK_Switch_CTRL'
    Switch_CTRL_Line = str(prefix) + 'IK_FK_VIS'
    
    clusterGRP = createControllers.CreateIKFKSwitch(axis, Switch_CTRL, CTRLs_GRP, Switch_CTRL_Line, wrist) 

    ConnectIKFKSwitch(prefix, Switch_CTRL, CTRLs_GRP, IKJntList[2], constrGRP)
    
    # ===================== Tidy ======================================= *
    
    # group vis & clusters
    pm.parent(Switch_CTRL_Line, rigging_GRPs[3])
    pm.parent(str(clusterGRP[1][1]), str(Switch_CTRL) + str(offset_GRP_Name))
    pm.parent(str(clusterGRP[0][1]), str(rigging_GRPs[1]))
    
    # group ctrls
    pm.parent(str(CTRLs_GRP[0]), str(rigging_GRPs[1]))
    pm.parent(str(CTRLs_GRP[1]), str(rigging_GRPs[1]))
    pm.parent(str(CTRLs_GRP[2]), str(rigging_GRPs[1]))
    
    pm.parent(str(CTRLs_GRP[5]), str(clavicle_Ctrl))   

    # group IK/FK jnts
    IK_GRP = pm.group( em=True, name= str(prefix) + 'IK_GRP' )
    pm.parent(str(IKJntList[0]) , IK_GRP)
   
    FK_GRP = pm.group( em=True, name= str(prefix) + 'FK_GRP' )
    pm.parent(str(FKJntList[0]) , FK_GRP)
    
    arm_GRP = pm.group( em=True, name= str(prefix) + 'arm_GRP' )
    pm.parent(FK_GRP, arm_GRP)
    pm.parent(IK_GRP, arm_GRP)
    
    pm.parent(arm_GRP, rigging_GRPs[0])
    pm.parent(jntList[0], rigging_GRPs[2])
    
    pm.parent(str(CTRLs_GRP[11]), str(rigging_GRPs[4]))   
    
    # constrain arm grp to clavicle 
    pm.parentConstraint(clavicle_Ctrl,arm_GRP, mo = True, w = 1) 

    
# ====================================================================================== #    
# ====================================================================================== #    


rigging_GRPs = []

rigging_GRP = pm.group( em=True, name= 'rigging_GRP' )
ctrl_GRP = pm.group( em=True, name= 'controllers_GRP' )
skeleton_GRP = pm.group( em=True, name= 'skeleton_GRP' )
vis_GRP= pm.group( em=True, name= 'vis_aid' )
switch_GRP= pm.group( em=True, name= 'IKFK_Switch_GRP' )

rigging_GRPs.extend([rigging_GRP, ctrl_GRP, skeleton_GRP, vis_GRP, switch_GRP])
pm.parent(vis_GRP, rigging_GRP)

"""
spaceGrps = []
world_LOC = pm.spaceLocator(n ='worldSpace_LOC')

spaces_GRP = pm.group( em=True, name= 'spaces_GRP')
world_GRP = pm.group( em=True, name= 'world_Space')

spaceGrps.append(spaces_GRP)
spaceGrps.append(world_GRP)
"""

jntList = []
CTRL_List = []
IKJntList = []
FKJntList = []
jntRadius = 0.1

CreateArm('na', 'na', rigging_GRPs, CTRL_List, 'L_', jntList, IKJntList, FKJntList, jntRadius)


jntList2 = []
CTRL_List2 = []
IKJntList2 = []
FKJntList2 = []
jntRadius2 = 0.1

CreateArm('na', 'na', rigging_GRPs, CTRL_List2, 'R_', jntList2, IKJntList2, FKJntList2, jntRadius2)
    
