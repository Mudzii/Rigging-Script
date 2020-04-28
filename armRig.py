# ================================ #
# ================================ #
import pymel.core as pm
import maya.cmds as cmds
import createControllers
import createJoints
# ================================ #
# ================================ #


#  ================= Function to create IK Arm ========================================= #
def CreateIK(prefix, jntIKList, ctrl_GRP):
    

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
